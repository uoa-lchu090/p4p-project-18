import os
from pydub import AudioSegment

# files                                                                         
src = "speech/common_voice_en_31901.mp3"
dst = "speech/common_voice_en_31901.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

