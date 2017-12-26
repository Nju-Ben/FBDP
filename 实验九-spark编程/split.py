# _*_ coding: utf-8 _*_
from pyspark import SparkConf, SparkContext  
import jieba
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from operator import add

#spark = SparkSession\
#.builder\
#.appName("PythonWordCount")\
#.getOrCreate()
if __name__ == "__main__":
	conf = SparkConf().setAppName("wordSplit")  
	conf.setMaster("local")  
	sc= SparkContext(conf = conf)  
	with open ("/home/huben/testdata.txt") as file:
	    data=file.read()
	cut = jieba.lcut(data)
	list=[]
	for i in cut:
	    if len(i)>=2:
		list.append(i)
	lines = sc.parallelize(list)
	#counts = lines.flatMap(lambda x: x.split(' ')) \
	counts = lines.map(lambda x: (x, 1)) \
		  .reduceByKey(add).sortByKey()
	output = counts.collect()
	result={}
	for (word, count) in output:
	    result[str(word)]=count
	y=sorted(result.items(), key=lambda result:result[1], reverse = True)
	#print(sys.argv[1])
	#print(y)
	for i in y:
	    if i[1]>int(int(sys.argv[1])):
		print("%s: %i" % (i[0], i[1]))
	
#spark.stop()
