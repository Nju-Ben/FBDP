import pandas as pd
from pandas.core.frame import DataFrame
import re
import jieba
import math
featureword=[]
positivenum=[]
neutralnum=[]
negativenum=[]
num=[]
#file = open("G:/positiveword.txt")
with open ("G:/featureword.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        #print(line)
        temp= re.split('\t|\n',line)
        #temp=line.split('\t|\n');
        #print(temp)
        if len(temp)>1:
            featureword.append(temp[1])
            num.append(temp[0])
        if not line:
            break
        pass
file.close()
c={"word":featureword,
   "totalnum":num}#

data=DataFrame(c)#
data['positivenum']=2
data['neutralnum']=2
data['negativenum']=2


with open ("G:/positive1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        temp= re.split('\t|\n',line)
       # print(temp)
        #temp=line.split('\t|\n');
        #print(temp)
        if len(temp)>1 and temp[1] in featureword:
           # data[data['word']==temp[1]].iloc[0,2]=temp[0]
            index = data[data.word==temp[1]].index
            data.iloc[index,2]=int(temp[0])
        if not line:
            break
        pass
file.close()

with open ("G:/neutral1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        temp= re.split('\t|\n',line)
       # print(temp)
        #temp=line.split('\t|\n');
        #print(temp)
        if len(temp)>1 and temp[1] in featureword:
           # data[data['word']==temp[1]].iloc[0,2]=temp[0]
            index = data[data.word==temp[1]].index
            data.iloc[index,3]=int(temp[0])
        if not line:
            break
        pass
file.close()

with open ("G:/negative1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        temp= re.split('\t|\n',line)
       # print(temp)
        #temp=line.split('\t|\n');
        #print(temp)
        if len(temp)>1 and temp[1] in featureword:
           # data[data['word']==temp[1]].iloc[0,2]=temp[0]
            index = data[data.word==temp[1]].index
            data.iloc[index,4]=int(temp[0])
        if not line:
            break
        pass
file.close()
print(data)

from collections import Counter
stockword=[]
title=[]
with open ("G:/fulldata1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    line = file.readline()
    temp= re.split('\t',line)
    stockword.append(temp[1])
    title.append(temp[4])
    while 1:
        line = file.readline()
        if not line:
            break
        #print(line)
        temp= re.split('\t',line)
        #print(temp)
        if len(temp)==7:
            if temp[1]==stockword[-1]:
                #stockword.append(temp[1])
                title[-1]=title[-1]+temp[4]
            else:
                stockword.append(temp[1])
                title.append(temp[4])
        pass
file.close()
c1={"stockword":stockword,
   "title":title}
data1=DataFrame(c1)#
#with open ("G://fulldata.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    #data=file.read()
    #print(data)
data1['sentiment']=0
for j in range(0,3260):
    cut = jieba.cut(data1.iloc[j,1])
    word=list(cut)
    word1=word
    for i in word1:
        if len(i)<2:
            word.remove(i)
    #print(data)
    #data1 = dict(Counter(cut))
    
    positive=1
    negative=1
    neutral=1
    for i in range(0,783):
        if data.iloc[i,1] in word:
            positive=positive*math.log2(data.iloc[i,2])
            neutral=neutral*math.log2(data.iloc[i,3])
            negative=negative*math.log2(data.iloc[i,4])
    positive=positive*math.log2(517)
    neutral=neutral*math.log2(512)
    negative=negative*math.log2(471)
    print(positive)
    print(neutral)
    print(negative)
    if positive>neutral and positive>negative:
        data1.iloc[j,2]=1
        print("fuck you positive")
    if neutral>positive and neutral>negative:
        print("fuck you neutral")
        data1.iloc[j,2]=0
    if negative>neutral and negative>positive:
        print("fuck you negative")
        data1.iloc[j,2]=-1
#print(data1)
    #index = data[data.word==temp[1]].index
    #data.iloc[index,2]=int(temp[0])
file.close()
file = open('G://result.txt','a')
for i in range(0,3260):
    file.write(repr(data1.iloc[i,0])+'\t')
    file.write(repr(data1.iloc[i,1])+'\t')
    file.write(repr(data1.iloc[i,2])+'\n')
file.close()