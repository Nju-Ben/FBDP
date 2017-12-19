import pandas as pd
import re
import math
from pandas.core.frame import DataFrame
#利用dataframe存储数据

positive=[]
neutral=[]
negative=[]

noneutral=[]
nonegative=[]
nopositive=[]

positiveword=[]
neutralword=[]
negativeword=[]

with open ("G:/positive.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        positive.append(line)
        noneutral.append(line)
        nonegative.append(line)
file.close()
    
with open ("G:/neutral.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        nopositive.append(line)
        nonegative.append(line)
        neutral.append(line)
file.close()

with open ("G:/negative.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        nopositive.append(line)
        noneutral.append(line)
        negative.append(line)
file.close()
#打开训练文本，后面主要用于判断分好的词是否在训练文本中

frequencypositive={}
frequencyneutral={}
frequencynegative={}

with open ("G:/positive1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        if not line:
            break
        temp= re.split('\t|\n',line)
        if len(temp)>1:
            positiveword.append(temp[1])
            frequencypositive[temp[1]]=temp[0]
            #dict2[neutralword[i]]=chisquare
        
        pass
file.close()
with open ("G:/neutral1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        if not line:
            break
        temp= re.split('\t|\n',line)
        if len(temp)>1:
            neutralword.append(temp[1])
            frequencyneutral[temp[1]]=temp[0]
        pass
file.close()
with open ("G:/negative1.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        if not line:
            break
        temp= re.split('\t|\n',line)
        if len(temp)>1:
            negativeword.append(temp[1])
            frequencynegative[temp[1]]=temp[0]
        pass
file.close()
#读入mapreduce处理好的分词文件，将词语记录在内存变量中

#卡方=(AD-BC)^2/((A+B)*(C+D))

#A为积极文件夹中包含该词的txt数目
#B其他两个文件夹中包含该词的txt数目
#C为积极文件夹中不包含该词的txt数目
#D为其他两个文件夹中不包含该词的txt数目

dict1={}
dict2={}
dict3={}

for i in range(0,len(positiveword)):
    A=0
    B=0
    C=0
    D=0
    chisquare=0
    for j in range(0,len(positive)):
        if positiveword[i] in positive[j]:
            A=A+1
        else:
            B=B+1
    for k in range(0,len(nopositive)):
        if positiveword[i] in nopositive[k]:
            C=C+1
        else:
            D=D+1
    chisquare=(A*D-B*C)*(A*D-B*C)/((A+B)*(C+D))
    dict1[positiveword[i]]=chisquare
    
y1=sorted(dict1.items(), key=lambda dict1:dict1[1], reverse = True)

for i in range(0,len(neutralword)):
    A=0
    B=0
    C=0
    D=0
    chisquare=0
    for j in range(0,len(neutral)):
        if neutralword[i] in neutral[j]:
            A=A+1
        else:
            B=B+1
    for k in range(0,len(noneutral)):
        if neutralword[i] in noneutral[k]:
            C=C+1
        else:
            D=D+1
    chisquare=(A*D-B*C)*(A*D-B*C)/((A+B)*(C+D))
    dict2[neutralword[i]]=chisquare
    
y2=sorted(dict2.items(), key=lambda dict2:dict2[1], reverse = True)

for i in range(0,len(negativeword)):
    A=0
    B=0
    C=0
    D=0
    chisquare=0
    for j in range(0,len(negative)):
        if negativeword[i] in negative[j]:
            A=A+1
        else:
            B=B+1
    for k in range(0,len(nonegative)):
        if negativeword[i] in nonegative[k]:
            C=C+1
        else:
            D=D+1
    chisquare=(A*D-B*C)*(A*D-B*C)/((A+B)*(C+D))
    dict3[negativeword[i]]=chisquare
    
y3=sorted(dict3.items(), key=lambda dict3:dict3[1], reverse = True)
#print(y3)


featureword=[]
for i in range(0,334):
    featureword.append(y1[i][0])
    featureword.append(y2[i][0])
    featureword.append(y3[i][0])
    
#print(featureword)

newfeatureword=[]

with open ("G:/newfeatureword.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        if not line:
            break
        temp= re.split('\ufeff\t|\n',line)
        print(temp)
        newfeatureword.append(temp[0])
        #temp= re.split('\t|\n',line)
        #if len(temp)>1:
            #negativeword.append(temp[1])
        pass
file.close()
newfeatureword.pop(0)
print(len(newfeatureword))

#print(frequencypositive.keys())
#print(frequencypositive.values())
print(newfeatureword)
file = open('G://chiwords.txt','a')
for i in range(0,len(featureword)):
    file.write(featureword[i]+'\n')
file.close()

# file = open('G://newfeature.txt','a')
# for i in range(0,len(newfeatureword)):
#     file.write(repr(newfeatureword[i])+'\t')
#     file.write(repr(frequencypositive[newfeatureword[i]])+'\t')
#     file.write(repr(frequencyneutral[newfeatureword[i]])+'\t')
#     file.write(repr(frequencynegative[newfeatureword[i]])+'\n')
# file.close()


#print(dict.values())
#print(dict.keys())

#print(len(positive))
#print(len(nopositive))
#print(positiveword)
