import tushare as ts
import math
import pandas as pd
import numpy as np

#历史行情
#code：股票代码，即6位数字代码，或者指数代码
# （sh=上证指数 sz=深圳成指 hs300=沪深300指数 sz50=上证50 zxb=中小板 cyb=创业板）
import time
from datetime import timedelta,date
import datetime
def GetNowDate():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))
#df = ts.get_hist_data('sh',start='2016-07-20',ktype='5')
#print(df['close'])
'''
code 股票代码
ktype：数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
'''



#先建一个索引
rowIndexs=[5,15,30,60,'D']
cols=['MA14','MA60','MA99','MA888','LOW','UP']
dayframe = pd.DataFrame(index=rowIndexs,columns=cols)

'''
#print(df)
#设置值
#print(list(df.index))
values={
    14:lambda index:MA(days=14,ktype=str(index)),
    60:lambda index:MA(days=60,ktype=str(index)),
    99:lambda index:MA(days=99,ktype=str(index)),
    888:lambda index:MA(days=888,ktype=str(index))
}
df.MA14=list(map(values[14],df.index))
df.MA60=list(map(values[60],df.index))
df.MA99=list(map(values[99],df.index))
df.MA888=list(map(values[888],df.index))
#print(df)
'''
#定义获取某日的值,
#注意:当ktype等于D时，开始可以等于结束,获取1天，总共获取end-start+1,包含了结束本身
#当ktype等于5,15,30,60时，则不包含end当天数据
def GetDateData(code='sh',end=GetNowDate(),ktype='D'):
    #为了数据准确,先尝试获取5分钟数据,以第一条5分钟数据为准
    realEnd=end
    endDate=datetime.datetime.strptime(realEnd,'%Y-%m-%d').date()
    if ktype !='D':
        #需要结束日期自动后延一天
        realEnd = (endDate+timedelta(days=1)).strftime('%Y-%m-%d')

    dh = ts.get_hist_data(code,end=realEnd,ktype=ktype)
    #将结果集进行升序排列,为了rolling获取值方便
    dh.sort_index(inplace=True,ascending=True)
    #第一步计算自定义的MA
    ma_day=[14,60,99,888]
    for ma in ma_day:
        colName='MA'+str(ma)
        dh[colName]=round(dh['close'].rolling(window=ma).mean(),2)
    #第二步计算自定义的BOLL-M，得到的注意并未偏转一天
    colName='LOW'
    dh[colName]=round(dh['MA99']-2*((((dh['close']-dh['MA99']).apply(lambda x:x**2)).rolling(window=99).mean())**0.5),2)
    colName='UP'
    dh[colName]=round(dh['MA99']+2*((((dh['close']-dh['MA99']).apply(lambda x:x**2)).rolling(window=99).mean())**0.5),2)
    return dh[['close','MA14','MA60','MA99','MA888','LOW','UP']]


#print(GetDateData(end='2016-07-23',ktype='5').tail(4))

#dh = ts.get_hist_data('sh',start='2016-07-20',end='2016-07-20',ktype='5')
#print(dh)


#获取值
def GetMyOwnDate(date=GetNowDate()):
    print(GetDateData(end=date).tail(1).index[0])

    for irow in range(len(dayframe.index)):
        ktype=dayframe.index[irow]
        data = GetDateData(end=date,ktype=str(ktype)).tail(1)
        #print(ktype,data)
        for icol in range(len(dayframe.columns)):
            itemp=icol+1
            dayframe.iat[irow,icol]=data.iat[0,itemp]

    print(dayframe)

GetMyOwnDate('2016-07-20')