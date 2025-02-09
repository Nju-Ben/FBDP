#_*_ coding: utf-8 _*_

import pandas as pd
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt

#读取上证指数数据，计算每一个月的指数收益率        
df2=pd.read_csv('G:\\2.csv',engine='python')
df2.drop(0,inplace=True)
basetime=df2['Idxtrd01'][1]
datetime= time.strptime(basetime, "%Y/%m/%d")
df2['monthdiff']=0
for i in range(1,len(df2)):
    datetimenew=time.strptime(df2.iloc[i,1], "%Y/%m/%d")
    df2.iloc[i,5]=(datetimenew.tm_year-datetime.tm_year)*12+datetimenew.tm_mon-datetime.tm_mon
index=[]
for i in range(0,72):
    x=df2[df2.monthdiff==i]
    d2=x.head(1)
    d3=x.tail(1)
    x1=float(d2.iloc[0,2])
    x2=float(d3.iloc[0,3])
    x3=(x2-x1)/x1
    index.append(x3)
print(index)

#选出赢家组合和输家组合和输家组合的函数
df1=pd.read_csv('G:\\1.csv',engine='python')
def loser(df1,monthcount,index):
    d1=df1
    d1['month0']=(d1[d1.columns[monthcount+1]]-d1[d1.columns[monthcount]])/d1[d1.columns[monthcount]]
    d1['sumprofit']=d1['month0']-index[monthcount-4]
    d1=d1.dropna()
    d1=d1.sort_values(by='sumprofit')
    num=len(d1)
    df2=d1.head(int(num/10))
    return df2

def winner(df1,monthcount,index):
    d1=df1
    d1['month0']=(d1[d1.columns[monthcount+1]]-d1[d1.columns[monthcount]])/d1[d1.columns[monthcount]]
    d1['sumprofit']=d1['month0']-index[monthcount-4]
    d1=d1.dropna()
    d1=d1.sort_values(by='sumprofit')
    num=len(d1)
    df2=d1.tail(int(num/10))
    return df2

x=[]
for i in range(0,48):
    x.append(i+1)
x1=[]
x2=[]
x3=[]
avg1=0
avg2=0
for i in range(0,48):
    df2=winner(df1,i+4,index)
    df3=loser(df1,i+4,index)
    
    df2['ckmonth']=(df2[df2.columns[i+6]]-df2[df2.columns[i+5]])/df2[df2.columns[i+5]]
    df3['ckmonth']=(df3[df3.columns[i+6]]-df3[df3.columns[i+5]])/df3[df3.columns[i+5]] 
    df2['profit']=df2['ckmonth']-index[i+1]
    df3['profit']=df3['ckmonth']-index[i+1]
    avg1=avg1+df2['profit'].mean()
    avg2=avg2+df3['profit'].mean()

    x1.append(avg1)
    x2.append(avg2)
        #x3.append(sum1-sum2)
#plt.plot(x,x1,Color='red')
#plt.plot(x,x2,Color='green')
for i in range(len(x1)):
     x3.append(x2[i]-x1[i])
plt.plot(x,x3)
plt.show()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          