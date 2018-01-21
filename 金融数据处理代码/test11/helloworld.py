# _*_ coding: GBK _*_

'''
Created on 2017年9月22日

@author: 1
'''
# def is_chinese(uchar):
#     if uchar >= u'\u4E00' and uchar <= u'\u9FA5':
#         return True
#     else:
#         return False
#   
#   
# with open ("d:/stock/货币政策报告2017.1.txt", 'r', encoding= 'gbk' ,errors="ignore") as file:
#     data=file.read()
# _dict={}
# for uchar in data:
#     if  is_chinese(uchar):
#         if uchar in _dict:
#             _dict[uchar] = _dict[uchar] + 1
#         else:
#             _dict[uchar] = 1
# file.close();
#  
# l=sorted(_dict.items(), key=lambda _dict:_dict[1], reverse = True)
# 
# for i in l:
#     if i[1]>200:
#         print(i)
# 
# print(l)

import jieba
from collections import Counter
with open ("d:/stock/货币政策报告2017.1.txt", 'r', encoding= 'gbk' ,errors="ignore") as file:
    data=file.read()
cut = jieba.cut(data)
print(cut)
data = dict(Counter(cut))
#print(data)
data1=data.copy()
# for (k,v) in data.items():
#     #print(len(k))
#     print(v)
#     if len(k)<2:
#         data1.pop(k)
# y1=sorted(data1.items(), key=lambda data1:data1[1], reverse = True )
# print(y1)
# file.close
for i in data.items():
    #print(len(k))
    if len(i[0])<2 or i[1]<10:
        data1.pop(i[0])
#y1=sorted(data1.items(), key=lambda data1:data1[1], reverse = True )
file.close


with open ("d:/stock/货币政策报告2017.2.txt", 'r', encoding= 'gbk' ,errors="ignore") as file:
    data=file.read()
cut = jieba.cut(data)
data = dict(Counter(cut))

data2=data.copy()

for i in data.items():
    #print(len(k))
    if len(i[0])<2 or i[1]<10:
        data2.pop(i[0])
#y2=sorted(data2.items(), key=lambda data2:data2[1], reverse = True )

k1=data1.keys();
k2=data2.keys();
y2=k2-k1

#print (y2)
dict2={}
for i in y2:
    dict2[i]=data2[i]
#print (dict2)

y3=sorted(dict2.items(), key=lambda dict2:dict2[1], reverse = True )
print(y3)       
    
#l=set(y1)|set(y2)-set(y1)



#print (l1)

#y3=sorted(l2.items(), key=lambda l2:l2[1], reverse = True)
#print(l1)

# y=sorted(data.items(), key=lambda d:d[1], reverse = True )
# print(y)
# print(len(y))









#print(_dict.items())
#print(_dict.keys())
#print(_dict['的'])
# 
# d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
# print(d['Michael'])
# l=sorted(d.items(), key=lambda d:d[1], reverse = True)










