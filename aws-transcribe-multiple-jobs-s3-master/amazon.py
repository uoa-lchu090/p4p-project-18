import os
import time
import boto3
import pandas as pd
from botocore.config import Config
import json
import datetime
import glob

def read_output(filename):
    # example filename: audio.json

    # take the input as the filename

    filename = (filename).split('.')[0]

    # Create an outputUS txt file
    print(filename + '.txt')
    with open(filename + '.txt', 'w') as w:
        with open(filename + '.json') as f:

            data = json.loads(f.read())
            labels = data['results']['speaker_labels']['segments']
            speaker_start_times = {}

            for label in labels:
                for item in label['items']:
                    speaker_start_times[item['start_time']] = item['speaker_label']

            items = data['results']['items']
            lines = []
            line = ''
            time = 0
            speaker = 'null'
            i = 0

            # loop through all elements
            for item in items:
                i = i + 1
                content = item['alternatives'][0]['content']

                # if it's starting time
                if item.get('start_time'):
                    current_speaker = speaker_start_times[item['start_time']]

                # in AWS outputUS, there are types as punctuation
                elif item['type'] == 'punctuation':
                    line = line + content

                # handle different speaker
                if current_speaker != speaker:
                    if speaker:
                        lines.append({'speaker': speaker, 'line': line, 'time': time})
                    line = content
                    speaker = current_speaker
                    time = item['start_time']

                elif item['type'] != 'punctuation':
                    line = line + ' ' + content
            lines.append({'speaker': speaker, 'line': line, 'time': time})

            # sort the results by the time
            sorted_lines = sorted(lines, key=lambda k: float(k['time']))

            # write into the .txt file
            for line_data in sorted_lines:
                line = '[' + str(
                    datetime.timedelta(seconds=int(round(float(line_data['time']))))) + '] ' + line_data.get(
                    'speaker') + ': ' + line_data.get('line')
                w.write(line + '\n\n')

def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='wav',
        LanguageCode='en-NZ'
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                 print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
                 data = pd.read_json(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                 text = data['results'][1][0]['transcript']
                 file = open('outputNZ/' + job_name + '.txt', 'w')
                 file.write(text)
                 file.close
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)


def main():

    my_config = Config(
        region_name='ap-southeast-2',
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    transcribe_client = boto3.client('transcribe',
                                     config=my_config,
                                     aws_access_key_id='',
    aws_secret_access_key=''
                                     )
    for name in os.listdir("./wavonly"):
        filename = name[:-4]
        file_uri = 's3://22p4p18/wavonly/' + filename + '.wav'
        transcribe_file(filename+'NZ', file_uri, transcribe_client)



if __name__ == '__main__':
    main()