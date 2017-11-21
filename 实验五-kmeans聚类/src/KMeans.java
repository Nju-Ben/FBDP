import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

import king.Utils.Distance;
import king.Utils.EuclideanDistance;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * KMeans�����㷨
 * @author KING
 *
 */
public class KMeans {
	public static class KMeansMapper extends Mapper<LongWritable,Text,IntWritable,Cluster>{
		private ArrayList<Cluster> kClusters = new ArrayList<Cluster>();
		
		/**
		 * ����Ŀǰ�Ĵ���Ϣ
		 */
		@Override
		protected void setup(Context context) throws IOException,InterruptedException{
			super.setup(context);
			FileSystem fs = FileSystem.get(context.getConfiguration());
	        FileStatus[] fileList = fs.listStatus(new Path(context.getConfiguration().get("clusterPath")));
	        BufferedReader in = null;
			FSDataInputStream fsi = null;
			String line = null;
	        for(int i = 0; i < fileList.length; i++){
	        	if(!fileList[i].isDirectory()){
	        		fsi = fs.open(fileList[i].getPath());
					in = new BufferedReader(new InputStreamReader(fsi,"UTF-8"));
					while((line = in.readLine()) != null){
						System.out.println("read a line:" + line);
						Cluster cluster = new Cluster(line);
						cluster.setNumOfPoints(0);
						kClusters.add(cluster);
					}
	        	}
	        }
	        in.close();
	        fsi.close();
		}
		
		/**
		 * ��ȡһ��Ȼ��Ѱ����õ�����Ĵط���(clusterID,instance)
		 */
		@Override
		public void map(LongWritable key, Text value, Context context)throws 
		IOException, InterruptedException{
			Instance instance = new Instance(value.toString());
			int id;
			try {
				id = getNearest(instance);
				if(id == -1)
					throw new InterruptedException("id == -1");
				else{
					Cluster cluster = new Cluster(id, instance);
					cluster.setNumOfPoints(1);
					System.out.println("cluster that i emit is:" + cluster.toString());
					context.write(new IntWritable(id), cluster);
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		/**
		 * ������instance����Ĵص�ID
		 * @param instance
		 * @return
		 * @throws Exception 
		 */
		public int getNearest(Instance instance) throws Exception{
			int id = -1;
			double distance = Double.MAX_VALUE;
			Distance<Double> distanceMeasure = new EuclideanDistance<Double>();
			double newDis = 0.0;
			for(Cluster cluster : kClusters){	
				newDis = distanceMeasure.getDistance(cluster.getCenter().getValue()
						, instance.getValue());
				if(newDis < distance){
					id = cluster.getClusterID();
					distance = newDis;
				}
			}
			return id;
		}
		
		public Cluster getClusterByID(int id){
			for(Cluster cluster : kClusters){
				if(cluster.getClusterID() == id)
					return cluster;
			}
			return null;
		}
	}
	
	public static class KMeansCombiner extends Reducer<IntWritable,Cluster,IntWritable,Cluster>{
		public void reduce(IntWritable key, Iterable<Cluster> value, Context context)throws 
		IOException, InterruptedException{
			Instance instance = new Instance();
			int numOfPoints = 0;
			for(Cluster cluster : value){
				numOfPoints += cluster.getNumOfPoints();
				System.out.println("cluster is:" + cluster.toString());
				instance = instance.add(cluster.getCenter().multiply(cluster.getNumOfPoints()));
			}
			Cluster cluster = new Cluster(key.get(),instance.divide(numOfPoints));
			cluster.setNumOfPoints(numOfPoints);
			System.out.println("combiner emit cluster:" + cluster.toString());
			context.write(key, cluster);
		}
	}
	
	
	
	public static class KMeansReducer extends Reducer<IntWritable,Cluster,NullWritable,Cluster>{
		public void reduce(IntWritable key, Iterable<Cluster> value, Context context)throws 
		IOException, InterruptedException{
			Instance instance = new Instance();
			int numOfPoints = 0;
			for(Cluster cluster : value){
				numOfPoints += cluster.getNumOfPoints();
				instance = instance.add(cluster.getCenter().multiply(cluster.getNumOfPoints()));
			}
			Cluster cluster = new Cluster(key.get(),instance.divide(numOfPoints));
			cluster.setNumOfPoints(numOfPoints);
			context.write(NullWritable.get(), cluster);
		}
	}
}
