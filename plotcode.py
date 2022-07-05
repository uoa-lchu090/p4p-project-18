import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Toggles for different plots
model_compare_toggle = True #toggles if the plot comparing model performance on different datasets is calculated
model_to_compare = "Microsoft_US" # Google_US, Google_NZ, Microsoft_US

dataset_compare_toggle = False #toggles if the plot comparing dataset performance on different models is calculated
dataset_to_compare = "Mozilla" # JL, Mansfield, Mozilla 

measuring_mode = "MER" # WER, MER, WIL



data_path = "./speech/Measurement Results/measurement_combined.xlsx"


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




#Loading in all Mozilla data
result_df = pd.read_excel(data_path, sheet_name= "Mozilla_measures_google_NZ")
Mozilla_google_NZ_WER = result_df.get("WER").tolist()
Mozilla_google_NZ_MER = result_df.get("MER").tolist()
Mozilla_google_NZ_WIL = result_df.get("WIL").tolist()

result_df = pd.read_excel(data_path, sheet_name= "Mozilla_measures_google_US")
Mozilla_google_US_WER = result_df.get("WER").tolist()
Mozilla_google_US_MER = result_df.get("MER").tolist()
Mozilla_google_US_WIL = result_df.get("WIL").tolist()

Mozilla_microsoft_US_WER = []
Mozilla_microsoft_US_MER = []
Mozilla_microsoft_US_WIL = []

result_df = pd.read_excel(data_path, sheet_name= "Mozilla_measures_microsoft_US")
Mozilla_microsoft_US_WER_temp = result_df.get("WER").tolist()
Mozilla_microsoft_US_MER_temp = result_df.get("MER").tolist()
Mozilla_microsoft_US_WIL_temp = result_df.get("WIL").tolist()

for x in Mozilla_microsoft_US_WER_temp:
    if x < 2:
        Mozilla_microsoft_US_WER.append(x)

for x in Mozilla_microsoft_US_MER_temp:
    if x < 2:
        Mozilla_microsoft_US_MER.append(x)

for x in Mozilla_microsoft_US_WIL_temp:
    if x < 2:
        Mozilla_microsoft_US_WIL.append(x)





fig, ax1 = plt.subplots()



# big if statements for different modes

if dataset_compare_toggle == True and measuring_mode == "WER":
    if dataset_to_compare == "JL":
        graph_data = [JL_google_NZ_WER, JL_google_US_WER, JL_microsoft_US_WER]
        ax1.set_title('Commerical ASR Performance on the JL Corpus (WER)')
        labels = ('Google NZ: ' + str(len(JL_google_NZ_WER)), 'Google US: ' + str(len(JL_google_US_WER)), 'Microsoft US: ' + str(len(JL_microsoft_US_WER)))
    elif dataset_to_compare == "Mansfield":
        graph_data = [Mansfield_google_NZ_WER, Mansfield_google_US_WER, Mansfield_microsoft_US_WER]
        ax1.set_title('Commerical ASR Performance on the Mansfield Corpus (WER)')
        labels = ('Google NZ: ' + str(len(Mansfield_google_NZ_WER)), 'Google US: ' + str(len(Mansfield_google_US_WER)), 'Microsoft US: ' + str(len(Mansfield_microsoft_US_WER)))
    else:
        graph_data = [Mozilla_google_NZ_WER, Mozilla_google_US_WER, Mozilla_microsoft_US_WER]
        ax1.set_title('Commerical ASR Performance on the Mozilla Corpus (WER)')
        labels = ('Google NZ: ' + str(len(Mozilla_google_NZ_WER)), 'Google US: ' + str(len(Mozilla_google_US_WER)), 'Microsoft US: ' + str(len(Mozilla_microsoft_US_WER)))

        

