import urllib.request
from bs4 import BeautifulSoup




#利用requests表来做

import requests
#html = requests.get("http://www.newrank.cn/static/public/info/detail_new.js",params={"t":1467628480596})
url='http://www.newrank.cn/xdnphb/detail/getAccountArticle'
params={'uuid':'F061A94EDA0AA1F18273663B8CEEE329',
        #'nonce':'c0b94fe77',
        #'xyz':'f719249f27c0374518054fa236fec8e6'
        }
headers={
    'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Content-Length':90,
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie':'CNZZDATA1253878005=314656530-1468373666-http%253A%252F%252Flink.zhihu.com%252F%7C1468379066; Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed=1468375490; Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed=1468383490',
'Host':'www.newrank.cn',
'Origin':'http://www.newrank.cn',
'Referer':'http://www.newrank.cn/public/info/detail.html?account=gushequ',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'
}
response = requests.post(url,params,headers=headers)
if response.status_code !=200:
    print('error',response.status_code)
    exit()


print('.......')
'''
with open('text.html','w') as f:
    f.write(response.text)
'''
#过滤关键字
#获取股票收盘价格
import tushare as ts
def GetStockClose(code,date):
    df = ts.get_hist_data(code,date,date)
    if df.size !=0:
        return df['close'].values[0]

key = '临界'
keywords=['上证','创业板','中小板','国证有色']
import json
#对json格式数据进行解析
json_obj = json.loads(response.text)
print('.....')

import xlrd
from xlutils.copy import copy

file = 'yupen.xls'
#打开excel工作表保留原有样式
data = xlrd.open_workbook(file,formatting_info=True)
#获取第一个sheet
table = data.sheet_by_index(0)
#获取工作表的副本
wb = copy(data)
#获取副本的第一个sheet
ws = wb.get_sheet(0)
#h获取已经多少行
nrow = table.nrows
#计算器
i = 0
#查看某个日期是否已经存在
def CheckDate(date):
    for row in range(table.nrows):
        if date in table.cell(row,0).value:
            print('日期已经存在...')
            global nrow
            nrow = row
            return True
    #找不到已知行
    global i
    nrow = table.nrows + i
    i += 1
    #print('i=',i)
    #print('check nrow:',nrow)
    return False
#写入列值
def WriteCol(col,value):
    if value is not None:
        ws.write(nrow,col,value)

def WriteSZZSClose(date):
    close= GetStockClose('sh',date)
    WriteCol(1,close)
def WriteCYBZClose(date):
    close= GetStockClose('cyb',date)
    WriteCol(4,close)
def WriteZXBZClose(date):
    close= GetStockClose('zxb',date)
    WriteCol(7,close)
def WriteYSBKClose(date):
    close= GetStockClose('399395',date)
    WriteCol(10,close)
#解析返回的json格式的结果
for article in json_obj['value']['lastestArticle']:
    print(article['url'])
    #打开链接并找到内容收集
    soup = BeautifulSoup(urllib.request.urlopen(article['url']),'html5lib')
    #找到日期
    date1 = soup.find('em',id='post-date',class_='rich_media_meta rich_media_meta_text')
    date = date1.get_text()
    CheckDate(date)
    #print('write before',nrow)
    WriteCol(0,date)
    #获取对应日期的收盘价格写入
    WriteSZZSClose(date)
    WriteCYBZClose(date)
    WriteZXBZClose(date)
    WriteYSBKClose(date)
    #获取内容
    context = soup.find('div',class_='rich_media_content')
    for p in context.contents:
        #段落 换行
        if p.name=='p' :
            text = p.get_text()
            if key in text and len(text)>4 and text[-4:].isdigit():
                print(p.get_text(),'\r\n')
                for word in keywords:
                    if word in text :
                        if word == keywords[0]:
                            #这个临界后面的数字是需要写入的
                            WriteCol(2,int(text[-4:]))
                        elif word ==keywords[1]:
                            WriteCol(5,int(text[-4:]))
                        elif word == keywords[2]:
                            WriteCol(8,int(text[-4:]))
                        elif word == keywords[3]:
                            WriteCol(11,int(text[-4:]))

#保存文件
wb.save(file)
