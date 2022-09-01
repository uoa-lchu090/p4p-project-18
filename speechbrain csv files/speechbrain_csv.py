import shutil
import csv
import os

import pandas as pd
path = "./testing.xlsx"
df = pd.read_excel(path, sheet_name="MANtesting")
f = open('combined_test_data.csv', 'w')
writer = csv.writer(f)
writer.writerow(["id", "file_path", "words"])
total_id = 0

for i in range(len(df)):
    #filename=os.path.splitext(df.get("Column1").tolist()[i])[0]
    filename=df.get("Column1").tolist()[i]
    text=df.get("Column2").tolist()[i]

    print(str(total_id) + ", ./training/Mansfield_test/" + filename + ".wav, " + text)
    data = [total_id, "./training/Mansfield_test/" + filename + ".wav", text]

    total_id = total_id + 1
    writer.writerow(data)

df = pd.read_excel(path, sheet_name="JLtesting")

for i in range(len(df)):
    filename=os.path.splitext(df.get("Column1").tolist()[i])[0]
    #filename=df.get("Column1").tolist()[i]
    text=df.get("Column2").tolist()[i]

    print(str(total_id) + ", ./training/JL_test/" + filename +".wav, " + text)
    data = [total_id, "./training/JL_test/" + filename + ".wav", text]
    total_id = total_id + 1
    writer.writerow(data)


df = pd.read_excel(path, sheet_name="MZtesting")

for i in range(len(df)):
    #filename=os.path.splitext(df.get("Column1").tolist()[i])[0]
    filename=df.get("Column1").tolist()[i]
    text=df.get("_1").tolist()[i]

    print(str(total_id) + ", ./training/Mozilla_test/" + filename +", " + text)
    data = [total_id, "./training/Mozilla_test/" + filename , text]

    total_id = total_id + 1
    writer.writerow(data)

f.close()
    