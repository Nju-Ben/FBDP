package hbaseoperation;
import java.io.IOException;  

import org.apache.hadoop.conf.Configuration;  
import org.apache.hadoop.hbase.HBaseConfiguration;  
import org.apache.hadoop.hbase.HColumnDescriptor;  
import org.apache.hadoop.hbase.HTableDescriptor;  
import org.apache.hadoop.hbase.KeyValue;  
import org.apache.hadoop.hbase.client.Delete;  
import org.apache.hadoop.hbase.client.Get;  
import org.apache.hadoop.hbase.client.HBaseAdmin;  
import org.apache.hadoop.hbase.client.HTable;  
//import org.apache.hadoop.hbase.client.HTablePool;  
import org.apache.hadoop.hbase.client.Put;  
import org.apache.hadoop.hbase.client.Result;  
import org.apache.hadoop.hbase.client.ResultScanner;  
import org.apache.hadoop.hbase.client.Scan;  
import org.apache.hadoop.hbase.util.Bytes;  
  
@SuppressWarnings("unused")
public class hbasecreate {  
    // 声明静态配置  
    static Configuration conf = null;  
    static {  
        conf = HBaseConfiguration.create();  
        conf.set("hbase.zookeeper.quorum", "localhost");  
    }  
  
 //创建表
    public static void creatTable(String tableName, String[] family)  
            throws Exception {  
		HBaseAdmin admin = new HBaseAdmin(conf);
    	//Connection conn = ConnectionFactory.createConnection( HBaseConfiguration.create() );
    	//Admin admin = conn.getAdmin();
        HTableDescriptor desc = new HTableDescriptor(tableName);  
        for (int i = 0; i < family.length; i++) {  
            desc.addFamily(new HColumnDescriptor(family[i]));  
        }  
        if (admin.tableExists(tableName)) {  
            System.out.println("table Exists!");  
            System.exit(0);  
        } else {  
            admin.createTable(desc);  
            System.out.println("create table Success!");  
        }  
    }  
  
      
      //为表添加数据（适合知道有多少列族的固定表）  
    
    public static void addData(String rowKey, String tableName,  
    String[] column1, String[] value1, String[] column2, String[] value2,
    String[] column3, String[] value3)  
    throws IOException {  
        Put put = new Put(Bytes.toBytes(rowKey));// 设置rowkey  
        HTable table = new HTable(conf, Bytes.toBytes(tableName));
        HColumnDescriptor[] columnFamilies = table.getTableDescriptor()
               .getColumnFamilies();  
  
        for (int i = 0; i < columnFamilies.length; i++) {  
            String familyName = columnFamilies[i].getNameAsString(); 
            	if (familyName.equals("Description")) {
                for (int j = 0; j < column1.length; j++) {  
                    put.add(Bytes.toBytes(familyName),  
                            Bytes.toBytes(column1[j]), Bytes.toBytes(value1[j]));  
                }  
            }  
 
            if (familyName.equals("Courses")) {
                for (int j = 0; j < column2.length; j++) {  
                    put.add(Bytes.toBytes(familyName),  
                            Bytes.toBytes(column2[j]), Bytes.toBytes(value2[j]));  
                }  
            } 
            
            if (familyName.equals("Home")) { 
                for (int j = 0; j < column3.length; j++) {  
                    put.add(Bytes.toBytes(familyName),  
                            Bytes.toBytes(column3[j]), Bytes.toBytes(value3[j]));  
                }  
            } 
        }  
        table.put(put);  
        System.out.println("add data Success!");  
    }  
    
public static void main(String[] args) throws Exception {  
//		  
//        // 创建表  
        String tableName = "students";  
        String[] family = { "Description", "Courses","Home"};  
        creatTable(tableName, family);  
  
        String[] column1 = { "Name", "Height"};
        String[] column2 = { "Chinese", "Math","Physics"};
        String[] column3 = {"Province"};
        
        String[] value11= {"Li lei","176"};
        String[] value21= {"Han Meimei","183"};
        String[] value31= {"Xiao Ming","162"};
        
        String[] value12= {"80","90","95"};
        String[] value22= {"88","77","66"};
        String[] value32= {"90","90","90"};
        
        String[] value13= {"Zhejiang"};
        String[] value23= {"Beijing"};
        String[] value33= {"Shanghai"};
        
        addData("001", "students", column1, value11, column2, value12,column3,value13);  
        addData("002", "students", column1, value21, column2, value22,column3,value23);  
        addData("003", "students", column1, value31, column2, value32,column3,value33);  
  
        // 删除表  
        //deleteTable("students");  
    }  
} 
