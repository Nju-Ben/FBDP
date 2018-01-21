#_*_ coding: utf-8 _*_
import jieba
from collections import Counter
with open ("G://fulldata.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    data=file.read()
    print(data)
cut = jieba.cut(data)
data = dict(Counter(cut))

data1=data.copy()

# for (k,v) in data.items():
#     #print(len(k))
#     if len(k)<2:
#         data1.pop(k)
# y1=sorted(data1.items(), key=lambda data1:data1[1], reverse = True)
# 
for i in data.items():
    if len(i[0])<2 or i[1]<10:
        data1.pop(i[0])
dict2={}
for i in data1:
    dict2[i]=data1[i]

y3=sorted(dict2.items(), key=lambda dict2:dict2[1], reverse = True )
print (y3)
#print(y1)

