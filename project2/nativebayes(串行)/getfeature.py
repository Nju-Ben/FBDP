import pandas as pd
from pandas.core.frame import DataFrame
import re
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
data['positivenum']=0
data['neutralnum']=0
data['negativenum']=0


with open ("G:/positive1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        temp= re.split('\t|\n',line)
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
        if len(temp)>1 and temp[1] in featureword:
           # data[data['word']==temp[1]].iloc[0,2]=temp[0]
            index = data[data.word==temp[1]].index
            data.iloc[index,4]=int(temp[0])
        if not line:
            break
        pass
file.close()

# sum1=data['positivenum'].sum()
# sum2=data['neutralnum'].sum()
# sum3=data['negativenum'].sum()
# data['positivenum']=data['positivenum']/sum1
# data['neutralnum']=data['neutralnum']/sum2
# sum3=data['negativenum']=sum3=data['negativenum']/sum3

print(data)
file = open('G://feature.txt','a')
for i in range(0,783):
    file.write(repr(data.iloc[i,0])+'\t')
    file.write(repr(data.iloc[i,1])+'\t')
    file.write(repr(data.iloc[i,2])+'\t')
    file.write(repr(data.iloc[i,3])+'\t')
    file.write(repr(data.iloc[i,4])+'\n')
file.close()
