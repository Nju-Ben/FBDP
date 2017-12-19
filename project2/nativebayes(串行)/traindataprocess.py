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
        
for i in range(0,512):
    with open ("G://TrainingData/neutral/"+str(i)+".txt", 'r', encoding= 'gbk' ,errors="ignore") as file:
        data=file.read()
        neutral.append(data)

for i in range(0,517):
    with open ("G://TrainingData/positive/"+str(i)+".txt", 'r', encoding= 'gbk' ,errors="ignore") as file:
        data=file.read()
        positive.append(data)
        
for i in range(0,471):
    nagative[i]=re.sub("[A-Za-z0-9\“\”\:\：\)\《\》\;\；\【\】\<\>\-\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+", "", nagative[i])

for i in range(0,512):
    neutral[i]=re.sub("[A-Za-z0-9\“\”\·\:\：\)\《\》\;\；\【\】\<\>\-\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+", "", neutral[i])
    
for i in range(0,517):
    positive[i]=re.sub("[A-Za-z0-9\“\”\·\:\：\)\《\》\;\；\【\】\<\>\-\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+", "", positive[i])
    #pattern =re.compile(u"[\u4e00-\u9fa5]+")
    #nagative[i]=re.findall(pattern,nagative[i])
    
    #nagative[i]=re.match("[\u4E00-\u9FA5]",nagative[i]);

#[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]"
#line = line.decode("utf8")
#string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),line)
#file = open('G://negative.txt','w+')

file = open('G://positive.txt','a')
for i in range(0,517):
    #file.write(repr(str(nagative[i])+'\n'))
    file.write(repr(positive[i])+'\n')
file.close()

file = open('G://neutral.txt','a')
for i in range(0,512):
    #file.write(repr(str(nagative[i])+'\n'))
    file.write(repr(neutral[i])+'\n')
file.close()

