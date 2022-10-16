# Author: Louis Chuo
# Code for importing and plotting all the commercial results in a box plot

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


data_path = "./speech/measurement_combined.xlsx"


#Loading in all JL data
result_df = pd.read_excel(data_path, sheet_name= "JL_measures_google_NZ")
JL_google_NZ_WER = result_df.get("WER").tolist()
JL_google_NZ_MER = result_df.get("MER").tolist()
JL_google_NZ_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "JL_measures_google_US")
JL_google_US_WER = result_df.get("WER").tolist()
JL_google_US_MER = result_df.get("MER").tolist()
JL_google_US_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "JL_measures_microsoft_US")
JL_microsoft_US_WER = result_df.get("WER").tolist()
JL_microsoft_US_MER = result_df.get("MER").tolist()
JL_microsoft_US_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "JL_measures_microsoft_NZ")
JL_microsoft_NZ_WER = result_df.get("WER").tolist()
JL_microsoft_NZ_MER = result_df.get("MER").tolist()
JL_microsoft_NZ_WIL = result_df.get("WIL").tolist()



#Loading in all Mansfield data
result_df = pd.read_excel(data_path, sheet_name= "Mansfield_measures_google_NZ")
Mansfield_google_NZ_WER = result_df.get("WER").tolist()
Mansfield_google_NZ_MER = result_df.get("MER").tolist()
Mansfield_google_NZ_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "Mansfield_measures_google_US")
Mansfield_google_US_WER = result_df.get("WER").tolist()
Mansfield_google_US_MER = result_df.get("MER").tolist()
Mansfield_google_US_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "Mansfield_measures_microsoft_US")
Mansfield_microsoft_US_WER = result_df.get("WER").tolist()
Mansfield_microsoft_US_MER = result_df.get("MER").tolist()
Mansfield_microsoft_US_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "Mansfield_measures_microsoft_NZ")
Mansfield_microsoft_NZ_WER = result_df.get("WER").tolist()
Mansfield_microsoft_NZ_MER = result_df.get("MER").tolist()
Mansfield_microsoft_NZ_WIL = result_df.get("WIL").tolist()




#Loading in all Mozilla data
result_df = pd.read_excel(data_path, sheet_name= "Mozilla_measures_google_NZ")
Mozilla_google_NZ_WER = result_df.get("WER").tolist()
Mozilla_google_NZ_MER = result_df.get("MER").tolist()
Mozilla_google_NZ_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "Mozilla_measures_google_US")
Mozilla_google_US_WER = result_df.get("WER").tolist()
Mozilla_google_US_MER = result_df.get("MER").tolist()
Mozilla_google_US_WIL = result_df.get("WIL").tolist()


result_df = pd.read_excel(data_path, sheet_name= "Mozilla_measures_microsoft_US")
Mozilla_microsoft_US_WER = result_df.get("WER").tolist()
Mozilla_microsoft_US_MER = result_df.get("MER").tolist()
Mozilla_microsoft_US_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "Mozilla_measures_microsoft_NZ")
Mozilla_microsoft_NZ_WER = result_df.get("WER").tolist()
Mozilla_microsoft_NZ_MER = result_df.get("MER").tolist()
Mozilla_microsoft_NZ_WIL = result_df.get("WIL").tolist()




sns.set(style="whitegrid")
data = {"JL": JL_google_NZ_MER, "Mansfield": Mansfield_google_NZ_MER, "Mozilla": Mozilla_google_NZ_MER}

dataframe = pd.DataFrame.from_dict(data, orient='index')
dataframe = dataframe.transpose()

ax = sns.boxplot(data=dataframe, showfliers = False, width=0.3)
ax = sns.stripplot(data=dataframe, color=".25", jitter=True, s = 3)

plt.title("MER of corpuses on goole ASR NZ model")

plt.show()