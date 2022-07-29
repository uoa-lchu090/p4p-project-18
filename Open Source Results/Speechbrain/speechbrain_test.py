from unittest import result
from speechbrain.pretrained import EncoderDecoderASR
import os
import pandas as pd
import csv


asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="./pretrained_ASR")

def recognise_pretrained(file_path):
    result = asr_model.transcribe_file(file_path)
    #print(result)
    return result



if __name__ == "__main__":

    name_array = []
    result_array = []
    x = 0


    for filename in os.listdir("speech/Mozilla"):
        if filename.endswith(".mp3"):
            file_path = "speech/Mozilla/" + filename
            translated_result = recognise_pretrained(file_path)
            print(filename)
            print(translated_result)
            name_array.append(filename)
            result_array.append(translated_result)

    with open('speech/Mozilla_output_speechbrain.csv', 'w', newline= '') as out_file:
        tsv_writer = csv.writer(out_file)
        while x < len(name_array) :
            tsv_writer.writerow([name_array[x], result_array[x]])
            x += 1