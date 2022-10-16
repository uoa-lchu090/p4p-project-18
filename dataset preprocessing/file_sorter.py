# Author: Louis Chuo, Henry An
# Description:  This code reads data from an excel file and moves the present filenames into another specified folder

import shutil
import pandas as pd
path = "./train_filtered_NZ.xlsx"
df = pd.read_excel(path, sheet_name="path") 


def sort(input_folder, output_folder):
    notfound = 0

    for i in range(len(df)):
        file=df.get("file").tolist()[i]
        print(i)
        try:
            shutil.copy(input_folder+"//"+file, output_folder+"//"+file)
        except FileNotFoundError:
            notfound+=1

    return notfound


if __name__ == '__main__':
    notfound = sort("./en", "./NZ")
    print("done")
    print(notfound)#print no. of files present in list but not in folder