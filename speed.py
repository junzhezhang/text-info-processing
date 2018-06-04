import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model


truePath ="/Users/junzhezhang/Downloads/text-info-processing/"

### info for AlexNet
fileName1 =truePath+"speed_alex.text" 
fileName2 = truePath+"speed_alex.csv"
title = "Alex in ncrb"

# ### info for resnet
fileName1 =truePath+"speed_resnet.text" 
fileName2 = truePath+"speed_resnet.csv"
title = "resnet in ncrb"

### info for vgg
fileName1 =truePath+"speed_vgg.text" 
fileName2 = truePath+"speed_vgg.csv"
title = "vgg in ncrb"

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

# d, s, t
Out_x =[] 
Out_y =[]
In_x =[]
In_y =[]

for row in rows:
  values = row.split(',')
  if values[0] == "Out":
    Out_x.append(float(values[1]))
    Out_y.append(float(values[2]))
  else:
    In_x.append(float(values[1]))
    In_y.append(float(values[2]))
fig = plt.figure()

### plot
# ax1 = fig.add_subplot(111)
# ax1.set_title(title)    
# ax1.set_xlabel('size in B')
# ax1.set_ylabel('time in ns')
# ax1.plot(Out_x,Out_y, 'bo',c='r', label='the data')
# leg = ax1.legend()
# plt.show()

regr = linear_model.LinearRegression()
In_x_a = np.array(Out_x).reshape(-1,1)
regr.fit(In_x_a, In_y)
# Out_x_a[0,0]=3000
# y_pred = regr.predict(Out_x_a[0,0])
#print y_pred
print regr.coef_
print regr.intercept_

# coef of the 3 models - Out
# [0.07684619]
# 27301.063591829094

# [0.07678375]
# 18875.929790618946

# [0.07567032]
# 47188.75553667371


# coef of the 3 models - In
# [0.08141258]
# 20592.239990252827

# [0.08205873]
# 13572.657949837565

# [0.08230714]
# 9703.084538640105



