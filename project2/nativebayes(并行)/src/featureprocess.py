import pandas as pd
from pandas.core.frame import DataFrame
import re
featureword=[]
positivenum=[]
neutralnum=[]
negativenum=[]
num=[]

with open ("G:/newfeatureword.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        temp= re.split('\t|\n',line)
        if len(temp)>1:
            featureword.append(temp[0])
        #num.append(temp[0])
        if not line:
            break
        pass
file.close()
c={"word":featureword}

data=DataFrame(c)#
data['positivenum']=1
data['neutralnum']=1
data['negativenum']=1


with open ("G:/positive1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        temp= re.split('\t|\n',line)
        if len(temp)>1 and temp[1] in featureword:
            index = data[data.word==temp[1]].index
            data.iloc[index,1]=int(temp[0])
        if not line:
            break
        pass
file.close()

with open ("G:/neutral1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        temp= re.split('\t|\n',line)
        print(temp)
        if len(temp)>1 and temp[1] in featureword:
            index = data[data.word==temp[1]].index
            data.iloc[index,2]=int(temp[0])
        if not line:
            break
        pass
file.close()

with open ("G:/negative1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        temp= re.split('\t|\n',line)
        if len(temp)>1 and temp[1] in featureword:
            index = data[data.word==temp[1]].index
            data.iloc[index,3]=int(temp[0])
        if not line:
            break
        pass
file.close()

sum1=data['positivenum'].sum()
sum2=data['neutralnum'].sum()
sum3=data['negativenum'].sum()
data['positivenum']=data['positivenum']/sum1*1000
data['neutralnum']=data['neutralnum']/sum2*1000
sum3=data['negativenum']=sum3=data['negativenum']/sum3*1000

#print(data)
file = open('G://newfeature.txt','a')
for i in range(0,610):
    file.write(repr(data.iloc[i,0])+'\t')
    file.write(repr(data.iloc[i,1])+'\t')
    file.write(repr(data.iloc[i,2])+'\t')
    file.write(repr(data.iloc[i,3])+'\n')
    #file.write(repr(data.iloc[i,4])+'\n')
file.close()