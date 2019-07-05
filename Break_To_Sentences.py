#coding: utf-8
"""
Created on Tue Jul  2 19:55:30 2019

@author: raymond
"""
#-----------------------------IMPORT------------------------------------------#
import csv
import spacy
import pandas as pd
#------------------------------CONSTANS---------------------------------------#
description = []
titles = []
locations = []
companies = []
urls = []
salaries = []
summaries = []
headers = ["Title","Location","Company","Salary", "URL","Summary"]
df = pd.DataFrame(columns=headers)# HEADER OF CSV FILE
filename = "Scraping_From_Indeed5.csv"
#---------------------------METHODS-------------------------------------------#
with open(filename, 'r',encoding = 'utf8',errors = 'ignore') as f:
    reader = csv.reader(f)
    count = 0
    for row in reader:
        if count != 0:
            titles.append(row[0])
            locations.append(row[1])
            companies.append(row[2])
            salaries.append(row[3])
            description.append(row[4])
            urls.append(row[5])
        count += 1    
print("Read File Done")
nlp = spacy.load('en')
for i in description:
    doc = nlp(i)
    sentences = []
    for sent in doc.sents:
        sentences.append(sent.string.replace("\n"," "))
    summaries.append(sentences)
print("Spacy Done")
i = 0
with open('test.csv','w', encoding = 'utf8') as f:
    wtr = csv.writer(f)
    while i < len(urls):
        data_list = []
        data_list.append(titles[i])
        data_list.append(locations[i]) 
        data_list.append( companies[i])
        data_list.append(salaries[i])
        data_list.append(urls[i])
        j = 0
        while j < len(summaries[i]):
            data_list.append(summaries[i][j])
            j += 1
        if count == 0:
            wtr.writerow(tuple(headers))
            wtr.writerow(tuple(data_list))
        else:
            wtr.writerow(tuple(data_list))
        i += 1
#-----------------------------------------------------------------------------#





