import tushare as ts
import math
import pandas as pd
import numpy as np
import dateFrameTemplate as dft
import OwnTime as ot

#历史行情
#code：股票代码，即6位数字代码，或者指数代码
# （sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
import time
from datetime import timedelta,date
import datetime

#df = ts.get_hist_data('sh',start='2016-07-20',ktype='5')
#print(df['close'])
'''
code 股票代码
ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
'''



#先建一个索引

#定义获取某日的值,
#注意:当ktype等于D时，开始可以等于结束,获取1天，总共获取end-start+1,包含了结束本身
#当ktype等于5,15,30,60时，则不包含end当天数据
'''
BOLL-M 算法
N:=20;
MID:=MA(C,N);
VAR1:=POW((C-MID),2);
VAR2:=MA(VAR1,N);
VAR3:=SQRT(VAR2);
UPPER:=MID+2*VAR3;
LOWER:=MID-2*VAR3;
BOLL:REF(MID,1);
UB:REF(UPPER,1);
LB:REF(LOWER,1);

MID赋值:收盘价的N日简单移动平均
VAR1赋值:(收盘价-MID)的2乘幂
VAR2赋值:VAR1的N日简单移动平均
VAR3赋值:VAR2的开方
UPPER赋值:MID+2*VAR3
LOWER赋值:MID-2*VAR3
输出BOLL:1日前的MID
输出UB:1日前的UPPER
输出LB:1日前的LOWER
'''
def GetDateData(code='sh',end=ot.GetNowDate(),ktype='D'):
    #为了数据准确,先尝试获取5分钟数据,以第一条5分钟数据为准
    realEnd=end
    #print(end,ktype,'...')
    if ktype !='D':
        #需要结束日期自动后延一天
        realEnd = ot.GetOneMoreDate(end)
    #print(realEnd,ktype)
    dh = ts.get_hist_data(code,end=realEnd,ktype=ktype)
    #将结果集进行升序排列,为了rolling获取值方便
    dh.sort_index(inplace=True,ascending=True)
    #第一步计算自定义的MA
    ma_day=[14,60,99,888]
    for ma in ma_day:
        colName='MA'+str(ma)
        dh[colName]=round(dh['close'].rolling(window=ma).mean(),2)
    #第二步计算自定义的BOLL-M，得到的注意并未偏转一天
	#此处跟一般的股票软件计算方式有区别，
	
    colName='LOW'
    dh[colName]=round(dh['MA99']-2*((((dh['close']-dh['MA99']).apply(lambda x:x**2)).rolling(window=99).mean())**0.5),2)
    colName='UP'
    dh[colName]=round(dh['MA99']+2*((((dh['close']-dh['MA99']).apply(lambda x:x**2)).rolling(window=99).mean())**0.5),2)
    return dh[['close','MA14','MA60','MA99','MA888','LOW','UP']]


#print(GetDateData(end='2016-07-22',ktype='5').tail(4))

#dh = ts.get_hist_data('sh',start='2016-D07-20',end='2016-07-20',ktype='5')
#print(dh)


#获取值
def GetMyOwnDate(date=ot.GetNowDate()):
    date=GetDateData(end=date).tail(1).index[0]
    print(date)

    for irow in range(len(dft.dayframe.index)):
        ktype=dft.dayframe.index[irow]
        data = GetDateData(end=date,ktype=str(ktype)).tail(1)
        #print(ktype,data)
        for icol in range(len(dft.dayframe.columns)):
            itemp=icol+1
            dft.dayframe.iat[irow,icol]=data.iat[0,itemp]

    print(dft.dayframe)
    dft.dayframe.to_excel('日统计.xls',sheet_name=date)

GetMyOwnDate()