package wordcount;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URI;
import  java.lang.String;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Scanner;
//import java.util.StringTokenizer;


import org.wltea.analyzer.core.IKSegmenter;
import org.wltea.analyzer.core.Lexeme;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.WritableComparable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
//import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.Counter;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.util.StringUtils;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.hadoop.mapreduce.lib.map.InverseMapper;
//import org.wltea.analyzer.core.Lexeme;

public class wordcount2 {
	public static int wc;
	public static class TokenizerMapper
       extends Mapper<Object, Text, Text, IntWritable>{

    static enum CountersEnum { INPUT_WORDS }

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    private boolean caseSensitive;
    private Set<String> patternsToSkip = new HashSet<String>();

    private Configuration conf;
    private BufferedReader fis;
    
    String[] positive_p = new String[783];
   	String[] neutral_p = new String[783];
   	String[] negative_p = new String[783];
   	double[] positivep=new double[783];
   	double[] neutralp=new double[783];
   	double[] negativep=new double[783];
   	
    private BufferedReader br;
    String[] featureword = new String[783];
  
    @Override
    public void setup(Context context) throws IOException,
        InterruptedException {
      conf = context.getConfiguration();
      caseSensitive = conf.getBoolean("wordcount.case.sensitive", true);
      if (conf.getBoolean("wordcount.skip.patterns", false)) {
        URI[] patternsURIs = Job.getInstance(conf).getCacheFiles();
        for (URI patternsURI : patternsURIs) {
          Path patternsPath = new Path(patternsURI.getPath());
          String patternsFileName = patternsPath.getName().toString();
          parseSkipFile(patternsFileName);
        }
      }
      try {
    	  BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(new File("/home/huben/feature.txt")), "UTF-8"));
    	  String lineTxt = null;
    	  int get_line=0;
    	  while ((lineTxt = br.readLine()) != null) {
    		  //get_idf_words_information[get_line] = new String(lineTxt);
    		  get_line++;
    		  String[] temp = lineTxt.split("\t");
    		  featureword[get_line]=temp[1].substring(temp[1].indexOf("'")+1,temp[1].lastIndexOf("'"));
    		  positive_p[get_line]=temp[2].substring(temp[1].indexOf("'")+1,temp[1].lastIndexOf("'"));
    		  neutral_p[get_line]=temp[3].substring(temp[1].indexOf("'")+1,temp[1].lastIndexOf("'"));
    		  negative_p[get_line]=temp[4].substring(temp[1].indexOf("'")+1,temp[1].lastIndexOf("'"));
    		  positivep[get_line]= Double.valueOf(positive_p[get_line]);
    		  neutralp[get_line]=Double.valueOf(neutral_p[get_line]);
    		  negativep[get_line]=Double.valueOf(negative_p[get_line]);
    		  
    		  System.out.println("0:"+negativep[get_line]);
    		  //if (temp.length < 6)   
    		  //return;
    		  //String values=temp[4];
    		  System.out.println("1:"+featureword[get_line]);
    		  System.out.println("2:"+positive_p[get_line]);
    	  }
    	  br.close();
  } catch (Exception e) {
      System.err.println("read errors :" + e);
  	}
    }

    private void parseSkipFile(String fileName) {
      try {
        fis = new BufferedReader(new FileReader(fileName));
        String pattern = null;
        while ((pattern = fis.readLine()) != null) {
          patternsToSkip.add(pattern);
        }
      } catch (IOException ioe) {
        System.err.println("Caught exception while parsing the cached file '"
            + StringUtils.stringifyException(ioe));
      }
    }

    @Override
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
	     String line = (caseSensitive) ?
	         value.toString() : value.toString().toLowerCase();
	     for (String pattern : patternsToSkip) {
	    	 line = line.replaceAll(pattern, "");
	     }
	     double positive=1;
	     double neutral=1;
	     double negative=1;
	     if ( line == null || line.equals("") )   
	    	 return;  
//	     String[] temp = line.split("\t");
//	     if (temp.length != 2)   
//	    	 return;
	     
	     
	     
	     //String values=temp[4];
	     //System.out.println("1:"+values);
	     //System.out.println("2:"+temp[5]);
	      
        //byte[]bt=values.getBytes();
	     
	     
	    byte[]bt=line.getBytes();
        InputStream ip=new ByteArrayInputStream(bt);
        Reader read=new InputStreamReader(ip);
        IKSegmenter iks=new IKSegmenter(read,true);
        Lexeme t;
        while((t=iks.next())!=null)
	    {
	    	  word.set(t.getLexemeText());
	    	  context.write(word, one);
	    	  Counter counter = context.getCounter(CountersEnum.class.getName(),
	    	  CountersEnum.INPUT_WORDS.toString());
	    	  counter.increment(1);
	     }
