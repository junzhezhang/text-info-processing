import csv

truePath ="/Users/junzhezhang/Downloads/text-info-processing/"
#fileName =truePath+"epochTimeLog_resnet_3epoch.text"
fileName1 =truePath+"vec_run.text" 
fileName2 = truePath+"vec_run.csv"
fileName3 = truePath + "swap_block.text"

### convert from vec_run.text (one iteration) into vec_run.csv
# rows_list = []
# rows_list.append(['index','MallocFree','block_','data_'])
# f1 = open(fileName1)
# for row in f1:
#     rows_list.append(row.split())

# with open(fileName2, 'wb') as f:
#     writer = csv.writer(f)
#     writer.writerows(rows_list) 

### info for AlexNet
maxLen = 612
location = 1247
maxIdx = 247
blocks = set([]) 

### split_row, list of blockInfo; sort with 
f2 = open(fileName2)
rows = f2.read().splitlines()
print len(rows)
split_rows = []
i = 0
for row in rows:
  if i>0:
    values = row.split(',')
    #print values
    split_rows.append(values+[i-1])
    #break
  i = i+1
print len(split_rows)
print split_rows[0]


split_rows.sort(key = lambda x: x[2]) # sort in place.

print len(blocks)
for row in split_rows:
  blocks.add(row[2])
print len(blocks)

rows_by_blocks =[]
tempBlock = ''
rows_for_this_block =[]
rows_by_blocks = []
for row in split_rows:
  if tempBlock == row[2] and row[1] != '-1':
    rows_for_this_block.append(row)
  else: 
    tempBlock = row[2]
    if len(rows_for_this_block)>0:
      rows_by_blocks.append(rows_for_this_block)
      rows_for_this_block = []
print len(rows_by_blocks)

for row in rows_by_blocks:
  print "====================="
  for r in row:
    print r

#   print "------------------------------"
#   rows_for_this_block =[]

#     if block == row[2]:
#       .append(row)
#       if row[1] == '-1': # handle -1 in btw
#         rows_by_blocks.append(rows_for_this_block)
#         print len(rows_for_this_block)

#         rows_for_this_block =[]
#       #print row
#   rows_by_blocks.append(rows_for_this_block)

# print len(rows_by_blocks)


# for row in rows_by_blocks:
# #   print "------------------------------"
#   print len(row)
#   if int(row[0][-1]) > 247:  #and int(row[0][1]) != 1:
#     for r in row:
#       print r
# print "=========================="
# for row in rows_by_blocks:
#   print len(row)






