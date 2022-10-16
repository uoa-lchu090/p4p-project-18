#Author: Louis Chuo
# Code for testing a model against its baseline and calculating the MER of it


from itertools import count
from pandas import *
import shutil
import os
from speechbrain.pretrained import EncoderDecoderASR
import jiwer
from speechbrain.utils.checkpoints import Checkpointer
import speechbrain as sb
import csv

checkpoint_dir = "./saved_checkpoint" #change to saved checkpoint folder containing needed model
checkpointer = Checkpointer(checkpoint_dir)

dataset = "Mozilla" #Mozilla, JL, Mansfield

transformation = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveWhiteSpace(replace_by_space=True),
    jiwer.RemoveMultipleSpaces(),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
]) 

asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="./pretrained_ASR", run_opts={"device":"cuda:0"}) #https://huggingface.co/speechbrain/asr-crdnn-rnnlm-librispeech

ckpt_finder = Checkpointer(checkpoint_dir)
get_ckpt = ckpt_finder.find_checkpoint(min_key="MER")
current_paramfile = get_ckpt.paramfiles["enc"]
print("The checkpoint being loaded is", current_paramfile)

# parameter transfer
sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.model, get_ckpt.paramfiles['enc'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.emb, get_ckpt.paramfiles['emb'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.dec, get_ckpt.paramfiles['dec'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.compute_features, get_ckpt.paramfiles['compute_features'], device='cpu')
#sb.utils.checkpoints.torch_parameter_transfer(asr_model.mods.encoder.normalize, get_ckpt.paramfiles['normalize'], device='cpu')
sb.utils.checkpoints.torch_parameter_transfer(asr_model.hparams.seq_lin, get_ckpt.paramfiles['seq_lin'], device='cpu')

mer_list = []
wer_list = []
wil_list = []
baselines_spec = []
hypothesis_array = []
filename_array = []

csv_file = read_csv("test_data_new.csv")
filepaths = csv_file['file_path'].tolist()
baselines = csv_file['words'].tolist()
counter = 0

for filepath in filepaths :
    if dataset + "_test" in filepath:
        result = asr_model.transcribe_file(filepath)
        measures = jiwer.compute_measures(baselines[counter], result, truth_transform=transformation, hypothesis_transform=transformation)

        wer = measures['wer']
        mer = measures['mer']
        wil = measures['wil']
    
        mer_list.append(mer)
        wer_list.append(wer)
        wil_list.append(wil)

        print("filename: " + os.path.basename(filepath))
        filename_array.append(os.path.basename(filepath))
        print("hypothesis: " + result)
        hypothesis_array.append(result)
        print("ground truth: " + baselines[counter])
        baselines_spec.append(baselines[counter])


        print("MER: " + str(mer))
        print("number: " + str(counter + 2))

    counter = counter + 1

    

average = sum(mer_list)/len(mer_list)
print ("Average: " + str(average))

x = 0

with open(dataset + "_test_results.csv", 'w', newline= '') as out_file:
        tsv_writer = csv.writer(out_file)
        while x < len(filename_array) :
            tsv_writer.writerow([filename_array[x], baselines_spec[x], hypothesis_array[x], wer_list[x], mer_list[x], wil_list[x]])
            x += 1