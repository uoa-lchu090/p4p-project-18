import sounddevice as sd
from scipy.io.wavfile import write
from speechbrain.pretrained import EncoderDecoderASR
from speechbrain.utils.checkpoints import Checkpointer
import speechbrain as sb

fs = 16000  # Sample rate
seconds = 5  # Duration of recording

checkpoint_dir = "./saved_checkpoint"
checkpointer = Checkpointer(checkpoint_dir)

print("Recording audio start!")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file 
print("Recording audio finished")

asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="./pretrained_ASR", run_opts={"device":"cuda:0"})

ckpt_finder = Checkpointer(checkpoint_dir)
get_ckpt = ckpt_finder.find_checkpoint(min_key="MER")
current_paramfile = get_ckpt.paramfiles["enc"]
#print("The checkpoint being loaded is", current_paramfile)

# parameter transfer
sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.model, get_ckpt.paramfiles['enc'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.emb, get_ckpt.paramfiles['emb'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.dec, get_ckpt.paramfiles['dec'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.compute_features, get_ckpt.paramfiles['compute_features'], device='cpu')
#sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.normalize, get_ckpt.paramfiles['normalize'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.seq_lin, get_ckpt.paramfiles['seq_lin'], device='cpu')

result = asr_model.transcribe_file("output.wav")

print("Guess: " + result)