import shutil

import pandas as pd
path = "./similar_word.xlsx"
df = pd.read_excel(path, sheet_name="NZoutput")


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
    notfound = sort("./NZ", "./NZsimilar")
    print("done")
    print(notfound)
    #print(sort(".//clips", ".//clips2"))