import urllib.request
import urllib.parse
import gzip
import re
import http.cookiejar

def ungzip(data):
    try:
        print('正在解压...')
        data = gzip.decompress(data)
        print('解压完毕')
    except:
        print('无需解压')
    return data

def getXSRF(data):
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"',flags=0)
    strlist=cer.findall(data)
    return strlist[0]

def getOpener(head):

#deal with the cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key ,value in head.items():
        elem = (key,value)
        header.append(elem)
    opener.addheaders = header
    return opener

url='https://www.zhihu.com/'
webheader2={
    'Accept':'text/html,application/xhtml+xml,*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Host':'www.zhihu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
}

opener = getOpener(webheader2)
op = opener.open(url)
data = op.read()
data = ungzip(data)
_xsrf = getXSRF(data.decode())
print(_xsrf)
url +='login/phone_num'
id = '2457924944@qq.com'
password = 'zehua147'
postDict ={
    '_xsrf':_xsrf,
    'email':id,
    'password':password,
    'remeberme':'y'
}
postData = urllib.parse.urlencode(postDict).encode()
op = opener.open(url,postData)
data = op.read()
data = ungzip(data)
print(data.decode('utf-8'))
print('done')