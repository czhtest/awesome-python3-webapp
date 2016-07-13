import urllib.request
from bs4 import BeautifulSoup

#import GuSheQuExcel as ex

'''
import zlib
def deflate(data):
    try:
        return zlib.decompress(data,-zlib.MAX_WBITS)
    except:
        return zlib.decompress(data)


url = 'http://mp.weixin.qq.com/s?__biz=MjM5MjAxNTE4MA==&mid=2652140878&idx=1&sn=1378f7d6d4ae1a0bfda658c30112cd9c&scene=23&srcid=0711fzIIh9UpfnvRMECCjj1P#rd'
print(url)
url1 = 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MjM5MjAxNTE4MA==&uin=MjY5NzE0ODE1&key=77421cf58af4a65309782d38c285b5aa849ece1509e31c61587d240a8627ffb8b90d88cfb215b7f75e04f37a8a2ee270'
header_dict={
    'Host':'mp.weixin.qq.com',
    'Connection':'keep-alive',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent':\
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-us,en;q=0.8',
    'Cookie':'wxtokenkey=05e91a96dd60817e6a02e371f2a9848b9d9875696aeda119aaacc255b8b306cb; wxticket=1429999366; wxticketkey=7035b8209834a9cdb26532e2b167a21b9d9875696aeda119aaacc255b8b306cb'
}

req = urllib.request.Request(url1,headers=header_dict)
#由于返回数据类型是deflate类型,需要解密

f = urllib.request.urlopen(req)
print(f.getcode())
contexts = f.read()
f.close()
fd = deflate(contexts)
fp = open('test3.html','wb')
fp.write(contexts)
fp.close()
soupList = BeautifulSoup(fd)
#print(soupList.prettify())

from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.get('http://weixin.sogou.com')
driver.find_element_by_id('upquery').send_keys(u'浙江旅游')
driver.find_element_by_class_name('swz2').click()
now_handle = driver.current_window_handle
driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div/div[2]/div/div[1]').click()
time.sleep(10)
all_handle = driver.window_handles
for handle in all_handle:
    print(handle)
if handle != now_handle:
    driver.switch_to.window(handle)
    print ( '当前网页title',driver.title)
#driver.quit()
'''
'''
url='http://www.newrank.cn/public/info/detail.html?account=gushequ'
urllib.request.urlretrieve(url,'test2.html')
urllib.request.urlcleanup()
soup = BeautifulSoup(urllib.request.urlopen(url),'html5lib')
#获取标题
print(soup.head.title.string)
#获取日期
list = soup.find_all('a',class_='ellipsis',href=True,target='_blank',title=True)
print(list)
for li in list:
    print(li)
'''
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
print(json_obj)



for article in json_obj['value']['lastestArticle']:
    print(article['url'])
    #打开链接并找到内容收集
    soup = BeautifulSoup(urllib.request.urlopen(article['url']),'html5lib')
    #找到日期
    date1 = soup.find('em',id='post-date',class_='rich_media_meta rich_media_meta_text')

    print(date1.get_text())
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
                            print(int(text[-4:]))
                        elif word ==keywords[1]:
                            print(int(text[-4:]))
                        elif word == keywords[2]:
                            print(int(text[-4:]))
                        elif word == keywords[3]:
                            print(int(text[-4:]))
                #datas.append(data)
