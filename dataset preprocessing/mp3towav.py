import os
from os import path
from pydub import AudioSegment

for filename in os.listdir("testing/Mozilla_test"):
    destination = os.path.splitext(filename)[0]+".wav"
    sound = AudioSegment.from_mp3("testing/Mozilla_test/" + filename)
    sound.export("MZWav/"+destination, format="wav")