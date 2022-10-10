import shutil
import pandas as pd
import jiwer
import sys
import os
import re
import csv

result_path = "./speech/Results/Mansfield_output_combined.xlsx"
result_df = pd.read_excel(result_path, sheet_name="Mansfield_output_Microsoft_US")

control_path = "./speech/mansfield_excel.xlsx"
control_df = pd.read_excel(control_path, sheet_name="metadataNZ")

result_file_names = result_df.get("Column1").tolist()
result_contents = result_df.get("Column2").tolist()

control_file_names = control_df.get("Column1").tolist()
control_contents = control_df.get("Column2").tolist()

control_match_array = []
WER_array = []
MER_array = []
WIL_array = []

wer_preprocess = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveWhiteSpace(replace_by_space=True),
    jiwer.RemoveMultipleSpaces(),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
]) 





for i in range(len(result_file_names)):
    for j in  range(len(control_file_names)):
        if ((control_file_names[j] + ".wav") == result_file_names[i]):
            control_match_array.append(control_contents[j])



    print(result_file_names[i])
    print(result_contents[i])
    print(control_match_array[i])

    if (isinstance(result_contents[i], str)):
        measures = jiwer.compute_measures(control_match_array[i], result_contents[i], truth_transform=wer_preprocess, hypothesis_transform=wer_preprocess)
        wer = measures['wer']
        mer = measures['mer']
        wil = measures['wil']
        print("WER: " + str(wer))
        print("MER: " + str(mer))
        print("WIL: " + str(wil))
        WER_array.append(wer)
        MER_array.append(mer)
        WIL_array.append(wil)
    else:
        WER_array.append(5)
        MER_array.append(5)
        WIL_array.append(5)

x = 0
with open('speech/Measurement Results/Mansfield_measures_Microsoft_US.csv', 'w', newline= '') as out_file:
        tsv_writer = csv.writer(out_file)
        while x < len(result_file_names) :
            tsv_writer.writerow([result_file_names[x], result_contents[x], control_match_array[x], WER_array[x], MER_array[x], WIL_array[x]])
            x += 1