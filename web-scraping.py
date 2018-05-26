##web scraping
##Joe Huang
## https://github.com/jhuangsa/

import requests
from bs4 import BeautifulSoup
import re
import itertools
import csv
import time 
# cd Dropbox/code2017August/pachong-2018/ && source .env/bin/activate  
# source .env/bin/activate      
# and ('dd' == papers.contents[1].name))  
# and ('a' == papers.dt.contents[0].name)
# and ('dd' == papers.contents[-1].name))

def getnames_econpapers(links, l):
    for link in links:     
        soup = BeautifulSoup(requests.get(link).text)
        
        list_volume = []
        list_paper = []
        list_name = []
        i =0 
        j =0
        for volume in soup.find_all('b'):
            if ('a' == volume.contents[0].name):
                volume_values = volume.find_all('a')
                #print type(volume_values)
                volume_values_name = [" ".join(str(x.get_text().encode('ascii', 'ignore')).split()[0:]) for x in volume_values]
                
                volume_values_name = volume_values_name[0].split(',')
                list_volume.append(volume_values_name)
                #print volume_values_name
        for papers in soup.find_all('dl'):
            list_paper = []
            for paper_name in papers.find_all('dt'):
                paper_name_value = paper_name.find_all('a')
                paper_name_value = [" ".join(str(x.get_text().encode('ascii', 'ignore')).split()[0:]) for x in paper_name_value] 
                list_paper.append(list_volume[i]+paper_name_value)

            j = 0
            for part in papers.find_all('dd'):
                name = part.find_all('i')
                name = [" ".join(str(x.get_text().encode('ascii', 'ignore')).split()[::-1]) for x in name]
                list_name.append(name)
                l.append(list_paper[j]+name)
                print l[-1]

                j=j+1

            i=i+1
            if (i == len(list_volume)) :
                break;

        #time.sleep(10)

                

#Site:        http://econpapers.repec.org/article/ucpjpolec/       

names_jpe = []
link_stem = 'https://econpapers.repec.org/article/ucpjpolec/default'

page_range = ['']
links = [link_stem + str(num) + '.htm' for num in page_range]
getnames_econpapers(links, names_jpe)

#page_range = range(1,10)
#links = [link_stem + str(num) + '.htm' for num in page_range]
#getnames_econpapers(links, names_jpe)

with open('names_jpe.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(names_jpe) 
