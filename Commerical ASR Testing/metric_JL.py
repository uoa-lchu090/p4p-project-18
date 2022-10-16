#Author: Louis Chuo
# Used to calcualte the WER, MER, and WIL from the hypothesised data and baseline data for the JL corpus

import shutil
import pandas as pd
import jiwer
import sys
import os
import re
import csv

result_path = "./speech/Results/JL_output_combined.xlsx"
result_df = pd.read_excel(result_path, sheet_name="JL_output_Microsoft_US")

wer_preprocess = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveWhiteSpace(replace_by_space=True),
    jiwer.RemoveMultipleSpaces(),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
]) 

result_file_names = result_df.get("Column1").tolist()
result_contents = result_df.get("Column2").tolist()
control_line_array = []
WER_array = []
MER_array = []
WIL_array = []

for i in range(len(result_file_names)):
    with open("speech/JL_Control/" + re.split(r"\.\s*",result_file_names[i])[0] + ".txt") as f:
        control_line = f.readline()
        #print (control_line)
        control_line_array.append(control_line)

    print(result_file_names[i])
    print(result_contents[i])
    print(control_line)

    measures = jiwer.compute_measures(control_line, result_contents[i], truth_transform=wer_preprocess, hypothesis_transform=wer_preprocess)
    wer = measures['wer']
    mer = measures['mer']
    wil = measures['wil']
    print("WER: " + str(wer))
    print("MER: " + str(mer))
    print("WIL: " + str(wil))
    WER_array.append(wer)
    MER_array.append(mer)
    WIL_array.append(wil)

x = 0
with open('speech/Measurement Results/JL_measures_Microsoft_US.csv', 'w', newline= '') as out_file:
        tsv_writer = csv.writer(out_file)
        while x < len(result_file_names) :
            tsv_writer.writerow([result_file_names[x], result_contents[x], control_line_array[x], WER_array[x], MER_array[x], WIL_array[x]])
            x += 1