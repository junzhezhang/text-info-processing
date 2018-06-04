import csv

truePath ="/Users/junzhezhang/Downloads/text-info-processing/"

smallest_block = 1<<20

### info for AlexNet
fileName1 =truePath+"vec_run_alex.text" 
fileName2 = truePath+"vec_run_alex.csv"
fileName3 =truePath+"vec_run_alex_2.text" 
fileName4 = truePath+"vec_run_alex_2.csv"
maxLen = 612
location = 1247
maxIdx = 247

# ### info for resnet
# fileName1 =truePath+"vec_run_resnet.text" 
# fileName2 = truePath+"vec_run_resnet.csv"
# fileName3 =truePath+"vec_run_resnet_2.text" 
# fileName4 = truePath+"vec_run_resnet_2.csv"
# maxLen = 4144
# location = 8737
# maxIdx = 1059

# ### info for vgg
# fileName1 =truePath+"vec_run_vgg.text" 
# fileName2 = truePath+"vec_run_vgg.csv"
# fileName3 =truePath+"vec_run_vgg_2.text" 
# fileName4 = truePath+"vec_run_vgg_2.csv"
# maxLen = 3172
# location = 6675
# maxIdx = 1369

blocks = set([]) 

def text_2_csv(fileName1, fileName2,smallest_block):
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

  ### split_row, list of blockInfo; sort with 
  f2 = open(fileName2)
  rows = f2.read().splitlines()
  split_rows = []
  i = 0
  for row in rows:
    if i>0:
      values = row.split(',')
      if int(values[3]) >= smallest_block:
        split_rows.append(values[0:-1]) # exclude last item, t
    i = i+1
  print "================================="
  return split_rows
split_rows = text_2_csv(fileName1,fileName2,smallest_block)

split_rows_2 = text_2_csv(fileName3,fileName4,smallest_block)

split_rows.sort(key = lambda x: x[2]) # sort in place.

### group in to distinct blocks, verified with blow prints
for row in split_rows:
  blocks.add(row[2])
print "no of block names: "+str(len(blocks))

# create blocks - new, should be no problem
tempBlock = ''
distinct_blocks = []
current_block = []
count = 0
print "no of rows in total: "+str(len(split_rows))
for row in split_rows:
  if tempBlock == '':
    current_block.append(row)
    count+=1
    tempBlock = row[2]
  else:
    if tempBlock == row[2]:
      if row[1] != 'Malloc':
        current_block.append(row)
        count+=1
      else:
        distinct_blocks.append(current_block)        
        current_block =[]
        current_block.append(row)
        count+=1
    else:
      distinct_blocks.append(current_block)
      current_block =[]      
      current_block.append(row)      
      count+=1
      tempBlock = row[2]
    if count == maxLen:
      distinct_blocks.append(current_block)
print "no of distinct blocks: "+str(len(distinct_blocks))
sum_rows = 0
for block in distinct_blocks:
  sum_rows+=len(block)
print "no of rows of all distinct blocks: "+str(sum_rows)

## verify share block name
# print count
# lastBlock = ''
# count = 0
# for block in distinct_blocks:
#   if lastBlock == block[0][2]:
#     print "block share name"
#   lastBlock = block[0][2]
#   print "======================="+block[0][2]
#   for row in block:
#     print row
#     count+=1
# print "total row: "+str(count)

### categorization cat_A
cat_A = [] # cross peak
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

# sub cat of A, other than A1~A3, can be 1~a few malloc during peak, ignore.
cat_A1 = [] # layer to R/W
cat_A1_size = 0 
cat_A2 = [] # read to R/W
cat_A2_size = 0
cat_A3 = [] # w to R/W
cat_A3_size = 0
cat_A4 = [] # during peak
cat_A4_size = 0
for block in cat_A:
  last_row = block[0]
  for row in block:
    if (row != last_row) and int(last_row[0]) < maxIdx and int(row[0]) > maxIdx:
      if last_row[1] == "Layer":
        cat_A1.append(block)
        cat_A1_size+=int(block[0][3])
      if last_row[1] == "Read":
        cat_A2.append(block)
        cat_A2_size+=int(block[0][3])
      if last_row[1] == "Mutable":
        cat_A3.append(block)
        cat_A3_size+=int(block[0][3])
    last_row = row
for block in cat_A:
  if (block not in cat_A1) and (block not in cat_A2) and (block not in cat_A3):
    cat_A4.append(block)
    cat_A4_size+=int(block[0][3])

print "------below A sub cat and size:"
print len(cat_A1), float(cat_A1_size)/1024/1024
print len(cat_A2), float(cat_A2_size)/1024/1024
print len(cat_A3), float(cat_A3_size)/1024/1024
print len(cat_A4), float(cat_A4_size)/1024/1024
print "------ END of Cat A -----------"

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

# for block in cat_B:
#   print '==================='
#   if int(block[0][0]) < maxIdx:
#     for row in block:
#       print row

# for block in distinct_blocks:
#   print '==================='
#   for row in block:
#     print row
### to compute other than cat A and B, how much it occupies:

# sub cat of B
cat_B1 = [] # exactly the same
cat_B1_size = 0 
cat_B2 = [] # malloc this iteration and free at next.
cat_B2_size = 0
cat_B3 = [] # 
cat_B3_size = 0
cat_B4 = [] # 
cat_B4_size = 0

for block in cat_B:
  block2 = []
  for row in split_rows_2:
    if row[2] == block[0][2]:
      block2.append(row)
  block.sort(key = lambda x: x[0]) # sort in place.
  block2.sort(key = lambda x: x[0]) # sort in place.
  if block2 == block: # sorted
    cat_B1.append(block)
    cat_B1_size+=int(block[0][3])
print "cat_B1 blocks: "+str(len(cat_B1))+" size in MB: "+str(float(cat_B1_size)/1024/1024)

for block in cat_B:
  if block[0][1] == "Malloc":
    cat_B2.append(block)
    cat_B2_size+=int(block[0][3])
print "cat_B2 blocks: "+str(len(cat_B2))+" size in MB: "+str(float(cat_B2_size)/1024/1024)

# for block in cat_B:
#   if block not in cat_B1:
#     print '==================='
#   #if int(block[0][0]) > maxIdx:
#     for row in block:
#      print row
#     print "------------"
#     for row in split_rows_2:
#       if row[2] == block[0][2]:
#         if row[1] == "Malloc":
#           break
#         print row

print "------ END of Cat B -----------"
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

# for block in cat_A1:
#   print "---------------"
#   last_row = block[0]
#   for row in block:
#     if (row != last_row) and int(last_row[0]) < maxIdx and int(row[0]) > maxIdx:
#       print last_row
#       print row
#       last_row = row

# for block in cat_A2:
#   print "---------------"
#   last_row = block[0]
#   for row in block:
#     if (row != last_row) and int(last_row[0]) < maxIdx and int(row[0]) > maxIdx:
#       print last_row
#       print row
#       last_row = row


