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
    
df1=pd.read_csv('G:\\1.csv',engine='python')

for i in range(0,2):
    df1['month'+str(i)]=(df1[df1.columns[5+i]]-df1[df1.columns[4+i]])/df1[df1.columns[4+i]]
df1['sumprofit']=df1['month0']-index[0]+df1['month1']-index[1]+df1['month2']-index[2]
df1=df1.dropna()
df1=df1.sort_values(by='sumprofit')
num=len(df1)
df4=df1.head(int(num/10))
df5=df1.tail(int(num/10))
print(df4)
#计算检验期的超额收益率 检验期为2010-7 - 2010-12 6个月
sum1=0
cr1=[]
cr2=[]
avg1=1
avg2=1
sum2=0
for i in range(0,3):
    df4['ckmonth'+str(i)]=(df4[df4.columns[8+i]]-df4[df4.columns[7+i]])/df4[df4.columns[7+i]]
    df5['ckmonth'+str(i)]=(df5[df5.columns[8+i]]-df5[df4.columns[7+i]])/df5[df4.columns[7+i]]
for i in range(0,3):
    df4['profit'+str(i)]=df4['ckmonth'+str(i)]-index[3+i]
    df5['profit'+str(i)]=df5['ckmonth'+str(i)]-index[3+i]
    #avg1=avg1+df4['profit'+str(i)].mean()
    #avg2=avg2+df5['profit'+str(i)].mean()
    #avg1=avg1*(1+df4['profit'+str(i)].mean())
    #avg2=avg2*(1+df5['profit'+str(i)].mean())
    sum1=sum1+df4['profit'+str(i)].sum()
    sum2=sum2+df5['profit'+str(i)].sum()
    cr1.append(sum1)
    cr2.append(sum2)
    #cr1.append(avg1)
    #cr2.append(avg2)
x=[]
cr3=[]
for i in range(0,6):
    x.append(i+1)
for i in range(0,6):
    cr3.append(cr1[i]-cr2[i])
print(cr3)
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
plt.plot(x,cr1,label=u'loser')
plt.plot(x,cr2,label=u'winner')
plt.show()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       