#_*_ coding: utf-8 _*_
import shci
import portfoliogenerate
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend
from matplotlib import legend_handler

index=shci.getshci()
df1=pd.read_csv('G:\\1.csv',engine='python')
x=[]
for i in range(0,48):
    x.append(i+1)
car_loser=[]
car_winner=[]
Arbitrage=[]
avg1=0
avg2=0
for i in range(0,48):
    df2=portfoliogenerate.portfolio(df1,i+4,index,1)
    df3=portfoliogenerate.portfolio(df1,i+4,index,0)
    df2['ckmonth']=(df2[df2.columns[i+6]]-df2[df2.columns[i+5]])/df2[df2.columns[i+5]]
    df3['ckmonth']=(df3[df3.columns[i+6]]-df3[df3.columns[i+5]])/df3[df3.columns[i+5]] 
    df2['profit']=df2['ckmonth']-index[i+1]
    df3['profit']=df3['ckmonth']-index[i+1]
    avg1=avg1+df2['profit'].mean()
    avg2=avg2+df3['profit'].mean()
    car_loser.append(avg2)
    car_winner.append(avg1)
        #x3.append(sum1-sum2)
plt.plot(x,car_winner,Color='green',label='winer')
plt.plot(x,car_loser,Color='red',label='loser')
for i in range(len(car_loser)):
     Arbitrage.append(car_loser[i]-car_winner[i])
plt.plot(x,Arbitrage,Color='blue',label='arbitrage')
plt.legend(loc='upper left')
plt.show()