if dataset_compare_toggle == True and measuring_mode == "MER":
    if dataset_to_compare == "JL":
        graph_data = [JL_google_NZ_MER, JL_google_US_MER, JL_microsoft_US_MER]
        ax1.set_title('Commerical ASR Performance on the JL Corpus (MER)')
        labels = ('Google NZ: ' + str(len(JL_google_NZ_MER)), 'Google US: ' + str(len(JL_google_US_MER)), 'Microsoft US: ' + str(len(JL_microsoft_US_MER)))
    elif dataset_to_compare == "Mansfield":
        graph_data = [Mansfield_google_NZ_MER, Mansfield_google_US_MER, Mansfield_microsoft_US_MER]
        ax1.set_title('Commerical ASR Performance on the Mansfield Corpus (MER)')
        labels = ('Google NZ: ' + str(len(Mansfield_google_NZ_MER)), 'Google US: ' + str(len(Mansfield_google_US_MER)), 'Microsoft US: ' + str(len(Mansfield_microsoft_US_MER)))
    else:
        graph_data = [Mozilla_google_NZ_MER, Mozilla_google_US_MER, Mozilla_microsoft_US_MER]
        ax1.set_title('Commerical ASR Performance on the Mozilla Corpus (MER)')
        labels = ('Google NZ: ' + str(len(Mozilla_google_NZ_MER)), 'Google US: ' + str(len(Mozilla_google_US_MER)), 'Microsoft US: ' + str(len(Mozilla_microsoft_US_MER)))



if dataset_compare_toggle == True and measuring_mode == "WIL":
    if dataset_to_compare == "JL":
        graph_data = [JL_google_NZ_WIL, JL_google_US_WIL, JL_microsoft_US_WIL]
        ax1.set_title('Commerical ASR Performance on the JL Corpus (WIL)')
        labels = ('Google NZ: ' + str(len(JL_google_NZ_WIL)), 'Google US: ' + str(len(JL_google_US_WIL)), 'Microsoft US: ' + str(len(JL_microsoft_US_WIL)))
    elif dataset_to_compare == "Mansfield":
        graph_data = [Mansfield_google_NZ_WIL, Mansfield_google_US_WIL, Mansfield_microsoft_US_WIL]
        ax1.set_title('Commerical ASR Performance on the Mansfield Corpus (WIL)')
        labels = ('Google NZ: ' + str(len(Mansfield_google_NZ_WIL)), 'Google US: ' + str(len(Mansfield_google_US_WIL)), 'Microsoft US: ' + str(len(Mansfield_microsoft_US_WIL)))
    else:
        graph_data = [Mozilla_google_NZ_WIL, Mozilla_google_US_WIL, Mozilla_microsoft_US_WIL]
        ax1.set_title('Commerical ASR Performance on the Mozilla Corpus (WIL)')
        labels = ('Google NZ: ' + str(len(Mozilla_google_NZ_WIL)), 'Google US: ' + str(len(Mozilla_google_US_WIL)), 'Microsoft US: ' + str(len(Mozilla_microsoft_US_WIL)))







if model_compare_toggle == True and measuring_mode == "WER":
    if model_to_compare == "Google_US":
        graph_data = [JL_google_US_WER, Mansfield_google_US_WER, Mozilla_google_US_WER]
        ax1.set_title('Google US Model performance on varied datasets (WER)')
        labels = ('JL: '+ str(len(JL_google_US_WER)), 'Mansfield: ' + str(len(Mansfield_google_US_WER)), 'Mozilla: ' + str(len(Mozilla_google_US_WER)))
    elif model_to_compare == "Google_NZ":
        graph_data = [JL_google_NZ_WER, Mansfield_google_NZ_WER, Mozilla_google_NZ_WER]
        ax1.set_title('Google NZ Model performance on varied datasets (WER)')
        labels = ('JL: '+ str(len(JL_google_NZ_WER)), 'Mansfield: ' + str(len(Mansfield_google_NZ_WER)), 'Mozilla: ' + str(len(Mozilla_google_NZ_WER)))
    else:
        graph_data = [JL_microsoft_US_WER, Mansfield_microsoft_US_WER, Mozilla_microsoft_US_WER]
        ax1.set_title('Microsoft US Model performance on varied datasets (WER)')
        labels = ('JL: ' + str(len(JL_microsoft_US_WER)), 'Mansfield: ' + str(len(Mansfield_microsoft_US_WER)), 'Mozilla: ' + str(len(Mozilla_microsoft_US_WER)))

        


