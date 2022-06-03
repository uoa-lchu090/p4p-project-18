import shutil

import pandas as pd
path = ".\WER\mansfield_excel.xlsx"
df = pd.read_excel(path)


def sort(input_folder, output_folder):

    for i in range(len(df)):
        file=df.get("Column1").tolist()[0]
        shutil.copy(input_folder+"//"+file, output_folder+"//"+file)


sort(".//clips", ".//clips2")