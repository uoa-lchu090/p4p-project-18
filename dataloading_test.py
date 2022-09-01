from email.mime import audio
import speechbrain
import torch
import matplotlib.pyplot as plt

from speechbrain.dataio.dataset import DynamicItemDataset

dataset = DynamicItemDataset.from_csv("combined_test_data.csv")

dataset.add_dynamic_item(speechbrain.dataio.dataio.read_audio, takes="file_path", provides="signal")
dataset.set_output_keys(["id", "signal", "words"])

print(dataset[38])

plt.figure(1)
plt.title("Sig item")
plt.plot(dataset[38]["signal"])
plt.show()