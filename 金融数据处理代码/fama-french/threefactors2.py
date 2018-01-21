#encoding=utf8
#导入的包
import time
import prcs
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from pandas.core.frame import DataFrame
from scipy import stats
from sklearn.linear_model import LinearRegression

#格式处理函数若干

#第一阶段，将个股的月回报与财务数据合并并分组，计算smb和hml值，并对时间进行调整
equity=pd.read_csv('F:\\FS_Combas.csv',engine='c',encoding= u'utf-8') 
stock=pd.read_csv('F:\\TRD_Mnthnew.csv',engine='c',encoding= u'utf-8') 

##第一步 对财务数据进行处理，按股票代码取出每年12.31日的所有者权益
equity['code']=equity.rawdata.apply(prcs.getcode)
equity['Stkcdnum']=equity.code.apply(prcs.code2int)
equity['date']=equity.rawdata.apply(prcs.getdate)
equity['equity']=equity.rawdata.apply(prcs.getequity)
equity['month']=equity.rawdata.apply(prcs.getmonth1)
equity['year']=equity.rawdata.apply(prcs.getyear1)+1
equity=equity.drop('rawdata',1)
equity1=equity[equity.month==12]
equity1=equity1.reset_index(drop=True)

##第二步 对月个股数据进行处理，对时间进行调整，调整方法详见报告
#stock=stock[]
stock['month']=stock.Trdmnt.apply(prcs.getmonth2)
stock['year']=stock.Trdmnt.apply(prcs.getyear2)
stock['Stkcdnum']=stock.Stkcd.apply(prcs.code2int)
stock=stock.reset_index(drop=True)
stock=stock.drop('year',1)
stock['year']=stock.Trdmnt.apply(prcs.changeyear)
stockregression=stock[['Stkcdnum','Trdmnt','Mretwd','year','month']]#用于以后进行回归
print(stockregression)

##第三步 对月个股数据的总市值进行处理，取出t-1年12月1日和t年5月1日的数据，进行表的合并。
##合并后，月个股回报新增三个字段，一个是所有者权益，一个是12月1日总市值，一个是5月1日总市值。
##根据合并后的表计算出bm，并且将利用词表进行分组
result = pd.merge(stock, equity1, on=['Stkcdnum', 'year'])
result['equity']=result['equity'].apply(prcs.code2double)
result['Msmvttl']=result['Msmvttl'].apply(prcs.code2double)
result=result[['Stkcdnum','Trdmnt','equity','Msmvttl','Mretwd','year','month_x']]
size1=result[result.month_x==12]
size1=size1[['Stkcdnum','year','Msmvttl']]
size1['year']=size1['year']+1
size2=result[result.month_x==5]
size2=size2[['Stkcdnum','year','Msmvttl']]
result = pd.merge(result, size1, on=['Stkcdnum', 'year'])
result = pd.merge(result, size2, on=['Stkcdnum', 'year'])
result.rename(columns={'Msmvttl_y':'size1231', 'Msmvttl':'size430'}, inplace = True)
result['bm']=result['equity']/result['size1231']
#result=result.dropna()

# result1=result[result.Stkcdnum<500000]
# writer = pd.ExcelWriter('F:\\分组前个股数据.xlsx')
# result1.to_excel(writer,'bm',index=False)
# writer.save()

##第四步，进行分组并计算每一年每个月的smb值和hml值
monthlist=[]
yearlist=[]
smblist=[]
hmllist=[]
for i in range(2003,2014):
    for j in range(1,13):
        dfyear=result[(result.month_x==j) & (result.year==i)]
        sizeline=dfyear.size430.quantile(0.5)
        bm30=dfyear.bm.quantile(0.3)
        bm70=dfyear.bm.quantile(0.7)
        dfyear["sizegroup"]=np.where(dfyear.size430<=sizeline,1,0)
        dfyear["bmgroup"]=np.where(dfyear.bm<=bm30,1,np.where(dfyear.bm<=bm70,2,3))  #data1 =np.where(data > 0,1,np.where(data <0,-1,0))
        dfbg=dfyear[(dfyear.sizegroup==0) & (dfyear.bmgroup==1)]
        dfbn=dfyear[(dfyear.sizegroup==0) & (dfyear.bmgroup==2)]
        dfbv=dfyear[(dfyear.sizegroup==0) & (dfyear.bmgroup==3)]
        dfsg=dfyear[(dfyear.sizegroup==1) & (dfyear.bmgroup==1)]
        dfsn=dfyear[(dfyear.sizegroup==1) & (dfyear.bmgroup==2)]
        dfsv=dfyear[(dfyear.sizegroup==1) & (dfyear.bmgroup==3)]
        sg=(dfsg.Msmvttl_x*dfsg.Mretwd/(dfsg.Msmvttl_x.sum())).sum()
        sn=(dfsn.Msmvttl_x*dfsn.Mretwd/(dfsn.Msmvttl_x.sum())).sum()
        sv=(dfsv.Msmvttl_x*dfsv.Mretwd/(dfsv.Msmvttl_x.sum())).sum()
        bg=(dfbg.Msmvttl_x*dfbg.Mretwd/(dfbg.Msmvttl_x.sum())).sum()
        bn=(dfbn.Msmvttl_x*dfbn.Mretwd/(dfbn.Msmvttl_x.sum())).sum()
        bv=(dfbv.Msmvttl_x*dfbv.Mretwd/(dfbv.Msmvttl_x.sum())).sum()
        smb=1/3*(sg+sn+sv)-1/3*(bg+bn+bv)
        hml=1/2*(sv+bv)-1/2*(sg+bg)
        monthlist.append(j)
        yearlist.append(i)
        smblist.append(smb)
        hmllist.append(hml)
         
