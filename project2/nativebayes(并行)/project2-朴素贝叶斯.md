# 151099044 胡犇 project2

------
## 朴素贝叶斯

实验目标:使用多种机器学习算法对文本进行情感判别，包括KNN、决策树、朴素贝叶斯、支持向量机等，学习如何进行模型训练，如何进行分类预测。
### 1 实验设计说明
1.1 设计思路：训练集训练和测试集预测两部分利用mapreduce完成，中间部分数据处理利用python完成

1.2 流程说明
#### step1 将traindata中positive,neutral,negative三个文件夹下的txt分别合并，并且只保留新闻内容，形成positive.txt,neutral.txt,negative.txt三个文本文档。合并前的txt内容是新的文件中的一行。

处理代码:trainingdataprocess.py

输入:Trainingdata数据集

![](https://i.imgur.com/ctaoiao.png)


输出:positive.txt,neutral.txt,negative.txt

![](https://i.imgur.com/Ks2ekCY.png)

该数据用于hadoop分词并统计词频



#### step2、将第一步得到的三个分类下的文档进行分词，统计词频(词频用于计算特征值)。
处理代码:wordcount2.java及其项目

输入:positive.txt,neutral.txt,negative.txt（图片同上）

输出:positive1.txt,neutral.txt,negative1.txt

![](https://i.imgur.com/vw0tn1s.png)
（该图片展示为negative1.txt）

#### step3.卡方检验挑选特征词，卡方=(AD-BC)^2/((A+B)*(C+D))，其中A为积极文件夹中包含该词的txt数目，B为其他两个文件夹中包含该词的txt数目，C为积极文件夹中不包含该词的txt数目，D为其他两个文件夹中不包含该词的txt数目，计算出卡方后，按卡方大小进行排序，每个分类凑够1000词，然后去重，剩下约670词。
处理代码:chisquaretest.py

输入:
positive.txt positive1.txt
negative.txt negative1.txt
neutral.txt neutral1.txt

输出:newfeatureword.txt

![](https://i.imgur.com/wPh1vxC.png)


#### step4.计算特征向量(基于词频):每一类特征上的值为该分类下特征词除以总词数，将所有频数为0的词初始化为1，防止乘数为0的情况，同时为避免数据过小无法读出结果，对每一个词频进行乘1000调整。

处理代码:featureprocess.txt

输入:positive1.txt,neutral.txt,negative1.txt
输出:newfeature.txt

![](https://i.imgur.com/UbwVsHe.png)

#### step5.测试集预处理
将公司的所有新闻标题进行合并。
输入:fulldata.txt

![](https://i.imgur.com/ljcMb8h.png)

输出:testdata.txt

![](https://i.imgur.com/gi5VFoP.png)

处理代码fulldataprocess.py

step6.测试集进行分类
原理:将三类特征的特征向量数据存储在全局变量中，读取testdata.txt数据,并行处理时，对于每一个公司的新闻标题，扫描特征词，若特征词出现在标题中，则按三类，乘以其特征值，否则乘以某一调整后数值，这样能计算出三类特征的P(Yi|X),再乘以P（Yi），比较i=1,2,3,时P(Yi|X)*P（Yi）大小，最大的那个即为分类。
处理代码 wordcount3.java及其项目

输入:
testdata.txt(hdfs)
newfeature.txt(本地)
输出
result.txt

![](https://i.imgur.com/2MjwD0v.png)

![](https://i.imgur.com/fxBBTFZ.png)

![](https://i.imgur.com/rB1ppB7.png)

因为某些特殊原因，1代表积极，2代表中立，3代表消极

### 2 程序说明和分析(未完待续)
