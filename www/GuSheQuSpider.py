import urllib.request
from bs4 import BeautifulSoup

#import GuSheQuExcel as ex


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
key = '临界'
keywords=['上证','创业板','中小板','国证有色']
import json
#对json格式数据进行解析
json_obj = json.loads(response.text)
print('.....')

import xlrd
from xlutils.copy import copy
file = 'yupen.xls'
data = xlrd.open_workbook(file)
table = data.sheet_by_index(0)
wb = copy(data)
ws = wb.get_sheet(0)
nrow = table.nrows
i = 0
def CheckDate(date):
    for row in range(table.nrows):
        if date in table.cell(row,0).value:
            print('日期已经存在...')
            nrow = row
            return True
    #找不到已知行
    nrow = table.nrows + i
    i = i + 1
    return False

def WriteCol(col,value):
    ws.write(nrow,col,value)

for article in json_obj['value']['lastestArticle']:
    print(article['url'])
    #打开链接并找到内容收集
    soup = BeautifulSoup(urllib.request.urlopen(article['url']),'html5lib')
    #找到日期
    date1 = soup.find('em',id='post-date',class_='rich_media_meta rich_media_meta_text')
    CheckDate(date1.get_text())
    WriteCol(0,date1.get_text())
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
                            WriteCol(4,int(text[-4:]))
                        elif word == keywords[2]:
                            WriteCol(6,int(text[-4:]))
                        elif word == keywords[3]:
                            WriteCol(8,int(text[-4:]))


wb.save(file)