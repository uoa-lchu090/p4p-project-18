#Author: Louis Chuo
#Loop to call speechbrain multiple times for multiple itterations

import subprocess
import sys

script_name = 'speechbrain_finetune.py'

for i in range(1, 31):
    print ("Itteration: " + str(i))
    subprocess.call(['python3', script_name])