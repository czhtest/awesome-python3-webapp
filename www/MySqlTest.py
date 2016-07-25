import DBOperation as db
import tushare as ts
import pandas as pd
import OwnTime as ot
import dateFrameTemplate as dft
#链接数据库

'''
df =pd.read_csv('stockData/2011-01-012016-07-23_5m.csv')

#print(df)
#exit()


#写入数据库
tbName='sh_5'
df.to_sql(name=tbName,con=conn,flavor='mysql',if_exists='append',chunksize=100)
#读取
cur.execute('select date,open,close,high,low,volume from '+tbName)
for each in cur:
    print(each)
#rf=pd.read_sql('select * from sh',con=conn)
#print(rf)
'''
#检查数据是否完整
date='2011-01-04'
#rf_5=pd.read_sql('select * from sh_5 ',con=db.conn)
#rf_d=pd.read_sql('select * from sh_d',con=conn)
#数据加工
def CalcOwnData(dateframe):
    #判断数据类型
    if isinstance(dateframe,pd.core.frame.DataFrame):
        #判断数据是否含有close,date,列
        if 'close' in dateframe.columns and 'date' in dateframe.columns:
            #小日期在前,大日期在后
            dateframe.sort_values(by=['date'],inplace=True)
            #计算
            #第一步计算自定义的MA
            ma_day=[14,60,99,888]
            for ma in ma_day:
                colName='MA'+str(ma)
                dateframe[colName]=round(dateframe['close'].rolling(window=ma).mean(),2)

            #第二步计算自定义的BOLL-M，得到的注意并未偏转一天
	        #此处跟一般的股票软件计算方式有区别，
            colName='LOW'
            dateframe[colName]=round(dateframe['MA99']-2*((((dateframe['close']-dateframe['MA99']).apply(lambda x:x**2)).rolling(window=99).mean())**0.5),2)
            colName='UP'
            dateframe[colName]=round(dateframe['MA99']+2*((((dateframe['close']-dateframe['MA99']).apply(lambda x:x**2)).rolling(window=99).mean())**0.5),2)
            #一切正常返回值
            return dateframe[['date','close','MA14','MA60',
            'MA99','MA888','LOW','UP']]

        else:
            print(dateframe,'数据中缺失date,close列无法完成计算')
    else:
        print(dateframe,'错误的数据类型')


#第一步检查某日期数据是否存在
#1代表完整,2代表数据垃圾,3代表不存在

#从数据库获取某日的数据
def GetDateDataDB(end,ktype='D'):
    tbName='sh_'
    if ktype == 'D' or ktype =='60' or ktype =='30'or ktype == '15'or ktype == '5':
        tbName = tbName+ktype
    else:
        print('未识别的数据库',ktype)
        return
    sql = 'select * from '+tbName+' where substr(date,1,10) <= '+('"'"%s"'"' % end[:10])
    #print(sql)
    rf = pd.read_sql(sql,con=db.conn)
    return CalcOwnData(rf)
#获取值

def GetMyDBDate(date=ot.GetNowDate()):

    date=GetDateDataDB(end=date).tail(1).iat[0,0]

    #print(date)

    for irow in range(len(dft.dayframe.index)):
        ktype=dft.dayframe.index[irow]
        data = GetDateDataDB(end=date,ktype=str(ktype)).tail(1)
        #print(ktype,data)
        for icol in range(len(dft.dayframe.columns)):
            itemp=icol+2
            dft.dayframe.iat[irow,icol]=data.iat[0,itemp]

    #print(dft.dayframe)
    return date,dft.dayframe
    #dft.dayframe.to_csv('DB统计.csv')


import xlrd
from xlutils.copy import copy
import xlwt
#将统计的结果追加到已有的excel中
def WriteDataToExcel(date,dayframe):
    file = '日统计.xls'
    #打开excel工作表保留原有样式
    data = xlrd.open_workbook(file,formatting_info=True)
    #获取第一个sheet
    table = data.sheet_by_index(0)
    #获取工作表的副本
    wb = copy(data)
    #获取副本的第一个sheet
    ws = wb.get_sheet(0)
    #h获取已经多少行
    irows = table.nrows
    startrow=irows
    #加粗
    style=xlwt.easyxf('font: bold 1')
    #第一步遍历已存在的数据中是否已经有该日期
    for irow in range(irows):
        if date in str(table.cell(irow,0).value):
            print('日期已经存在,更新中...')
            startrow = irow
            break
    #第二步按照日期,dayframe的格式进行写入值


    if isinstance(dayframe,pd.core.frame.DataFrame):
        #写入日期
        ws.write(startrow,0,date,style)
        startrow +=1
        #写入列头
        for col in range(len(dayframe.columns)):
            value = dayframe.columns[col]
            #print(value)
            icol = col + 1
            ws.write(startrow,icol,value,style)
        startrow +=1
        #写入内容
        for row in range(len(dayframe.index)):
            #索引行的名称
            value=dayframe.index[row]
            ws.write(startrow,0,value,style)
            for col in range(len(dayframe.columns)):
                #列头
                #value=dayframe.columns[col]
                icol=col + 1


                value=dayframe.iat[row,col]
                ws.write(startrow,icol,value)
            #行数加1
            startrow +=1
        wb.save(file)
    else:
        print(dayframe,'不能识别的数据')
#将数据生成一个text 文本
def GetTextDayFrame(date,dayframe):
    text=''
    if isinstance(dayframe,pd.core.frame.DataFrame):
        text = text + date + '\n\r'
        #列头
        text = text +'\t'
        for col in range(len(dayframe.columns)):
            value = dayframe.columns[col]
            text = text+str(value)
            text = text + '\t'+'\t'
        text =text+'\n\r'
        #写入内容
        for row in range(len(dayframe.index)):
            #索引行的名称
            value=dayframe.index[row]
            text = text+str(value)
            text = text + '\t'
            for col in range(len(dayframe.columns)):
                value=dayframe.iat[row,col]
                text = text+str(value)
                text = text + '\t'+'\t'
            text =text+'\n\r'
        text =text+'\n\r'
        return text





