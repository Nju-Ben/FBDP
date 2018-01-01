# 151099044 胡犇 project2

------
## K最邻近算法

实验目标:使用多种机器学习算法对文本进行情感判别，包括KNN、决策树、朴素贝叶斯、支持向量机等，学习如何进行模型训练，如何进行分类预测。
### 1 实验设计说明
1.1 设计思路：采用朴素贝叶斯方法中选好的特征词，对训练集每个文档提取特征词计算TF-IDF值实现对训练集文档的文本向量化，用同样方法实现测试集文本向量化。之后根据k个距离最短训练集打分选出分类。

1.2 流程说明
step1 step2 step4与朴素贝叶斯类似，主要差异在于利用sklearn库函数进行stp3 tf-idf值计算和step5 knn法进行分类

#### step1 将traindata中positive,neutral,negative三个文件夹下的txt分别合并，并且只保留新闻内容，形成positive.txt,neutral.txt,negative.txt三个文本文档。合并前的txt内容是新的文件中的一行。

处理代码:trainingdataprocess.py

输入:Trainingdata数据集

![](https://i.imgur.com/ctaoiao.png)


输出:positive.txt,neutral.txt,negative.txt

![](https://i.imgur.com/Ks2ekCY.png)

该数据用于计算TF-IDF值


#### step2.卡方检验挑选特征词，卡方=(AD-BC)^2/((A+B)*(C+D))，以积极情感为例，A为积极文件夹中包含该词的txt数目，B为其他两个文件夹中包含该词的txt数目，C为积极文件夹中不包含该词的txt数目，D为其他两个文件夹中不包含该词的txt数目，计算出卡方后，按卡方大小进行排序，每个分类凑够1000词，然后去重，剩下约670词。
处理代码:chisquaretest.py

输入:
positive.txt positive1.txt
negative.txt negative1.txt
neutral.txt neutral1.txt

输出:newfeatureword.txt

![](https://i.imgur.com/wPh1vxC.png)


#### step3.计算特征向量(基于TF-IDF方法):这儿的特征向量是指三种情感文件夹中每一个txt(我处理成了一个情感txt中一行)的特征向量，首先将文本内容转化为只保留特征词的文本，利用sklearn包，能够自动计算tf-idf值。

处理代码:knn.py

输入:positive1.txt,neutral.txt,negative1.txt，featureword.txt

该部分文本向量化代码一共使用了四次，分别对积极，中立，消极训练文件和测试文件使用，因此封装
成txt2vector函数,代码如下
```python
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
    print(positive)
    vectorizer=CountVectorizer()
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(positive))
    word=vectorizer.get_feature_names()
    weight=tfidf.toarray()
    return weight
```
上述代码首先是将文本分词和提取特征词后转化为如下格式，每一个单引号之间的内容代表一个原txt文件提取出来的特征词

![](https://i.imgur.com/t7wakZZ.png)

上述文本再调用tf-idf计算函数，转化成向量形式，如图所示，这儿没有写入文件，只显示了部分。

![](https://i.imgur.com/8y4qTlF.png)

该矩阵共有a行b列 a为情感文件夹下txt数量，b为特征词个数

 
#### step4.测试集预处理
将公司的所有新闻标题进行合并。

处理代码fulldataprocess.py

输入:fulldata.txt

![](https://i.imgur.com/ljcMb8h.png)

输出:testdata.txt

![](https://i.imgur.com/gi5VFoP.png)

#### step5.分类结果
基于计算好的tfidf值，利用sklearn中Knn函数进行分类,并写入
knnresult.txt文件中
处理代码仍然在knn.py中
```python
testweight=text2vector("G:/testdata.txt")
for i in range(25):
    testweight=np.insert(testweight, -1, values=0, axis=1)

weight=[]
weight1=text2vector("G:/positive.txt")
weight2=text2vector("G:/neutral.txt")
weight3=text2vector("G:/negative.txt")
weight3 = np.delete(weight3, -1, axis=1) 

#将三种情感的训练样本合并，并且生成标签类型
for i in range(len(weight1)+len(weight2)+len(weight3)):
    if i<len(weight1):
        weight.append(weight1[i])
    elif i<len(weight1)+len(weight2):
        weight.append(weight2[i-len(weight1)])
    else:
        weight.append(weight3[i-len(weight1)-len(weight2)])
#将三种情感的训练样本合并    
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
#生成标签类型    
        
knn = neighbors.KNeighborsClassifier() #取得knn分类器    
data = np.array(weight)
labels = np.array(l) 
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
```
分类结果如下图所示，3 代表消极，2 代表中立，1 代表积极

![](https://i.imgur.com/wb0sqXw.png)

上述为实验结果


