# coding:utf-8  
import jieba  
import os  
import sys  
import re
import numpy as np  
import jieba.posseg as pseg  
from sklearn import feature_extraction 
from sklearn import neighbors  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer

  
#text2vector函数用于将测试文本进行向量化
#转换为tf-idf值

def text2vector(filename):
    featureword=[]
    positive=[]
    with open ("G:/newfeatureword.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
        while 1:
            line = file.readline()
            temp= re.split('\t|\n',line)
            if len(temp)>1:
                featureword.append(temp[0])
            if not line:
                break
            pass
    file.close()
     
    with open (filename, 'r', encoding= 'utf-8' ,errors="ignore") as file:
        while 1:
            line = file.readline()
            if not line:
                break
            pass
            cut = jieba.lcut(line)
            tempstr=''
            for word in cut:
                if word in featureword:
                    tempstr=tempstr+str(word) 
                    tempstr=tempstr+' '
            positive.append(tempstr)
    file.close()
    
    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(positive))
    word=vectorizer.get_feature_names()
    weight=tfidf.toarray()
    return weight
#计算tf-idf值

#取得测试数据
testweight=text2vector("G:/testdata.txt")
for i in range(25):
    testweight=np.insert(testweight, -1, values=0, axis=1)

weight=[]
weight1=text2vector("G:/positive.txt")
weight2=text2vector("G:/neutral.txt")
weight3=text2vector("G:/negative.txt")
weight3 = np.delete(weight3, -1, axis=1)  
for i in range(len(weight1)+len(weight2)+len(weight3)):
    if i<len(weight1):
        weight.append(weight1[i])
    elif i<len(weight1)+len(weight2):
        weight.append(weight2[i-len(weight1)])
    else:
        weight.append(weight3[i-len(weight1)-len(weight2)])
        
l1=[1 for x in range(517)]
l2=[2 for x in range(512)]
l3=[3 for x in range(471)]
l=[]
for i in range(len(l1+l2+l3)):
    if i<len(l1):
        l.append(l1[i])
    elif i<len(l1+l2):
        l.append(l2[i-len(l1)])
    else:
        l.append(l3[i-len(l1)-len(l2)])
        
        
#将三种情感的训练样本合并，并且生成标签类型

knn = neighbors.KNeighborsClassifier() #取得knn分类器    
data = np.array(weight)
labels = np.array(l) #labels则是对应Romance和Action  
knn.fit(data,labels) #导入数据进行训练   



sentiment=[]
for i in range(len(testweight)):
    sentiment.append(knn.predict([testweight[i]]))
incname=[]

with open ("G:/testdata.txt", 'r', encoding= 'utf-8' ,errors="ignore") as file:
    while 1:
        line = file.readline()
        if not line:
            break
        temp= re.split('\t|\n',line)
        #print(temp)
        incname.append(temp[0])
        
        pass
file.close()

file = open('G://knnresult.txt','a')
for i in range(3260):
    file.write(repr(incname[i])+'\t')
    file.write(repr(sentiment[i])+'\n')
file.close()

