#Author: Louis Chuo
# This code is to use the microsoft azure api for processing the given NZ datasets, configurations as to the models can be changed here

import azure.cognitiveservices.speech as speechsdk
import os
from pyexpat import model
import shutil
from unittest import result
import pandas as pd
import csv

# Code taken from https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=linux%2Cterminal&pivots=programming-language-python
def recognize_from_file(speechAddress):
    speech_config = speechsdk.SpeechConfig(subscription="ec52ecd14b3c4e4d8739ea0191849bf3", region="australiaeast") #server configuaration and credential key input here, change to obtain personal code as this one will not work
    speech_config.speech_recognition_language="en-NZ" # en-NZ for NZ enlgish, en-US for US english

    audio_config = speechsdk.audio.AudioConfig(filename=speechAddress)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return "{}".format(speech_recognition_result.text)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        return ""
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
        return ""


# Code taken from https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/how-to-use-codec-compressed-audio-input-streams?tabs=linux%2Cdebian%2Cjava-android%2Cterminal&pivots=programming-language-python
# Use this one for compressed audio formats like .mp3
def speech_recognize_once_compressed_input(speechAddressmp3):
    """performs one-shot speech recognition with compressed input from an audio file"""
    # <SpeechRecognitionWithCompressedFile>
    class BinaryFileReaderCallback(speechsdk.audio.PullAudioInputStreamCallback):
        def __init__(self, filename: str):
            super().__init__()
            self._file_h = open(filename, "rb")

        def read(self, buffer: memoryview) -> int:
            try:
                size = buffer.nbytes
                frames = self._file_h.read(size)

                buffer[:len(frames)] = frames

                return len(frames)
            except Exception as ex:
                print('Exception in `read`: {}'.format(ex))
                raise

        def close(self) -> None:
            print('closing file')
            try:
                self._file_h.close()
            except Exception as ex:
                print('Exception in `close`: {}'.format(ex))
                raise
    # Creates an audio stream format. For an example we are using MP3 compressed file here
    compressed_format = speechsdk.audio.AudioStreamFormat(compressed_stream_format=speechsdk.AudioStreamContainerFormat.MP3)
    callback = BinaryFileReaderCallback(filename=speechAddressmp3)
    stream = speechsdk.audio.PullAudioInputStream(stream_format=compressed_format, pull_stream_callback=callback)

    speech_config = speechsdk.SpeechConfig(subscription="ec52ecd14b3c4e4d8739ea0191849bf3", region="australiaeast")#server configuaration and credential key input here, change to obtain personal code as this one will not work
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    # Creates a speech recognizer using a file as audio input, also specify the speech language
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()
    result_string = result.text
    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        #print("Recognized:" + result_string)
        return result_string
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
        return ""
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return ""


if __name__ == "__main__":

    name_array = []
    result_array = []
    x = 0

# Loop for processing and saving audio files, change file directories and names to respective datasets to run
    for filename in os.listdir("speech/Mansfield"):
        if filename.endswith(".wav"):
            file_path = "speech/Mansfield/" + filename
            translated_result = recognize_from_file(file_path)
            #translated_result = speech_recognize_once_compressed_input(file_path)
            print(filename)
            print(translated_result)
            name_array.append(filename)
            result_array.append(translated_result)

    with open('speech/Mansfield_output_microsoft_NZ.csv', 'w', newline= '') as out_file:
        tsv_writer = csv.writer(out_file)
        while x < len(name_array) :
            tsv_writer.writerow([name_array[x], result_array[x]])
            x += 1