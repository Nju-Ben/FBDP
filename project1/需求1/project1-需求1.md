# 151099044 胡犇 project1

------
## 需求1 

需求1：针对股票新闻数据集中的新闻标题，编写WordCount程序，统计所有除Stop-word（如“的”，“得”，“在”等）出现次数k次以上的单词计数，最后的结果按照词频从高到低排序输出。
### 1 实验设计说明
1.1 设计思路：涉及mapreduce的部分仍然是wordcount统计词频部分，此部分由过往实验写好，因此本实验的主要任务由key value键值对的设计变为处理key value的输入格式和wordcount程序完成后的降序排序两部分。

1.2 算法设计
step1:读取fulldata.txt数据
step2:每一行按照多个空白进行分片，取其中标题部分
step3:对标题进行分词
step4:将分出来的词进行wordcount统计词频（已由前面任务写好）
step5:生成新的排序Job对step4的结果进行降序处理

1.3 流程图
![](https://i.imgur.com/PToUDde.png)

1.4 程序及类说明
1.4.1 动态输入k：
为wordcount2类定义一个成员变量wc，用来记录词频
```java
	public static int wc;
```
在执行mapreduce job 之前询问用户词频大小，把输入传给wordcount2.wc
```java
	Scanner sc = new Scanner(System.in); 
    System.out.println("请输入词频k?); 
    int wc = sc.nextInt();
    wordcount2.wc=wc;
```
在reduce时会对key value对的词频进行判断，如果词频>=并且字符串长度大于2(说明是词语不是字)，才将其reduce
```java
	Text key1=new Text();
    key1 =key;
	if(sum>=wc && key1.toString().length()>=2)
      {
		result.set(sum);
      	context.write(key, result);
      }
```
1.4.2 分词方法：

采用封装好的IKAnalyzier包，这个软件包能够针对特定的词典进行分词，同时也可以对特定的词典进行忽略停词。（如何配置将在实验报告第二部分说明），配置以后导入相应的包。
```java
    import org.wltea.analyzer.core.IKSegmenter;
	import org.wltea.analyzer.core.Lexeme;
```
对输入格式进行处理，采用split("\t")进行分片，取第五项为标题
```java
	String[] temp = line.split("\t");
	if (temp.length < 6)   
	   	return;
	String values=temp[4];
```
用封装好的包对标题进行分词，分词结果写入key value对中
```java
	byte[]bt=values.getBytes();
    InputStream ip=new ByteArrayInputStream(bt);
    Reader read=new InputStreamReader(ip);
    IKSegmenter iks=new IKSegmenter(read,true);
    Lexeme t;
    while((t=iks.next())!=null)
	{
	    word.set(t.getLexemeText());
		context.write(word, one);
	}
```
1.4.3 排序方法：
排序用到的类：

I 降序输出的类
```java
	private static class IntWritableDecreasingComparator extends IntWritable.Comparator {
      public int compare(WritableComparable a, WritableComparable b) {
        return -super.compare(a, b);
      }

```
II 上一个类中用到的比较的类
```java
	public int compare(byte[] b1, int s1, int l1, byte[] b2, int s2, int l2) {
          return -super.compare(b1, s1, l1, b2, s2, l2);
      }
  }

```
III 读取wordcount输出的中间文件，执行mapreduce排序任务的脚本（仍然在main函数中）
```java
	 FileOutputFormat.setOutputPath(job, new Path("output/wordcount/temp7"));//先将词频统计任务的输出结果写到临时目  
    //录中, 下一个排序任务以临时目录为输入目录。  
    job.setOutputFormatClass(SequenceFileOutputFormat.class);  
    if(job.waitForCompletion(true))  
    {  
        Job sortJob = new Job(conf, "sort");  
        sortJob.setJarByClass(wordcount2.class);  

        FileInputFormat.addInputPath(sortJob, new Path("output/wordcount/temp7"));  
        sortJob.setInputFormatClass(SequenceFileInputFormat.class);  

        /*InverseMapper由hadoop库提供，作用是实现map()之后的数据对的key和value交换*/  
        sortJob.setMapperClass(InverseMapper.class);  
        /*将 Reducer 的个数限定为1, 最终输出的结果文件就是一个。*/  
        sortJob.setNumReduceTasks(1);   
        FileOutputFormat.setOutputPath(sortJob, new Path(otherArgs.get(1)));  

        sortJob.setOutputKeyClass(IntWritable.class);  
        sortJob.setOutputValueClass(Text.class);  
        /*Hadoop 默认对 IntWritable 按升序排序，而我们需要的是按降序排列。 
        * 因此实现了一个 IntWritableDecreasingComparator 类,　 
        * 并指定使用这个自定义的 Comparator 类对输出结果中的 key (词频)进行排序*/  
        sortJob.setSortComparatorClass(IntWritableDecreasingComparator.class);  

        System.exit(sortJob.waitForCompletion(true) ? 0 : 1); 
    }  
```
```java

```

### 2 程序运行和实验结果说明和分析
2.1 实验步骤
首先配置停词文件，按照IkAnalyzer包的readme配置

![](https://i.imgur.com/X5ild6A.png)

将IKAnalyzer.cfg.xml文件中改为使用stopword.dic作为停词词典

![](https://i.imgur.com/tGa6oit.png)

将xml文件和停词词典放在/src下完成配置。

![](https://i.imgur.com/1H7I8mK.png)

打包好源代码成2.jar，打包完成以后在命令行进行操作，首先将fulldata.txt放入HDFS系统中

``` linux
    bin/hdfs dfs -put input/fulldata.txt/fudata.txt /input/wordcount
```

查看其结果（部分）

![](https://i.imgur.com/Qe9hmih.png)

写了个python脚本读取它，发现有121508条记录（非实验步骤）

![](https://i.imgur.com/GSGzoTK.png)
接着执行wordcount程序

``` linux
    bin/hadoop jar 2.jar /input/wordcount/fulldata.txt /output/wordcount/9

```
执行后需要输入词频

![](https://i.imgur.com/Yl1lCk2.png)

输入后查看在命令行的运行结果

![](https://i.imgur.com/WoCFOMo.png)

接下来用cat命令并展示结果（部分）
```linux
	bin/hdfs dfs -cat /output/wordcount/9/*
```
开始部分

![](https://i.imgur.com/LB6RJYC.png)

结束部分

![](https://i.imgur.com/hG1WEH2.png)

2.2 实验结果分析

公告是词频最大的词汇，词频为24011，在总记录为121508条下，基本合理，程序也成功实现了只统计词频大于输入k（此处K=150）的记录。在停词处理方面，当采用如下停词表时，成功过滤掉相关词汇

![](https://i.imgur.com/LxHo3Bz.png)

2.3 实验不足分析
在执行排序任务时，读取的临时文件目录没有将其写活，因此执行完一次之后需要更改其目录，不够灵活。

上述即为实验结果，相关代码及文件同时上传至github