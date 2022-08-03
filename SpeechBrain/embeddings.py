from speechbrain.pretrained import SpeakerRecognition
import torchaudio
from pathlib import Path
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import glob 
import numpy as np

#utterances = glob.glob("./LibriSpeech/dev-clean-2/**/*.flac", recursive=True)
#utterances = glob.glob("./speech/JL/*.wav", recursive=True)
#utterances = glob.glob("./speech/Mansfield/*.wav", recursive=True)
utterances = glob.glob("./speech/Mozilla/*.mp3", recursive=True)
np.random.shuffle(utterances)
utterances = utterances[:50]

verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="./pretrained_ecapa")
#signal, fs = torchaudio.load('./LibriSpeech/dev-clean-2/1272/135031/1272-135031-0003.flac')
#embedding = verification.encode_batch(signal)
#embedding.shape

embeddings = []
labels = []
for u in utterances:
    tmp, fs = torchaudio.load(u)
    e = verification.encode_batch(tmp)
    embeddings.append(e[0, 0].numpy())
    #spk_label = Path(u).parent.parent.stem
    #labels.append(spk_label)

embeddings = np.array(embeddings)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(embeddings)

fig, ax = plt.subplots()
ax.scatter(principalComponents[:, 0], principalComponents[:, 1])

for i, spkid in enumerate(labels):
    ax.annotate(spkid, (principalComponents[i, 0], principalComponents[i, 1]))
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

plt.show()