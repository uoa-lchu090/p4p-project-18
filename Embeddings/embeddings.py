from speechbrain.pretrained import SpeakerRecognition
import torchaudio
from pathlib import Path
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import glob 
import numpy as np


utterances1 = glob.glob("./speech/Mozilla/*.mp3", recursive=True)
np.random.shuffle(utterances1)
utterances1 = utterances1[:200]

utterances2 = glob.glob("./speech/US/*.mp3", recursive=True)
np.random.shuffle(utterances2)
utterances2 = utterances2[:200]

verification = SpeakerRecognition.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")

embeddings1 = []
labels = []
for u in utterances1:
    tmp, fs = torchaudio.load(u)
    e = verification.encode_batch(tmp)
    embeddings1.append(e[0, 0].numpy())

embeddings1 = np.array(embeddings1)

pca = PCA(n_components=2)
principalComponents1 = pca.fit_transform(embeddings1)

embeddings2 = []
labels = []
for u in utterances2:
    tmp, fs = torchaudio.load(u)
    e = verification.encode_batch(tmp)
    embeddings2.append(e[0, 0].numpy())

embeddings2 = np.array(embeddings2)

pca = PCA(n_components=2)
principalComponents2 = pca.fit_transform(embeddings2)


fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(principalComponents1[:, 0], principalComponents1[:, 1],c='r', label='NZ')
ax1.scatter(principalComponents2[:, 0], principalComponents2[:, 1],c='g',label='US')


plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(loc='upper left')

plt.show()