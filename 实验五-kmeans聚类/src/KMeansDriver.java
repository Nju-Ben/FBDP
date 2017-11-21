import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


/**
 * ��������KMeans���еĹ���
 * @author KING
 *
 */
public class KMeansDriver {
	private int k;
	private int iterationNum;
	private String sourcePath;
	private String outputPath;
	
	private Configuration conf;
	
	public KMeansDriver(int k, int iterationNum, String sourcePath, String outputPath, Configuration conf){
		this.k = k;
		this.iterationNum = iterationNum;
		this.sourcePath = sourcePath;
		this.outputPath = outputPath;
		this.conf = conf;
	}
	
	public void clusterCenterJob() throws IOException, InterruptedException, ClassNotFoundException{
		for(int i = 0;i < iterationNum; i++){
			Job clusterCenterJob =Job.getInstance();
			clusterCenterJob .setJobName("clusterCenterJob" + i);
			clusterCenterJob .setJarByClass(KMeans.class);
			
			clusterCenterJob.getConfiguration().set("clusterPath", outputPath + "/cluster-" + i +"/");

			clusterCenterJob.setMapperClass(KMeans.KMeansMapper.class);
			clusterCenterJob.setMapOutputKeyClass(IntWritable.class);
			clusterCenterJob.setMapOutputValueClass(Cluster.class);

			clusterCenterJob.setCombinerClass(KMeans.KMeansCombiner.class);
			clusterCenterJob.setReducerClass(KMeans.KMeansReducer .class);
			clusterCenterJob.setOutputKeyClass(NullWritable.class);
			clusterCenterJob.setOutputValueClass(Cluster.class);

			FileInputFormat.addInputPath(clusterCenterJob, new Path(sourcePath));
			FileOutputFormat.setOutputPath(clusterCenterJob, new Path(outputPath + "/cluster-" + (i + 1) +"/"));
			
			clusterCenterJob.waitForCompletion(true);
			System.out.println("finished!");
		}
	}
	
	public void KMeansClusterJod() throws IOException, InterruptedException, ClassNotFoundException{
		//Job kMeansClusterJob = new Job();
		Job kMeansClusterJob = Job.getInstance();
		kMeansClusterJob.setJobName("KMeansClusterJob");
		kMeansClusterJob.setJarByClass(KMeansCluster.class);
		
		kMeansClusterJob.getConfiguration().set("clusterPath", outputPath + "/cluster-" + (iterationNum - 1) +"/");

		kMeansClusterJob.setMapperClass(KMeansCluster.KMeansClusterMapper.class);
		kMeansClusterJob.setMapOutputKeyClass(Text.class);
		kMeansClusterJob.setMapOutputValueClass(IntWritable.class);

		kMeansClusterJob.setNumReduceTasks(0);

		FileInputFormat.addInputPath(kMeansClusterJob, new Path(sourcePath));
		FileOutputFormat.setOutputPath(kMeansClusterJob, new Path(outputPath + "/clusteredInstances" + "/"));
		
		kMeansClusterJob.waitForCompletion(true);
		System.out.println("finished!");
	}
	
	public void generateInitialCluster(){
		RandomClusterGenerator generator = new RandomClusterGenerator(conf, sourcePath, k);
		generator.generateInitialCluster(outputPath + "/");
	}
	
	public static void main(String[] args) throws IOException, InterruptedException, ClassNotFoundException{
		System.out.println("start");
		Configuration conf = new Configuration();
		int k = Integer.parseInt(args[0]);
		int iterationNum = Integer.parseInt(args[1]);
		String sourcePath = args[2];
		String outputPath = args[3];
		KMeansDriver driver = new KMeansDriver(k, iterationNum, sourcePath, outputPath, conf);
		driver.generateInitialCluster();
		System.out.println("initial cluster finished");
		driver.clusterCenterJob();
		driver.KMeansClusterJod();
	}
}
