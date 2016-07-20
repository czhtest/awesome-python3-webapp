import requests
import lxml
import json
from bs4 import BeautifulSoup
import time
import numpy as np
import pandas as pd
import tushare as ts
'''
crawContentURL类:
爬取地址url
参数params说明:
__biz 每个公众号都唯一
uin 每个公众号都唯一
key 跟每个微信号访问端有关
frommsgid 因微信api count无法正常获取大于10的数据,需要这个值来重新填充
f 代表请求的数据格式
以上两个参数都可以通过fidder抓包工具获取requests
'''
class crawContentURL():
    url='https://mp.weixin.qq.com/mp/getmasssendmsg'
    frommsgid=0
    params={
        '__biz':'MjM5MjAxNTE4MA==',
        'uin':'MjY5NzE0ODE1',
        #每个公众号的__biz和uin的值都可以
        'key':'77421cf58af4a6537ad3a7327287fb3f6021e10a5715d272d75bfd3249a5833bbeb7694272f338106e63a683b726e8bc',
        'f':'json',
        'frommsgid':frommsgid,
        'count':'20'
        }
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-us,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
        'X-Requested-With': 'XMLHttpRequest',
        #'Referer': 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MjM5MjAxNTE4MA==&uin=MjY5NzE0ODE1&key=77421cf58af4a65391f33894925a7a05298b0cc9af8a273f8033a4ce98870ccfd541b04c3788d5e5f23090afaefee57d&devicetype=Windows+10&version=62000050&lang=zh_CN&pass_ticket=7vQoNFgohtesQjYD3XrXJ%2B1wX5b%2Ftevfn7pY%2B83MBBzYQt2MEOXH%2Blb5xAwt2sox',
        #'Host': 'mp.weixin.qq.com'
}
    def crawlURLS(self):
        self.params['frommsgid']=self.frommsgid
        response = requests.get(self.url,params=self.params,headers=self.headers,verify=False)


        content = response.content.decode('utf-8')
        py_objs = response.json()
        if py_objs['ret'] == 0:
            if isinstance(py_objs,dict):
                general_msg_list=py_objs['general_msg_list']
                g_lists = eval(general_msg_list)

                self.frommsgid = g_lists['list'][9]['comm_msg_info']['id']
                #print('下一个id',self.frommsgid)
                for url in g_lists['list']:
                    datetime=url['comm_msg_info']['datetime']
                    #print(datetime)
                    #print(isinstance(url,dict))
                    #print(url)
                    if 'app_msg_ext_info' in url:
                        content_url=(url['app_msg_ext_info']['content_url'])
                        #转义字符
                        url = content_url.replace('\\/','/')
                        url = url.replace('&amp;','&')
                        with open('content.txt','a') as file:
                            file.write(url)
                            file.write('\n')

        else:
            #这个不对,
            print('error:',py_objs)
            #break
'''
#生成content_url.txt文档
craw = crawContentURL()
for i in range(1000000):
    if i%1000 == 0 and i !=0:
        print('我要睡10s')
        time.sleep(10)
    craw.crawlURLS()
'''






'''
key = '临界'
keywords=['上证','创业板','中小板','国证有色']
import json
#对json格式数据进行解析
#json_obj = json.loads(response.text)
print('.....')





bDate=False

shlimits=[]
cyblimits=[]
zxblimits=[]
ysblimits=[]
dates=[]




#将url内容一一打开并爬取到excel中
with open('content_url.txt','r') as file:
    urls = file.readlines()
    for url in urls:
        global bDate
        bDate = False

        response = requests.get(url)
        #打开链接并找到内容收集
        soup = BeautifulSoup(response.content,'lxml')
        #找到日期
        date1 = soup.find('em',id='post-date',class_='rich_media_meta rich_media_meta_text')
        date = date1.get_text()

        #获取内容
        context = soup.find('div',class_='rich_media_content')
        for p in context.contents:
            #段落 换行
            if p.name=='p' :
                text = p.get_text()
                if key in text and  text[text.find(key)+2:].isdigit():
                    #print(p.get_text(),'\r\n')
                    number=int(text[text.find(key)+2:])
                    for word in keywords:
                        if word in text :
                            if word == keywords[0]:
                                #这个临界后面的数字是需要写入的
                                #print(int(text[-4:]))
                                #WriteCol(2,int(text[-4:]))
                                shlimits.append(number)
                                global bDate
                                bDate = True
                            elif word ==keywords[1]:
                                #print(int(text[-4:]))
                                #WriteCol(5,int(text[-4:]))
                                cyblimits.append(number)
                                global bDate
                                bDate = True
                            elif word == keywords[2]:
                                #print(int(text[-4:]))
                                #WriteCol(8,int(text[-4:]))
                                zxblimits.append(number)
                                global bDate
                                bDate = True


        if bDate:
            dates.append(date)


dlimit ={
    '日期':pd.Series(dates),
    '上证临界':pd.Series(shlimits),
    '创业板临界':pd.Series(cyblimits),
    '中小板临界':pd.Series(zxblimits),
    #'有色临界':ysblimits
}
#print(len(dates))
frame=pd.DataFrame(dlimit)
print(dlimit)
print(frame)
frame.to_excel('dlimit.xls',)
'''

'''
#将整理过后的数据gushequTotal.xls读取到dateframe
#获取股票收盘价格

def GetStockClose(code,date):
    df = ts.get_hist_data(code,date,date)
    if df.size !=0:
        return df['close'].values[0]

df=pd.read_excel('gushequTotal.xls','Sheet1',index_col=0)
print(df)
for irow in range(len(df.index)):
    date=df.get_value(irow,'日期')
    SZZS=GetStockClose('sh',date)
    ZXBZ=GetStockClose('zxb',date)
    CYBZ=GetStockClose('cyb',date)
    df.set_value(irow,'上证收盘',SZZS)
    df.set_value(irow,'中小板收盘',ZXBZ)
    df.set_value(irow,'创业板收盘',CYBZ)

print(df)
df.to_excel('gushequTotal.xls')
'''

#将数据计算一番
df=pd.read_excel('gushequTotal.xls','Sheet1',index_col=0)
df.上证涨跌幅=(df.上证临界-df.上证收盘)/df.上证收盘*100
df.中小板涨跌幅=(df.中小板临界-df.中小板收盘)/df.中小板收盘*100
df.创业板涨跌幅=(df.创业板临界-df.创业板收盘)/df.创业板收盘*100
df.to_excel('gushequTotal.xls')