#_*_ coding: utf-8 _*_

import time
import datetime
import pandas as pd
import numpy as np
def getshci():
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
    return index
