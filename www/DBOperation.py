import pymysql
import dateFrameTemplate as dft
import OwnTime as ot
import tushare as ts
import pandas as pd
import time

#链接数据库
conn=pymysql.connect(host='localhost',user='root',passwd='root',
                     db='stock',charset='utf8')

cur = conn.cursor()
#检查数据是否完整
#一天有1条sh_d数据,4条sh_60数据,8条sh_30数据,16条sh_15数据,48条sh_5数据
def CheckDateComplete(date):
    if isinstance(date,str):
        #将日期转化为年月日
        date=date[:10]
        num = 0
        cur.callproc('checkdatecompleted',(date,num))
        cur.execute('select @_checkdatecompleted_1')
        data = cur.fetchall()
        if data:
            for rec in data:
                num = rec[0]
        return num
    else:
        print(date,'CheckDateComplete参数错误')
#提交事务
def commitData():
    #cur.close()
    conn.commit()
#回滚事务
def rollBackData():
    #cur.close()
    conn.rollback()
#删除某一天的数据
def DelDateData(date):

    if isinstance(date,str):
        #将日期转化为年月日
        strdate=date[:10]
        print(date)
        cur.callproc('DelDateData',(strdate,2))
        commitData()
    else:
        print(date,'DelDateData参数错误')

#获取某段时间的历史数据
def GetHisData(start,end,ktype='D'):
    if start ==None or end == None:
        print('开始/结束日期不能为空')
        return
    df = ts.get_hist_data('sh',start=start,end=end,ktype=ktype)
    if len(df.index) != 0:
        print('获取',start,'到',end,'类型',ktype)
        df['date']=df.index
        return df[dft.dbCols]


def WriteDataToDB(dateframe,ktype):
    #检查列是否相同
    #print('写入数据dayframe',dateframe)
    tbName='sh_'
    correctNum=0
    if ktype == 'D' or ktype =='60' or ktype =='30'or ktype == '15'or ktype == '5':
        tbName = tbName+ktype
    else:
        print('未识别的数据库',ktype)
        return
    correctNums={
        'D':1,
        '60':4,
        '30':8,
        '15':16,
        '5':48
    }
    values=[]
    values.clear()

    if isinstance(dateframe,pd.core.frame.DataFrame):
        #判断列是否完全相同
        print(len(dateframe.index),ktype)
        if (len(dateframe.columns)==6):
            #判断某天的数据是否完整
            if len(dateframe.index)%correctNums[ktype]==0:
                sql = 'insert into '+tbName+'(date,open,close,high,low,volume) values (%s,%s,%s,%s,%s,%s)'
                for irow in range(len(dateframe.index)):
                    #这样写保证了数据的顺序
                    num = CheckDateComplete(str(dateframe.date[irow]))
                    if num !=1 :
                        values.append((str(dateframe.date[irow]),str(round(dateframe.open[irow],2)),
                               str(round(dateframe.close[irow],2)),str(round(dateframe.high[irow],2)),
                               str(round(dateframe.low[irow],2)),str(round(dateframe.volume[irow],2))
                               ))
                    else:
                        print('num=',num,str(dateframe.date[irow]))
            #print(values,sql)

                try:
                    sta=cur.executemany(sql,values)
                    print('执行数据插入:',sta)
                except Exception as e:
                    print('错误',sql,e)
            else:
                print('网络数据不完整',ktype)
    else:
        print('无需更新...')


#下载最大天的数据并写入到数据库中
def DownLoadlastest():
    #获取stock数据库中最大的一条数据的日期
    print(ot.GetNowHmDate(),'开始下载最新数据')
    maxDate=None

    et= ot.GetOneMoreDate(ot.GetNowDate())
    cur.callproc('getmaxdate',(1,maxDate))
    cur.execute('select @_getmaxdate_1')
    data = cur.fetchall()
    if data:
        for rec in data:
            maxDate = rec[0]
    print('数据库:',maxDate)
    st=maxDate
    if maxDate is not None:
        #判断最大这天的数据是否完整1,2多余，3不存在
        num = CheckDateComplete(maxDate)
        if num ==1:
            #获取从maxDate+1到现在为止包含现在的所有周期数据
            st = ot.GetOneMoreDate(maxDate)
        else:
            DelDateData(maxDate)
            print(maxDate,'数据不完整,清除...')
            st = maxDate

    print('最新数据范围',st,et)
    #获取最新的数据
    for ktype in dft.rowIndexs:
        WriteDataToDB(GetHisData(st,et,str(ktype)),str(ktype))
        #time.sleep(1)
    commitData()

#检查全体已有数据是否完整
def CheckAllDataCompleted():
    rf_d = pd.read_sql('select * from sh_d',con=conn)
    dates = rf_d['date']
    for date in dates:
        #print(date)
        num = CheckDateComplete(date)
        if num !=1:
            print(date,'数据不完整...需要修正')



'''
print(CheckDateComplete('2016-07-25'))
DownLoadlastest()
df = GetHisData('2016-07-25','2016-07-27','5')
print(len(df.index))
'''