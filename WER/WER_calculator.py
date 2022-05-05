
from openpyxl import load_workbook
import jiwer
import sys
import os

wb = load_workbook(filename='mansfield_excel.xlsx')
default_sheet = wb['metadataNZ']

filename = os.path.splitext(str(sys.argv[1]))
f = open(filename[0], 'r')

hypothesis = f.readline().strip()

field_names = default_sheet['A']
ground_truths = default_sheet['B']

for i in range(1, 2694):
    if (field_names[i].value == filename[0]):
        wer = jiwer.wer(ground_truths[i].value, hypothesis)
        print(ground_truths[i].value)
        print(hypothesis)
        print (wer)

