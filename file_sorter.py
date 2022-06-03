import shutil

import pandas as pd
path = ".\WER\mansfield_excel.xlsx"
df = pd.read_excel(path)


def sort(input_folder, output_folder):
    notfound = 0

    for i in range(len(df)):
        file=df.get("Column1").tolist()[0]
        try:
            shutil.copy(input_folder+"//"+file, output_folder+"//"+file)
        except FileNotFoundError:
            notfound+=1

    return notfound

print(sort(".//clips", ".//clips2"))