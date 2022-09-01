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
utterances1 = glob.glob("./speech/Mozilla/*.mp3", recursive=True)
np.random.shuffle(utterances1)
utterances1 = utterances1[:200]

utterances2 = glob.glob("./speech/US/*.mp3", recursive=True)
np.random.shuffle(utterances2)
utterances2 = utterances2[:200]

verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="./pretrained_ecapa")
#signal, fs = torchaudio.load('./LibriSpeech/dev-clean-2/1272/135031/1272-135031-0003.flac')
#embedding = verification.encode_batch(signal)
#embedding.shape

embeddings1 = []
labels = []
for u in utterances1:
    tmp, fs = torchaudio.load(u)
    e = verification.encode_batch(tmp)
    embeddings1.append(e[0, 0].numpy())
    #spk_label = Path(u).parent.parent.stem
    #labels.append(spk_label)

embeddings1 = np.array(embeddings1)

pca = PCA(n_components=2)
principalComponents1 = pca.fit_transform(embeddings1)

embeddings2 = []
labels = []
for u in utterances2:
    tmp, fs = torchaudio.load(u)
    e = verification.encode_batch(tmp)
    embeddings2.append(e[0, 0].numpy())
    #spk_label = Path(u).parent.parent.stem
    #labels.append(spk_label)

embeddings2 = np.array(embeddings2)

pca = PCA(n_components=2)
principalComponents2 = pca.fit_transform(embeddings2)

#fig, ax = plt.subplots()
#ax.scatter(principalComponents1[:, 0], principalComponents1[:, 1],c='r')
#ax.scatter(principalComponents2[:, 0], principalComponents2[:, 1],c='g')

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(principalComponents1[:, 0], principalComponents1[:, 1],c='r', label='NZ')
ax1.scatter(principalComponents2[:, 0], principalComponents2[:, 1],c='g',label='US')


#for i, spkid in enumerate(labels):
#    ax.annotate(spkid, (principalComponents1[i, 0], principalComponents1[i, 1]))
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(loc='upper left')

plt.show()