#Author: Louis Chuo
# Code for finetuning a pretrained model availbale on speechbrain
# Code based off: https://colab.research.google.com/drive/1LN7R3U3xneDgDRK2gC5MzGkLysCWxuC3?usp=sharing


import speechbrain as sb
from speechbrain.lobes.features import Fbank
import torch
from speechbrain.pretrained import EncoderDecoderASR
from speechbrain.dataio.dataset import DynamicItemDataset
from speechbrain.utils.checkpoints import Checkpointer
import torchaudio
import jiwer
from pandas import *
import shutil
import os

checkpoint_dir = "./saved_checkpoint_MZ_only"
checkpointer = Checkpointer(checkpoint_dir)

transformation = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveWhiteSpace(replace_by_space=True),
    jiwer.RemoveMultipleSpaces(),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
]) 

mer_list = []
csv_file = read_csv("valid_data_new.csv")
filepaths = csv_file['file_path'].tolist()
baselines = csv_file['words'].tolist()
counter = 0

asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="./pretrained_ASR", run_opts={"device":"cuda:0"}) #https://huggingface.co/speechbrain/asr-crdnn-rnnlm-librispeech

dataset = DynamicItemDataset.from_csv("combined_train_data_MZ_only.csv")
dataset.add_dynamic_item(sb.dataio.dataio.read_audio, takes="file_path", provides="signal")

# Define audio pipeline:
@sb.utils.data_pipeline.takes("file_path")
@sb.utils.data_pipeline.provides("signal")
def audio_pipeline(wav):
    info = torchaudio.info(wav)
    sig = sb.dataio.dataio.read_audio(wav)
    resampled = torchaudio.transforms.Resample(
        info.sample_rate, 16000,
    )(sig)
    return resampled

dataset.add_dynamic_item(audio_pipeline)


# Define text pipeline:
@sb.utils.data_pipeline.takes("words")
@sb.utils.data_pipeline.provides(
        "words", "tokens_list", "tokens_bos", "tokens_eos", "tokens")
def text_pipeline(words):
      yield words
      tokens_list = asr_model.tokenizer.encode_as_ids(words)
      yield tokens_list
      tokens_bos = torch.LongTensor([asr_model.hparams.bos_index] + (tokens_list))
      yield tokens_bos
      tokens_eos = torch.LongTensor(tokens_list + [asr_model.hparams.eos_index]) # we use same eos and bos indexes as in pretrained model
      yield tokens_eos
      tokens = torch.LongTensor(tokens_list)
      yield tokens


dataset.add_dynamic_item(text_pipeline)
dataset.set_output_keys(["id", "signal", "words", "tokens_list", "tokens_bos", "tokens_eos", "tokens"])
dataset[0]

# Define fine-tuning procedure 
class EncDecFineTune(sb.Brain):

    def on_stage_start(self, stage, epoch):
        # enable grad for all modules we want to fine-tune
        if stage == sb.Stage.TRAIN:
            for module in [self.modules.enc, self.modules.emb, self.modules.dec, self.modules.seq_lin]:
                for p in module.parameters():
                    p.requires_grad = True
     
    def compute_forward(self, batch, stage):
        """Forward computations from the waveform batches to the output probabilities."""
        batch = batch.to(self.device)
        wavs, wav_lens = batch.signal
        tokens_bos, _ = batch.tokens_bos
        wavs, wav_lens = wavs.to(self.device), wav_lens.to(self.device)

        # Forward pass
        feats = self.modules.compute_features(wavs)
        feats = self.modules.normalize(feats, wav_lens)
        #feats.requires_grad = True
        x = self.modules.enc(feats)
        
        e_in = self.modules.emb(tokens_bos)  # y_in bos + tokens
        h, _ = self.modules.dec(e_in, x, wav_lens)

        # Output layer for seq2seq log-probabilities
        logits = self.modules.seq_lin(h)
        p_seq = self.hparams.log_softmax(logits)

        return p_seq, wav_lens

    def compute_objectives(self, predictions, batch, stage):
        """Computes the loss (CTC+NLL) given predictions and targets."""

        
        p_seq, wav_lens = predictions

        ids = batch.id
        tokens_eos, tokens_eos_lens = batch.tokens_eos
        tokens, tokens_lens = batch.tokens

        loss = self.hparams.seq_cost(
            p_seq, tokens_eos, tokens_eos_lens)
        

        return loss

    def fit_batch(self, batch):
        """Train the parameters given a single batch in input"""
        predictions = self.compute_forward(batch, sb.Stage.TRAIN)
        loss = self.compute_objectives(predictions, batch, sb.Stage.TRAIN)
        loss.backward()
        if self.check_gradients(loss):
            self.optimizer.step()
        self.optimizer.zero_grad()
        return loss.detach()

    def evaluate_batch(self, batch, stage):
        """Computations needed for validation/test batches"""
        predictions = self.compute_forward(batch, stage=stage)
        with torch.no_grad():
            loss = self.compute_objectives(predictions, batch, stage=stage)
        return loss.detach()

modules = {"enc": asr_model.mods.encoder.model, 
           "emb": asr_model.hparams.emb,
           "dec": asr_model.hparams.dec,
           "compute_features": asr_model.mods.encoder.compute_features, # we use the same features 
           "normalize": asr_model.mods.encoder.normalize,
           "seq_lin": asr_model.hparams.seq_lin, 
           
          }

#Loads checkpoint with the lowest validation MER score
ckpt_finder = Checkpointer(checkpoint_dir)
get_ckpt = ckpt_finder.find_checkpoint(min_key="MER")
current_paramfile = get_ckpt.paramfiles["enc"]
print("The checkpoint being loaded is", current_paramfile)

# parameter transfer
sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.model, get_ckpt.paramfiles['enc'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.emb, get_ckpt.paramfiles['emb'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.dec, get_ckpt.paramfiles['dec'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.compute_features, get_ckpt.paramfiles['compute_features'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.normalize, get_ckpt.paramfiles['normalize'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.seq_lin, get_ckpt.paramfiles['seq_lin'], device='cpu')

hparams = {"seq_cost": lambda x, y, z: sb.nnet.losses.nll_loss(x, y, z, label_smoothing = 0.1),
            "log_softmax": sb.nnet.activations.Softmax(apply_log=True)}

brain = EncDecFineTune(modules, hparams=hparams, opt_class=lambda x: torch.optim.SGD(x, 1e-5),run_opts = {'device':"cuda:0"})
brain.tokenizer = asr_model.tokenizer

brain.fit(range(1), train_set=dataset, train_loader_kwargs={"batch_size": 4, "drop_last":True, "shuffle": True})

# Validation code by testing MER on a validation set
print("Starting Validation")
for filepath in filepaths :
    result = asr_model.transcribe_file(filepath)
    mer = jiwer.mer(baselines[counter], result, truth_transform=transformation, hypothesis_transform=transformation)
    
    mer_list.append(mer)
    counter = counter + 1

average = sum(mer_list)/len(mer_list)
print ("Average MER: " + str(average))


#Saves current itteration as a checkpint for further processing
checkpointer.add_recoverables(modules)
ckpt = checkpointer.save_checkpoint(meta={"MER": average})
