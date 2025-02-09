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
    for i in range(0,2):
        d1['month'+str(i)]=(d1[d1.columns[monthcount+1+i]]-d1[d1.columns[monthcount+i]])/d1[d1.columns[monthcount+i]]
    #df1['sumprofit']=df1['month0']-index[0]+df1['month1']-index[1]+df1['month2']-index[2]
    d1['sumprofit']=d1['month0']-index[monthcount-4]+d1['month1']-index[monthcount-3]
    d1=d1.dropna()
    print(d1)
    d1=d1.sort_values(by='sumprofit')
    num=len(d1)
    df2=d1.head(int(num/10))
    return df2

def winner(df1,monthcount,index):
    d1=df1
    for i in range(0,2):
        d1['month'+str(i)]=(d1[d1.columns[monthcount+1+i]]-d1[d1.columns[monthcount+i]])/d1[d1.columns[monthcount+i]]
    #df1['sumprofit']=df1['month0']-index[0]+df1['month1']-index[1]+df1['month2']-index[2]
    d1['sumprofit']=d1['month0']-index[monthcount-4]+d1['month1']-index[monthcount-3]
    d1=d1.dropna()
    d1=d1.sort_values(by='sumprofit')
    num=len(d1)
    df2=d1.tail(int(num/10))
    return df2
#计算检验期的超额收益率 检验期为2010-7 - 2010-12 6个月
# sum1=0
# cr1=[]
# cr2=[]
# avg1=1
# avg2=1
# sum2=0
x=[]
for i in range(0,24):
    x.append(i+1)
x1=[]
x2=[]
x3=[]
sum1=0
sum2=0
sum3=0
for i in range(0,48,4):
    df2=winner(df1,i+4,index)
    df3=loser(df1,i+4,index)
    for j in range(0,2):
        df2['ckmonth'+str(j)]=(df2[df2.columns[i+7+j]]-df2[df2.columns[i+j+6]])/df2[df2.columns[i+j+6]]
        df3['ckmonth'+str(j)]=(df3[df3.columns[i+7+j]]-df3[df3.columns[i+j+6]])/df3[df3.columns[i+j+6]] 
#     for i in range(0,3):
#     df4['ckmonth'+str(i)]=(df4[df4.columns[8+i]]-df4[df4.columns[7+i]])/df4[df4.columns[7+i]]
#     df5['ckmonth'+str(i)]=(df5[df5.columns[8+i]]-df5[df4.columns[7+i]])/df5[df4.columns[7+i]]
    for k in range(0,2):
        df2['profit'+str(k)]=df2['ckmonth'+str(k)]-index[k+i+2]
        df3['profit'+str(k)]=df3['ckmonth'+str(k)]-index[k+i+2]
    #avg1=avg1+df4['profit'+str(i)].mean()
    #avg2=avg2+df5['profit'+str(i)].mean()
    #avg1=avg1*(1+df4['profit'+str(i)].mean())
    #avg2=avg2*(1+df5['profit'+str(i)].mean())
        sum1=sum1+df2['profit'+str(k)].sum()
        sum2=sum2+df3['profit'+str(k)].sum()
        #sum3=sum3+sum1-sum2
        #x3.append(sum3)
        x1.append(sum1)
        x2.append(sum2)
        #x3.append(sum1-sum2)
#plt.plot(x,x1,Color='red')
#plt.plot(x,x2,Color='green')
for i in range(len(x1)):
     x3.append(x2[i]-x1[i])
plt.plot(x,x3)
plt.show()
    #cr1.append(avg1)
    #cr2.append(avg2)
# x=[]
# cr3=[]
# for i in range(0,6):
#     x.append(i+1)
# for i in range(0,6):
#     cr3.append(cr1[i]-cr2[i])
# print(cr3)





# for i in range(0,3):
#     df4['ckmonth'+str(i)]=(df4[df4.columns[8+i]]-df4[df4.columns[7+i]])/df4[df4.columns[7+i]]
#     df5['ckmonth'+str(i)]=(df5[df5.columns[8+i]]-df5[df4.columns[7+i]])/df5[df4.columns[7+i]]
# for i in range(0,3):
#     df4['profit'+str(i)]=df4['ckmonth'+str(i)]-index[3+i]
#     df5['profit'+str(i)]=df5['ckmonth'+str(i)]-index[3+i]
    #avg1=avg1+df4['profit'+str(i)].mean()
    #avg2=avg2+df5['profit'+str(i)].mean()
    #avg1=avg1*(1+df4['profit'+str(i)].mean())
    #avg2=avg2*(1+df5['profit'+str(i)].mean())
    
    
#     sum1=sum1+df4['profit'+str(i)].sum()
#     sum2=sum2+df5['profit'+str(i)].sum()
#     cr1.append(sum1)
#     cr2.append(sum2)
#     
    
    #cr1.append(avg1)
    #cr2.append(avg2)
# x=[]
# cr3=[]
# for i in range(0,6):
#     x.append(i+1)
# for i in range(0,6):
#     cr3.append(cr1[i]-cr2[i])
# print(cr3)


# y=[]
# base=2010.03
# for i in range(0,36):
#     if (base-int(base))<0.11:
#         base=base+0.01
#     else:
#         base=int(base)
#         base=base+1
#         base=base+0.01
#     y.append(base)
# print(y)
# y=y[4:16]
# print(y)
#plt.plot(x,cr1)
#plt.plot(x,cr1,label=u'输家组合',x,cr2,label=u'赢家组合')
#plt.plot(x,cr1,label=u'loser')
#plt.plot(x,cr2,label=u'winner')
#plt.plot(x,cr3)
#plt.yticks([-0.3,0.1,0.2])
#plt.xlim((y[0],2013))
#plt.xticks([y[0], 0.01,  y[-1]])
#plt.show()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       