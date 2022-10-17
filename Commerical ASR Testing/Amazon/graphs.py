import jiwer
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

wer_preprocess = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveWhiteSpace(replace_by_space=True),
    jiwer.RemoveMultipleSpaces(),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
])

count = 0
nzmert = 0
usmert = 0

nzarray = []
usarray = []

for filename in os.listdir('./textonly'):
    count+=1
    basefile = open('./textonly/' + filename)
    base = basefile.read()
    basefile.close()
    usfile = open('./outputUS/' + filename)
    us = usfile.read()
    usfile.close()
    usarray.append(jiwer.mer(base, us))
    nzfile = open('./outputNZ/' + filename.replace('.txt', 'NZ.txt'))
    nz = nzfile.read()
    nzfile.close()
    nzarray.append(jiwer.mer(base, nz))

    nzmert += jiwer.mer(base, nz)
    usmert += jiwer.mer(base, us)

nzmera = nzmert/count
usmera = usmert/count

print(nzmera)
print(usmera)

sns.set(style="whitegrid")

fig = plt.figure(figsize =(10, 7))
ax = fig.add_subplot(111)

data = {'NZ model' : nzarray, 'US model' : usarray}
dataframe = pd.DataFrame.from_dict(data, orient='index')
dataframe = dataframe.transpose()

ax = sns.boxplot(data=dataframe, showfliers = False, width=0.3)
ax = sns.stripplot(data=dataframe, color=".25", jitter=True, s = 3)
plt.title('MER of Amazon transcribe on JL corpus by model')

plt.show()