if model_compare_toggle == True and measuring_mode == "WIL":
    if model_to_compare == "Google_US":
        graph_data = [JL_google_US_WIL, Mansfield_google_US_WIL, Mozilla_google_US_WIL]
        ax1.set_title('Google US Model performance on varied datasets (WIL)')
        labels = ('JL: '+ str(len(JL_google_US_WIL)), 'Mansfield: ' + str(len(Mansfield_google_US_WIL)), 'Mozilla: ' + str(len(Mozilla_google_US_WIL)))
    elif model_to_compare == "Google_NZ":
        graph_data = [JL_google_NZ_WIL, Mansfield_google_NZ_WIL, Mozilla_google_NZ_WIL]
        ax1.set_title('Google NZ Model performance on varied datasets (WIL)')
        labels = ('JL: '+ str(len(JL_google_NZ_WIL)), 'Mansfield: ' + str(len(Mansfield_google_NZ_WIL)), 'Mozilla: ' + str(len(Mozilla_google_NZ_WIL)))
    else:
        graph_data = [JL_microsoft_US_WIL, Mansfield_microsoft_US_WIL, Mozilla_microsoft_US_WIL]
        ax1.set_title('Microsoft US Model performance on varied datasets (WIL)')
        labels = ('JL: ' + str(len(JL_microsoft_US_WIL)), 'Mansfield: ' + str(len(Mansfield_microsoft_US_WIL)), 'Mozilla: ' + str(len(Mozilla_microsoft_US_WIL)))





if model_compare_toggle == True and measuring_mode == "MER":
    if model_to_compare == "Google_US":
        graph_data = [JL_google_US_MER, Mansfield_google_US_MER, Mozilla_google_US_MER]
        ax1.set_title('Google US Model performance on varied datasets (MER)')
        labels = ('JL: '+ str(len(JL_google_US_MER)), 'Mansfield: ' + str(len(Mansfield_google_US_MER)), 'Mozilla: ' + str(len(Mozilla_google_US_MER)))
    elif model_to_compare == "Google_NZ":
        graph_data = [JL_google_NZ_MER, Mansfield_google_NZ_MER, Mozilla_google_NZ_MER]
        ax1.set_title('Google NZ Model performance on varied datasets (MER)')
        labels = ('JL: '+ str(len(JL_google_NZ_MER)), 'Mansfield: ' + str(len(Mansfield_google_NZ_MER)), 'Mozilla: ' + str(len(Mozilla_google_NZ_MER)))
    else:
        graph_data = [JL_microsoft_US_MER, Mansfield_microsoft_US_MER, Mozilla_microsoft_US_MER]
        ax1.set_title('Microsoft US Model performance on varied datasets (MER)')
        labels = ('JL: ' + str(len(JL_microsoft_US_MER)), 'Mansfield: ' + str(len(Mansfield_microsoft_US_MER)), 'Mozilla: ' + str(len(Mozilla_microsoft_US_MER)))








if model_compare_toggle or dataset_compare_toggle:
    ax1.boxplot(graph_data, showfliers=False)
    plt.xticks(np.arange(len(labels))+1,labels)
    if dataset_compare_toggle:
        plt.savefig('speech/boxplots/' + dataset_to_compare + "_" + measuring_mode + ".png")
    elif model_compare_toggle:
        plt.savefig('speech/boxplots/' + model_to_compare + "_" + measuring_mode + ".png")


    plt.show()
    