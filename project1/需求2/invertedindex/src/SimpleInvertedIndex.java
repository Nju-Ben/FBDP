
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.Iterator;
//import java.util.StringTokenizer;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
//import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
//import org.apache.hadoop.mapreduce.Counter;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
//import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.wltea.analyzer.core.IKSegmenter;
import org.wltea.analyzer.core.Lexeme;
public class SimpleInvertedIndex {
  /** 对文本进行处理，得到<word,filename#offset>格式的键值对输出，从而得到一个单词在文档中出现的位置 **/
  public static class InvertedIndexMapper extends
      Mapper<Object, Text, Text, Text> {
	  
    public void map(Object key, Text value, Context context)
        throws IOException, InterruptedException {
    	String line=value.toString();
    	if (line == null || line.equals("") )   
            return;  
    	String[] temp = line.split("\t");
    	if (temp.length != 6)   
            return;
    	String values=temp[4];
    	String urls=temp[5];
    	System.out.println("1:"+values);
    	System.out.println("2:"+urls);
        byte[]bt=values.getBytes();
        InputStream ip=new ByteArrayInputStream(bt);
        Reader read=new InputStreamReader(ip);
        IKSegmenter iks=new IKSegmenter(read,true);
        Lexeme t;
        Text word1 = new Text();
        Text word2 = new Text();
        while((t=iks.next())!=null)
 	    {
 	    	  word1.set(t.getLexemeText());
 	    	  word2.set(urls);
 	    	  context.write(word1,word2);
 	     }
//      FileSplit fileSplit = (FileSplit) context.getInputSplit();
//      String fileName = fileSplit.getPath().getName(); // 得到文件名
//      Text word = new Text();
//      Text fileName_lineOffset = new Text(fileName + "#" + key.toString());
//      StringTokenizer itr = new StringTokenizer(value.toString());
//      for (; itr.hasMoreTokens();) {
//        word.set(itr.nextToken());
//        context.write(word, fileName_lineOffset);
//      }
    }
  }
  
  public static boolean isContainNumber(String company) {

      Pattern p = Pattern.compile("[0-9]");
      Matcher m = p.matcher(company);
      if (m.find()) {
          return true;
      }
      return false;
  }

  /** 从Mapper处得到的内容，根据相同key值，进行累加处理，输出该单词所有出现的文档位置 **/
  public static class InvertedIndexReducer extends
      Reducer<Text, Text, Text, Text> {
    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException 
    { Iterator<Text> it = values.iterator();
      StringBuilder all = new StringBuilder();
      if (it.hasNext())
        all.append(it.next().toString());
      for (; it.hasNext();) {
        all.append(";");
        all.append(it.next().toString());
      }
      Text key1=new Text();
      key1=key;
      String x=key1.toString();
      if(x.length()>=2 && isContainNumber(x)==false)
      {
      context.write(key, new Text(all.toString()));
    } }// 最终输出键值对示例：("fish", "doc1#0; doc1#8;doc2#0;doc2#8 ")
  }

  public static void main(String[] args) throws Exception {
      Configuration conf = new Configuration();
      Job job = new Job(conf, "invert index");
      job.setJarByClass(SimpleInvertedIndex.class);
      job.setInputFormatClass(TextInputFormat.class);
      job.setMapperClass(InvertedIndexMapper.class);
      job.setReducerClass(InvertedIndexReducer.class);
      job.setOutputKeyClass(Text.class);
      job.setOutputValueClass(Text.class);
      FileInputFormat.addInputPath(job, new Path(args[0]));
      FileOutputFormat.setOutputPath(job, new Path(args[1]));
      System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
