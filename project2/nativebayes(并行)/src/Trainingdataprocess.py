#_*_ coding: gbk _*_
import re
import pandas as pd
nagative=[]
positive=[]
neutral=[]
for i in range(0,471):
    with open ("G://TrainingData/negative/"+str(i)+".txt", 'r', encoding= 'gbk' ,errors="ignore") as file:
        data=file.read()
        nagative.append(data)
#合并消极新闻       
 
for i in range(0,512):
    with open ("G://TrainingData/neutral/"+str(i)+".txt", 'r', encoding= 'gbk' ,errors="ignore") as file:
        data=file.read()
        neutral.append(data)
#合并中性新闻

for i in range(0,517):
    with open ("G://TrainingData/positive/"+str(i)+".txt", 'r', encoding= 'gbk' ,errors="ignore") as file:
        data=file.read()
        positive.append(data)
#合并积极新闻

        
for i in range(0,471):
    nagative[i]=re.sub("[A-Za-z0-9\“\”\:\：\)\《\》\;\；\【\】\<\>\-\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+", "", nagative[i])

for i in range(0,512):
    neutral[i]=re.sub("[A-Za-z0-9\“\”\·\:\：\)\《\》\;\；\【\】\<\>\-\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+", "", neutral[i])
    
for i in range(0,517):
    positive[i]=re.sub("[A-Za-z0-9\“\”\·\:\：\)\《\》\;\；\【\】\<\>\-\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+", "", positive[i])
#处理掉其中的数字符号等，只保留中文

file = open('G://negative.txt','a')
for i in range(0,471):
    file.write(repr(nagative[i])+'\n')
file.close()


file = open('G://positive.txt','a')
for i in range(0,517):
    file.write(repr(positive[i])+'\n')
file.close()

file = open('G://neutral.txt','a')
for i in range(0,512):
    file.write(repr(neutral[i])+'\n')
file.close()
#将处理结果写入txt中存储


