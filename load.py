import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model


truePath ="/Users/junzhezhang/Downloads/text-info-processing/"

### info for AlexNet
fileName1 =truePath+"load_0.text" 
fileName2 = truePath+"load_0.csv"

fileName3 =truePath+"load_1.text" 
fileName4 = truePath+"load_1.csv"

def text_2_list(fileName1,fileName2):
  rows_list = []
  f1 = open(fileName1)
  for row in f1:
      rows_list.append(row.split())
  with open(fileName2, 'wb') as f: 
      writer = csv.writer(f)
      writer.writerows(rows_list) 

  ### split_row, list of blockInfo; sort with 
  f2 = open(fileName2)
  rows = f2.read().splitlines()
  rows_float = []
  for row in rows:
    rows_float.append(float(row))

  return rows_float

rows_0 = text_2_list(fileName1,fileName2)
rows_1 = text_2_list(fileName3,fileName4)
rows_x = range(len(rows_0))

# Create plots with pre-defined labels.
fig, ax = plt.subplots()
ax.plot(rows_x, rows_0, 'k--', label='before swap')
ax.plot(rows_x, rows_1, 'k:', label='after swap')

legend = ax.legend(loc='upper right', shadow=True, fontsize='x-small')

# Put a nicer background color on the legend.
legend.get_frame().set_facecolor('#00FFCC')

plt.show()

