import subprocess
import sys

script_name = 'speechbrain_fine_tune_ex_CUDA.py'

for i in range(1, 31):
    print ("Itteration: " + str(i))
    subprocess.call(['python3', script_name])