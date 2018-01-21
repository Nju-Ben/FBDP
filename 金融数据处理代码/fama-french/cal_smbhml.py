#_*_ coding: utf-8 _*_
#����İ�
import time
import prcs
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

equity=pd.read_csv('F:\\FS_Combas.csv',engine='c',encoding= u'utf-8') 
stock=pd.read_csv('F:\\TRD_Mnthnew.csv',engine='c',encoding= u'utf-8') 

equity['code']=equity.rawdata.apply(prcs.getcode)
equity['Stkcdnum']=equity.code.apply(prcs.code2int)
equity['date']=equity.rawdata.apply(prcs.getdate)
equity['equity']=equity.rawdata.apply(prcs.getequity)
equity['month']=equity.rawdata.apply(prcs.getmonth1)
equity['year']=equity.rawdata.apply(prcs.getyear1)+1
equity=equity.drop('rawdata',1)
equity1=equity[equity.month==12]
equity1=equity1.reset_index(drop=True)

stock['month']=stock.Trdmnt.apply(prcs.getmonth2)
stock['year']=stock.Trdmnt.apply(prcs.getyear2)
stock['Stkcdnum']=stock.Stkcd.apply(prcs.code2int)
stock=stock.reset_index(drop=True)
stock=stock.drop('year',1)
stock['year']=stock.Trdmnt.apply(prcs.changeyear)
stockregression=stock[['Stkcdnum','Trdmnt','Mretwd','year','month']]#�����Ժ���лع�
print(stockregression)

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

for name, group in result.groupby('Trdmnt'):
    #print(group)
    sizeline=group.size430.quantile(0.5)
    bm30=group.bm.quantile(0.3)
    bm70=group.bm.quantile(0.7)
    print(sizeline)
    print(bm30)
    print(bm70)
    
    #y_train=group[['Mretwd']]
    #x_train=group[['profit','smb','hml']]
#     y_train=group[['Mretwd']]
#     x_train=group[['profit','smb','hml']]  

# ##���Ĳ������з��鲢����ÿһ��ÿ���µ�smbֵ��hmlֵ
# monthlist=[]
# yearlist=[]
# smblist=[]
# hmllist=[]
# for i in range(2003,2014):
#     for j in range(1,13):
#         dfyear=result[(result.month_x==j) & (result.year==i)]
#         sizeline=dfyear.size430.quantile(0.5)
#         bm30=dfyear.bm.quantile(0.3)
#         bm70=dfyear.bm.quantile(0.7)
#         dfyear["sizegroup"]=np.where(dfyear.size430<=sizeline,1,0)
#         dfyear["bmgroup"]=np.where(dfyear.bm<=bm30,1,np.where(dfyear.bm<=bm70,2,3))  #data1 =np.where(data > 0,1,np.where(data <0,-1,0))
#         dfbg=dfyear[(dfyear.sizegroup==0) & (dfyear.bmgroup==1)]
#         dfbn=dfyear[(dfyear.sizegroup==0) & (dfyear.bmgroup==2)]
#         dfbv=dfyear[(dfyear.sizegroup==0) & (dfyear.bmgroup==3)]
#         dfsg=dfyear[(dfyear.sizegroup==1) & (dfyear.bmgroup==1)]
#         dfsn=dfyear[(dfyear.sizegroup==1) & (dfyear.bmgroup==2)]
#         dfsv=dfyear[(dfyear.sizegroup==1) & (dfyear.bmgroup==3)]
#         sg=(dfsg.Msmvttl_x*dfsg.Mretwd/(dfsg.Msmvttl_x.sum())).sum()
#         sn=(dfsn.Msmvttl_x*dfsn.Mretwd/(dfsn.Msmvttl_x.sum())).sum()
#         sv=(dfsv.Msmvttl_x*dfsv.Mretwd/(dfsv.Msmvttl_x.sum())).sum()
#         bg=(dfbg.Msmvttl_x*dfbg.Mretwd/(dfbg.Msmvttl_x.sum())).sum()
#         bn=(dfbn.Msmvttl_x*dfbn.Mretwd/(dfbn.Msmvttl_x.sum())).sum()
#         bv=(dfbv.Msmvttl_x*dfbv.Mretwd/(dfbv.Msmvttl_x.sum())).sum()
#         smb=1/3*(sg+sn+sv)-1/3*(bg+bn+bv)
#         hml=1/2*(sv+bv)-1/2*(sg+bg)
#         monthlist.append(j)
#         yearlist.append(i)
#         smblist.append(smb)
#         hmllist.append(hml)
#          
# temp={"year":yearlist,
#    "month_x":monthlist,
#    "smb":smblist,
#    "hml":hmllist}
# smbhml=DataFrame(temp)