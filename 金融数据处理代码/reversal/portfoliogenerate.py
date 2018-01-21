#_*_ coding: utf-8 _*_

def portfolio(df1,monthcount,index,flag):
    d1=df1
    d1['month0']=(d1[d1.columns[monthcount+1]]-d1[d1.columns[monthcount]])/d1[d1.columns[monthcount]]
    d1['sumprofit']=d1['month0']-index[monthcount-4]
    d1=d1.dropna()
    d1=d1.sort_values(by='sumprofit')
    num=len(d1)
    df2=d1.head(int(num/10))
    df3=d1.tail(int(num/10))
    if flag==0:
        return df2
    if flag==1:
        return df3