//        
//      StringTokenizer itr = new StringTokenizer(line);
//      while (itr.hasMoreTokens()) {
//        word.set(itr.nextToken());
//        context.write(word, one);
//        System.out.println("word:"+word);
//        System.out.println("one:"+one);
//        Counter counter = context.getCounter(CountersEnum.class.getName(),
//            CountersEnum.INPUT_WORDS.toString());
//        counter.increment(1);
//      }
    }
  }

  private static class IntWritableDecreasingComparator extends IntWritable.Comparator {
      public int compare(WritableComparable a, WritableComparable b) {
        return -super.compare(a, b);
      }
      
      public int compare(byte[] b1, int s1, int l1, byte[] b2, int s2, int l2) {
          return -super.compare(b1, s1, l1, b2, s2, l2);
      }
  }
  
  public static class IntSumReducer
       extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable result = new IntWritable();
    
    public void reduce(Text key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
        //System.out.println(val.get());
      }
      Text key1=new Text();
      key1 =key;
      if(sum>=wc && key1.toString().length()>=2)
      {result.set(sum);
      context.write(key, result);
      }
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    GenericOptionsParser optionParser = new GenericOptionsParser(conf, args);
    String[] remainingArgs = optionParser.getRemainingArgs();
    if (!(remainingArgs.length != 2 || remainingArgs.length != 4)) {
      System.err.println("Usage: wordcount <in> <out> [-skip skipPatternFile]");
      System.exit(2);
    }
    
    Scanner sc = new Scanner(System.in); 
    System.out.println("请输入词频k："); 
    int wc = sc.nextInt();
    wordcount2.wc=wc;
    Job job = Job.getInstance(conf, "word count");
    job.setJarByClass(wordcount2.class);
    job.setMapperClass(TokenizerMapper.class);
    
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    List<String> otherArgs = new ArrayList<String>();
    for (int i=0; i < remainingArgs.length; ++i) {
      if ("-skip".equals(remainingArgs[i])) {
        job.addCacheFile(new Path(remainingArgs[++i]).toUri());
        job.getConfiguration().setBoolean("wordcount.skip.patterns", true);
      } else {
        otherArgs.add(remainingArgs[i]);
      }
    }
    FileInputFormat.addInputPath(job, new Path(otherArgs.get(0)));
    //FileOutputFormat.setOutputPath(job, new Path(otherArgs.get(1)));
    
    
    FileOutputFormat.setOutputPath(job, new Path("output/wordcount/te2"));//先将词频统计任务的输出结果写到临时目  
    //录中, 下一个排序任务以临时目录为输入目录。  
    job.setOutputFormatClass(SequenceFileOutputFormat.class);  
    if(job.waitForCompletion(true))  
    {  
        Job sortJob = new Job(conf, "sort");  
        sortJob.setJarByClass(wordcount2.class);  

        FileInputFormat.addInputPath(sortJob, new Path("output/wordcount/te2"));  
        sortJob.setInputFormatClass(SequenceFileInputFormat.class);  

        /*InverseMapper由hadoop库提供，作用是实现map()之后的数据对的key和value交换*/  
        sortJob.setMapperClass(InverseMapper.class);  
        /*将 Reducer 的个数限定为1, 最终输出的结果文件就是一个。*/  
        sortJob.setNumReduceTasks(1);   
        FileOutputFormat.setOutputPath(sortJob, new Path(otherArgs.get(1)));  

        sortJob.setOutputKeyClass(IntWritable.class);  
        sortJob.setOutputValueClass(Text.class);  
        /*Hadoop 默认对 IntWritable 按升序排序，而我们需要的是按降序排列。 
        * 因此我们实现了一个 IntWritableDecreasingComparator 类,　 
        * 并指定使用这个自定义的 Comparator 类对输出结果中的 key (词频)进行排序*/  
        sortJob.setSortComparatorClass(IntWritableDecreasingComparator.class);  
        System.exit(sortJob.waitForCompletion(true) ? 0 : 1); 
    }  

  }
    
  
    //System.exit(job.waitForCompletion(true) ? 0 : 1);
  //}
}
