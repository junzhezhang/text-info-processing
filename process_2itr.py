import csv

truePath ="/Users/junzhezhang/Downloads/text-info-processing/"

### info for AlexNet
fileName1 =truePath+"vec_run_alex_31.text" 
fileName2 = truePath+"vec_run_alex_31.csv"
fileName3 =truePath+"vec_run_alex_31_2.text" 
fileName4 = truePath+"vec_run_alex_31_2.csv"
maxLen = 612
location = 1247
maxIdx = 247

### info for resnet
# fileName1 =truePath+"vec_run_resnet.text" 
# fileName2 = truePath+"vec_run_resnet.csv"
# maxLen = 4144
# location = 8737
# maxIdx = 1059

### info for vgg
# fileName1 =truePath+"vec_run_vgg.text" 
# fileName2 = truePath+"vec_run_vgg.csv"
# maxLen = 3172
# location = 6675
# maxIdx = 1369


blocks = set([]) 

### convert from vec_run.text (one iteration) into vec_run.csv
# it deletes the existing contents if any.
rows_list = []
rows_list.append(['index','flag','block_','size', 'timeStamp'])
f1 = open(fileName1)
for row in f1:
    rows_list.append(row.split())

with open(fileName2, 'wb') as f: 
    writer = csv.writer(f)
    writer.writerows(rows_list) 

rows_list = []
rows_list.append(['index','flag','block_','size', 'timeStamp'])
f1 = open(fileName3)
for row in f1:
    rows_list.append(row.split())

with open(fileName4, 'wb') as f: 
    writer = csv.writer(f)
    writer.writerows(rows_list) 

### split_row, list of blockInfo; sort with 
f2 = open(fileName2)
rows = f2.read().splitlines()
split_rows = []
i = 0
for row in rows:
  if i>0:
    values = row.split(',')
    split_rows.append(values)
  i = i+1
# print len(split_rows)
# print split_rows[0]
f4 = open(fileName4)
rows2 = f4.read().splitlines()
split_rows2 = []
i = 0
for row in rows2:
  if i>0:
    values = row.split(',')
    split_rows2.append(values)
  i = i+1
print "================================="

split_rows.sort(key = lambda x: x[2]) # sort in place.

### verify if increasing idx for each block TODO(junzhe) omitted
# i = 0 
# for row in split_rows:
#   print row
#   i = i+1
#   if i>30:
#     break

### group in to distinct blocks, verified with blow prints
for row in split_rows:
  blocks.add(row[2])
print len(blocks)

tempBlock = ''
distinct_blocks = []
current_block = []
for row in split_rows:
  if tempBlock == row[2] and row[1] != 'Malloc':
    current_block.append(row)
  else:
    #print '-------------- cut '+str(tempBlock == row[2])
    i =i + 1
    if len(current_block) > 0:
      distinct_blocks.append(current_block)
      current_block =[]
      current_block.append(row)
    tempBlock = row[2]
  #print row
print len(distinct_blocks)



# categorize conditions of the distinct blocks && size to change
cat_A = []
cat_A_size = 0
for block in distinct_blocks:
  if (int(block[0][0]) <= maxIdx) and (int(block[-1][0]) >= maxIdx):
    cat_A_size = cat_A_size + int(block[0][3])
    cat_A.append(block)
    ##distinct_blocks.remove(block) #NOTE this will make it wrong
print "cat_A blocks: "+str(len(cat_A))+" size in MB: "+str(float(cat_A_size)/1024/1024)
for block in cat_A:
  distinct_blocks.remove(block)
print "after cat_A: "+str(len(distinct_blocks))+' '+str(len(cat_A))

# actually this no need to split, as this can be filtered in one shot
cat_A1 = [] # layer to R/W
cat_A1_size = 0 
cat_A2 = [] # read to R/W
cat_A2_size = 0

cat_B = [] # no free
cat_B_size = 0
global_flag =set([])


for block in distinct_blocks:
  flags =[]
  for row in block:
    flags.append(row[1])
    global_flag.add(row[1])
  if "Free" not in flags:
    cat_B.append(block)
    cat_B_size = cat_B_size + int(block[0][3])
print "cat_B blocks: "+str(len(cat_B))+" size in MB: "+str(float(cat_B_size)/1024/1024)
for block in cat_B:
  distinct_blocks.remove(block)
print "after cat_B: "+str(len(distinct_blocks))

for block in cat_B:
  print '==================='
  if int(block[0][0]) > maxIdx:
    for row in block:
      print row
    print "------------"
    for row in split_rows2:
      if row[2] == block[0][2]:
        print row

# for block in distinct_blocks:
#   print '==================='
#   for row in block:
#     print row
### to compute other than cat A and B, how much it occupies:
load = [0] * maxLen

for block in distinct_blocks:
  # must last "free" and the only free
  for i in range (int(block[0][0]), int(block[-1][0])+1):
    load[i]+=int(block[0][3])
print "after A and B maxLoad: "+str(max(load)/1024/1024)

# print len(cat_A)
# last_row = ['0']
# for block in cat_A:
#   print '==================='
#   for row in block:
#     if int(last_row[0]) < maxIdx and int(row[0]) > maxIdx:
#       if last_row[1] == "Read":
#         print last_row
#         print row
#     last_row = row

# # for block in cat_B:
#   print '==================='