temp={"year":yearlist,
   "month_x":monthlist,
   "smb":smblist,
   "hml":hmllist}
smbhml=DataFrame(temp)

#第二阶段 构建三因子数据
##第一步 读取rm和rf，计算每一年每个月市场超额收益rm-rf，并调整时间
rm=pd.read_csv('F:\\TRD_Cnmont.csv',engine='c',encoding= u'utf-8')
rf=pd.read_csv('F:\\TRD_Nrrate.csv',engine='c',encoding= u'utf-8')
rm=rm[rm.Markettype==5]
rm=rm[['Trdmnt','Cmretwdtl']]
rm['year']=rm.Trdmnt.apply(prcs.getyear2)
rm['month_x']=rm.Trdmnt.apply(prcs.getmonth2)  
rf['year']=rf.Clsdt.apply(prcs.getyear2)
rf['month_x']=rf.Clsdt.apply(prcs.getmonth2)
rf['day']=rf.Clsdt.apply(prcs.getday)
rf=rf[rf.day==1]
rf=rf[['Clsdt','Nrrmtdt','year','month_x']]
print(rf)
rf['Nrrmtdt']=rf['Nrrmtdt']/100
rf1=rf.drop('year',1)
rf1['year']=rf1.Clsdt.apply(prcs.changeyear)#该数据用于计算个股的超额收益

##第二步，将各表进行合并，得到准备回归的数据。
rmrf = pd.merge(rm, rf, on=['year', 'month_x'])
rmrf['profit']=rmrf['Cmretwdtl']-rmrf['Nrrmtdt']
rmrf=rmrf[['Clsdt','profit','year','month_x']]
rmrf['year']=rmrf.Clsdt.apply(prcs.changeyear)
threefactor=pd.merge(smbhml, rmrf, on=['year', 'month_x'])
stockregression.rename(columns={'month':'month_x'}, inplace = True)
stockregression=pd.merge(stockregression,rf1,on=['year','month_x'])
stockregression['Mretwd']=stockregression['Mretwd']-stockregression['Nrrmtdt']
lastbattle= pd.merge(stockregression, threefactor, on=['year', 'month_x'])

lastbattle=lastbattle.dropna()
#lastbattle=lastbattle[['Mretwd','profit','smb','hml']]
#第三阶段 回归
print("回归方法一:OLS回归")
model = ols(formula='Mretwd ~ profit + smb + hml',data=lastbattle)
results = model.fit()
print(results.summary())

#第二种回归按股票代码进行时间序列回归，得到长度为股票数量的四个向量，并进行显著性检验
##第一步 四个向量分别代表个股超额收益，市场超额收益,smb,hml,进行多元线性回归
intercept=[]
b1=[]
b2=[]
b3=[]
for name, group in lastbattle.groupby('Stkcdnum'):
    y_train=group[['Mretwd']]
    x_train=group[['profit','smb','hml']]  
    linreg = LinearRegression()  
    model=linreg.fit(x_train, y_train)  
    intercept.append(linreg.intercept_[0])
    b1.append(linreg.coef_[0][0])
    b2.append(linreg.coef_[0][1])
    b3.append(linreg.coef_[0][2])

test1=[0 for i in range(len(b1))]
test={"test1":test1}
reg={"intercept":intercept,
   "b1":b1,
   "b2":b2,
   "b3":b3}
reg=DataFrame(reg)    
# writer = pd.ExcelWriter('F:\\回归结果.xlsx')
# reg.to_excel(writer,'regression',index=False)
# writer.save()

##第二步 对回归结果进行参数检验
x=stats.ttest_ind(reg['intercept'],test1, equal_var=False)
x1=stats.ttest_ind(reg['b1'],test1, equal_var=False)
x2=stats.ttest_ind(reg['b2'],test1, equal_var=False)
x3=stats.ttest_ind(reg['b3'],test1, equal_var=False)
print("回归方法二:")
print("截距均值:"+str(reg.intercept.mean()))
print("系数1均值"+str(reg.b1.mean()))
print("系数2均值"+str(reg.b2.mean()))
print("系数3均值"+str(reg.b3.mean()))
print("截距p值"+str(x))
print("系数1p值"+str(x1))
print("系数2p值"+str(x2))
print("系数3p值"+str(x3))
print("")
print("")

















