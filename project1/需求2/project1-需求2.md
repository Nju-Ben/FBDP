# 151099044 胡犇 project1

------
## 需求2

需求2：针对股票新闻数据集，以新闻标题中的词组为key，编写带URL属性的文档倒排索引程序，将结果输出到指定文件。
### 1 实验设计说明
1.1 设计思路：仍然读取fulldata.txt数据文件,获取标题和url，将标题进行分词，涉及mapreduce的部分是倒排索引部分，map时将分好的词语作为Key,将url作为value，reduce时考虑到输出结果的价值，将包含数字的key都抛弃，因此需要写一个正则匹配。

1.2 算法设计
step1:读取fulldata.txt数据
step2:每一行按照多个空白进行分片，取其中标题和url部分
step3:对标题进行分词
step4:将分出来的词和url进行倒排索引
step5:reduce时加一个包含数字的判断，只输出不包含数字的结果。

1.3 流程图
![](https://i.imgur.com/Txi4fdd.png)

1.4 程序及类说明
1.4.1 分词方法：

采用封装好的IKAnalyzier包，这个软件包能够针对特定的词典进行分词，同时也可以对特定的词典进行忽略停词。（如何配置将在实验报告第二部分说明），配置以后导入相应的包。
```java
    import org.wltea.analyzer.core.IKSegmenter;
	import org.wltea.analyzer.core.Lexeme;
```
对输入格式进行处理，采用split("\t")进行分片，取第五项为标题，第六项为url
```java
	String[] temp = line.split("\t");
	if (temp.length ！= 6)   
	   	return;
	String values=temp[4];
	String url=temp[5];
```
用封装好的包对标题进行分词，分词结果写入key value对中
```java
    byte[]bt=values.getBytes();
    InputStream ip=new ByteArrayInputStream(bt);
    Reader read=new InputStreamReader(ip);
    IKSegmenter iks=new IKSegmenter(read,true);     Lexeme t;
    Text word1 = new Text();
    Text word2 = new Text();
    while((t=iks.next())!=null)
    {
    	  word1.set(t.getLexemeText());
 	   	  word2.set(urls);
 	   	  context.write(word1,word2);
    }
```
1.4.2 判断字符串包含数字：

I 相关类
```java
  public static boolean isContainNumber(String company) {

      Pattern p = Pattern.compile("[0-9]");
      Matcher m = p.matcher(company);
      if (m.find()) {
          return true;
      }
      return false;
  }

```
II reduce时调用该类
```java
	if(x.length()>=2 && isContainNumber(x)==false)
      {
      context.write(key, new Text(all.toString()));
    } }//

```

### 2 程序运行和实验结果说明和分析
2.1 实验步骤


打包好源代码成inverted.jar，

接着执行程序

``` linux
    bin/hadoop jar inverted.jar /input/wordcount/fulldata.txt /output/invertedIndex/5
```

输入后查看在命令行的运行结果

![](https://i.imgur.com/BhT4Pz2.png)

接下来用cat命令并展示结果（部分）
```linux
	bin/hdfs dfs -cat /output/invertedIndex/5/*
```
![](https://i.imgur.com/Rz8tn3d.png)

2.2 实验结果分析

成功地将词语和url相对应，处理掉了所有含数字的词组，相当于做了针对数字的停词。针对有些标题中含大段空白的问题，因为不方便分词，于是增加了分词后字符数组的长度等于6的片段，若不这样做会导致部分标题被当做url

2.3 实验不足分析

没有将停词文件加入

上述即为实验结果，相关代码及文件同时上传至github