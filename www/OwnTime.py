import time
import datetime
from datetime import timedelta

#获取当前时间
strFormat='%Y-%m-%d'
strHmFormat=' %H:%M'
strSFormat=':%S'
#传入yyyy-mm-dd hh:mm返回date类型数据
def GetDate(strDate):
    if isinstance(strDate,str):
        strDate=strDate.strip()
        if len(strDate)==10:
            return datetime.datetime.strptime(strDate,strFormat).date()
        elif len(strDate)==16:
            return datetime.datetime.strptime(strDate,strFormat+strHmFormat)
        elif len(strDate)==19:
            datetime.datetime.strptime(strDate,strFormat+strHmFormat+strSFormat)
        else:
            print(strDate,'无法识别的日期格式')
    else:
        print(strDate,'不是str类型')

#获取当前日期
def GetNowDate():
    return time.strftime(strFormat,time.localtime(time.time()))
def GetNowHmDate():
    return time.strftime(strFormat+strHmFormat,time.localtime(time.time()))
#传入的日期转化为字符串年月日
def FormatYmdDate(date):
    if isinstance(date,datetime.date):
        return date.strftime(strFormat)

    else:
        print(date,'不是日期类型')

#传入的日期转化为字符串年月日 XX:mm
def FormatHMDate(date):
    if isinstance(date,datetime.date):
        return date.strftime(strFormat+strHmFormat)
    else:
        print(date,'不是日期类型')
#传入的日期转化为字符串年月日 XX:mm
def FormatHMSDate(date):
    if isinstance(date,datetime.date):
        return date.strftime(strFormat+strHmFormat+strSFormat)
    else:
        print(date,'不是日期类型')
#日期加N天
def GetAddDays(date,days):
    if isinstance(date,datetime.date):
        return date + timedelta(days=days)
    else:
        print(date,'不是日期类型')

#获取时间的下一天
def GetOneMoreDate(date):
    if isinstance(date,datetime.date):
       return FormatYmdDate(GetAddDays(date,1))
    elif isinstance(date,str):
       return FormatYmdDate(GetAddDays(GetDate(date),1))

