import os
from pyexpat import model
import shutil
from unittest import result
import pandas as pd
import csv

def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    translated_speech = ""

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=48000,
        language_code="en-NZ"
        #model="latest_short"
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        #print(os.path.basename(speech_file))
        translated_speech = u"{}".format(result.alternatives[0].transcript)
    
    return translated_speech




if __name__ == "__main__":

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service.json'

    name_array = []
    result_array = []
    x = 0

    #result = transcribe_file("speech/JL/female2_excited_8a_1.wav")
    #print(result)

    for filename in os.listdir("speech/Mansfield"):
        if filename.endswith(".wav"):
            file_path = "speech/Mansfield/" + filename
            translated_result = transcribe_file(file_path)
            print(file_path)
            print(translated_result)
            name_array.append(filename)
            result_array.append(translated_result)

    with open('speech/Mansfield_output_google_NZ.csv', 'w', newline= '') as out_file:
        tsv_writer = csv.writer(out_file)
        while x < len(name_array) :
            tsv_writer.writerow([name_array[x], result_array[x]])
            x += 1


