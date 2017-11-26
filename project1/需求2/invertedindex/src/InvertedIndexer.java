
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.URI;
import java.util.List;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.ArrayList;
import java.util.TreeSet;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.RecordReader;
import org.apache.hadoop.mapreduce.lib.input.LineRecordReader;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import org.apache.hadoop.mapreduce.TaskAttemptContext;
import org.apache.hadoop.mapreduce.lib.partition.HashPartitioner;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class InvertedIndexer {
  /** 自定义FileInputFormat **/
  public static class FileNameInputFormat extends FileInputFormat<Text, Text> {
    @Override
    public RecordReader<Text, Text> createRecordReader(InputSplit split,
        TaskAttemptContext context) throws IOException, InterruptedException {
      FileNameRecordReader fnrr = new FileNameRecordReader();
        fnrr.initialize(split, context);
      return fnrr;
    }
  }

  /** 自定义RecordReader **/
  public static class FileNameRecordReader extends RecordReader<Text, Text> {
    String fileName;
    LineRecordReader lrr = new LineRecordReader();

    @Override
    public Text getCurrentKey() throws IOException, InterruptedException {
      return new Text(fileName);
    }

    @Override
    public Text getCurrentValue() throws IOException, InterruptedException {
      return lrr.getCurrentValue();
    }

    @Override
    public void initialize(InputSplit arg0, TaskAttemptContext arg1)
        throws IOException, InterruptedException {
      lrr.initialize(arg0, arg1);
      fileName = ((FileSplit) arg0).getPath().getName();
    }

    public void close() throws IOException {
        lrr.close();
    }

    public boolean nextKeyValue() throws IOException, InterruptedException {
      return lrr.nextKeyValue();
    }

    public float getProgress() throws IOException, InterruptedException {
      return lrr.getProgress();
    }
  }


  public static class InvertedIndexMapper extends
      Mapper<Text, Text, Text, IntWritable> {
    private Set<String> stopwords;
    private Path[] localFiles;
    private String pattern = "[^\\w]"; // 正则表达式，代表不是0-9, a-z, A-Z,的所有其它字

    public void setup(Context context) throws IOException, InterruptedException {
      stopwords = new TreeSet<String>();
      Configuration conf = context.getConfiguration();
      localFiles = DistributedCache.getLocalCacheFiles(conf); // 获得停词表
      for (int i = 0; i < localFiles.length; i++) {
        String line;
        BufferedReader br =
            new BufferedReader(new FileReader(localFiles[i].toString()));
        while ((line = br.readLine()) != null) {
          StringTokenizer itr = new StringTokenizer(line);
          while (itr.hasMoreTokens()) {
            stopwords.add(itr.nextToken());
          }
        }
      }
    }

    protected void map(Text key, Text value, Context context)
        throws IOException, InterruptedException {
      // map()函数这里使用自定义的FileNameRecordReader
      // 得到key: filename文件名; value: line_string每一行的内容
      String temp = new String();
      String line = value.toString().toLowerCase();
      line = line.replaceAll(pattern, " "); // 将非0-9, a-z, A-Z的字符替换为空格
      StringTokenizer itr = new StringTokenizer(line);
      for (; itr.hasMoreTokens();) {
        temp = itr.nextToken();
        if (!stopwords.contains(temp)) {
          Text word = new Text();
          word.set(temp + "#" + key);
          context.write(word, new IntWritable(1));
        }
      }
    }
  }

  /** 使用Combiner将Mapper的输出结果中value部分的词频进行统计 **/
  public static class SumCombiner extends
      Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }

  /** 自定义HashPartitioner，保证 <term, docid>格式的key值按照term分发给Reducer **/
  public static class NewPartitioner extends HashPartitioner<Text, IntWritable> {
    public int getPartition(Text key, IntWritable value, int numReduceTasks) {
      String term = new String();
      term = key.toString().split("#")[0]; // <term#docid>=>term
      return super.getPartition(new Text(term), value, numReduceTasks);
    }
  }

  public static class InvertedIndexReducer extends
      Reducer<Text, IntWritable, Text, Text> {
    private Text word1 = new Text();
    private Text word2 = new Text();
    String temp = new String();
    static Text CurrentItem = new Text(" ");
    static List<String> postingList = new ArrayList<String>();

    public void reduce(Text key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
      int sum = 0;
      word1.set(key.toString().split("#")[0]);
      temp = key.toString().split("#")[1];
      for (IntWritable val : values) {
        sum += val.get();
      }
      word2.set("<" + temp + "," + sum + ">");
      if (!CurrentItem.equals(word1) && !CurrentItem.equals(" ")) {
        StringBuilder out = new StringBuilder();
        long count = 0;
        for (String p : postingList) {
          out.append(p);
          out.append(";");
          count =
              count
                  + Long.parseLong(p.substring(p.indexOf(",") + 1,
                      p.indexOf(">")));
        }
        out.append("<total," + count + ">.");
        if (count > 0)
          context.write(CurrentItem, new Text(out.toString()));
        postingList = new ArrayList<String>();
      }
      CurrentItem = new Text(word1);
      postingList.add(word2.toString()); // 不断向postingList也就是文档名称中添加词表
    }

    // cleanup 一般情况默认为空，有了cleanup不会遗漏最后一个单词的情况

    public void cleanup(Context context) throws IOException,
        InterruptedException {
      StringBuilder out = new StringBuilder();
      long count = 0;
      for (String p : postingList) {
        out.append(p);
        out.append(";");
        count =
            count
                + Long
                    .parseLong(p.substring(p.indexOf(",") + 1, p.indexOf(">")));
      }
      out.append("<total," + count + ">.");
      if (count > 0)
        context.write(CurrentItem, new Text(out.toString()));
    }

  }

  public static void main(String[] args) throws Exception {
      Configuration conf = new Configuration();
      DistributedCache.addCacheFile(new URI(
        "hdfs://master01:54310/user/2014st08/stop-words.txt"), conf);// 设置停词列表文档作为当前作业的缓存文件
    Job job = new Job(conf, "inverted index");
      job.setJarByClass(InvertedIndexer.class);
      job.setInputFormatClass(FileNameInputFormat.class);
      job.setMapperClass(InvertedIndexMapper.class);
      job.setCombinerClass(SumCombiner.class);
      job.setReducerClass(InvertedIndexReducer.class);
      job.setPartitionerClass(NewPartitioner.class);
      job.setMapOutputKeyClass(Text.class);
      job.setMapOutputValueClass(IntWritable.class);
      job.setOutputKeyClass(Text.class);
      job.setOutputValueClass(Text.class);
      FileInputFormat.addInputPath(job, new Path(args[0]));
      FileOutputFormat.setOutputPath(job, new Path(args[1]));
      System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}

