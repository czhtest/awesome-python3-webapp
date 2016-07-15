'''
该文件主要作用:采集http://www.imaibo.net/space/1954702更新，
当发现有自上一次采集的新内容时,将新的内容采集下来并打印出来
'''
import time
import os
emailContext=None
#获取时间戳
def getNowTime():
    return time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
#print(getNowTime())
from bs4 import BeautifulSoup
import requests
import urllib
class crawlLiuMaibo():
    url='http://www.imaibo.net/space/1954702'
    params={
        'app':'home',
        'mod':'Space',
        'act':'getSpaceWeibo300',
        'uid':1954702,
        'limit':1,
        'p':1,
        'lastId':0,
        'syncShareSpaceWeiboId':0
    }

    response = requests.get(url,params=params)
    #返回编码方式
    #print(response.encoding)
    #打印内容
    #print(response.text)
    #内置json解析器,帮助处理json数据,返回python数据
    py_obj = response.json()
    #print(py_obj)
    #import json
    #print('..........')
    #将json格式数据转换成python对象loads,类同于.json()
    #py_obj1 = json.loads(response.text)
    #print(json_obj)
    #print(py_obj == py_obj1)
    #其实已经是部分文档了
    now_num=0
    newText=None
    Imgs=[]
    #写入本地图片文件夹中
    def writeImg(self,imgurl):
        if imgurl !=None:
            filename=imgurl[-17:-4]
            #print(filename)
            suffix=imgurl[-4:]
            #   print(suffix)
            if os.path.exists("WeiBoImg/"+filename+suffix):
                return
            else:
                newimg=requests.get(imgurl)
                with open("WeiBoImg/"+filename+suffix,'wb') as file:
                    file.write(newimg.content)
                self.imgs.append(filename+suffix)
    def crawLastest(self):
        #响应内容
        if self.response.status_code == requests.codes.ok:
            #响应成功将尝试采集内容
            lists = self.py_obj['data']['weibo_lists']
            soup = BeautifulSoup(lists,'html5lib')
            #print(soup.prettify())
            now_ids = soup.find_all('a',rel='commentFeed')
            for now_id in now_ids:
                if now_id['minid']!=2834108:
                    self.now_num = now_id['minid']
            key_list='list_li_'+str(self.now_num)
            span_id = 'longText-'+str(self.now_num)
            #获取内容
            #如果limit>1时这里需要循环
            content = soup.find('li',class_='lineD_btm char_info',id=key_list)

            #解析部分文档
            if content !=None:
                #获取长直播
                element=soup.find('span',id=span_id)
                if element == None:
                    #获取短博文
                    i = 0
                    elements = soup.find_all('div',class_='a_line')
                    for element in elements:
                        if i !=0:
                            print(element)
                            break
                        i = i + 1
                self.newText = element.get_text(strip=True)
                self.newText = self.newText.strip('[刘鹏程SaiL直播]')
            #查看原图
            img_child = soup.find('img',class_='ico_original')
            if img_child != None:
                img = img_child.parent
                writeImg(img['href'])
            #点击查看原图
            imgs = soup.find_all('a',class_='check')
            for img in imgs:
                writeImg(img['href'])

'''
发送QQ邮箱通知
'''
import time
import configparser
config = configparser.ConfigParser()
config.read('GetLiuMaibo.cfg')
print(config.sections())
from email.mime.text import MIMEText
import smtplib
import mimetypes
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
#发送邮件带图片
class email():
    filepath='E:/PYWork/awesome-python3-webapp/www/WeiBoImg/'
    def attach_img(self,img):
        if img != None:
            ctype,encoding = mimetypes.guess_type(img)
            if ctype is None or encoding is not None:
                ctype='application/octet-stream'
            maintype,subtype=ctype.split('/',1)
            #print(subtype)
            with open(img,'rb') as file:
                return MIMEImage(file.read(),_subtype=subtype)
    def sendMail(self,content,imgs):
        #生成MIME文档
        msg = MIMEMultipart()
        #date
        msg['From']=Header('autocrawl','utf-8')
        msg['Date']=formatdate()
        #文件主题
        msg['Subject']=Header('直播'+getNowTime(),'utf-8')
        #文本内容
        msg.attach(MIMEText(_text=content,_charset='utf-8'))
        #图片
        for img in imgs:
            file_msg=attach_img(img)
            #发送图片文件参数
            file_msg.add_header('Content-Disposition','attachment',
                        filename=os.path.split(img)[-1])
            #发送人
            msg.attach(file_msg)
        fromaddr=config.get('emailInfo','fromaddr')
        #发送密码
        password=config.get('emailInfo','password')
        #发送方的smtp服务，查看发送邮箱服务是否已经开启了SMTP服务
        stmp_server='smtp.qq.com'
        #目标邮箱
        to_addr=config.get('emailInfo','to_addr')
        #开始服务端口
        server =smtplib.SMTP(stmp_server,25)
        #server.set_debuglevel(1)
        #登陆
        server.login(fromaddr,password)
        #发送
        server.sendmail(fromaddr,to_addr,msg.as_string())
        #退出
        server.quit()


crawl = crawlLiuMaibo()
crawl.crawLastest()
#print(crawl.newText)
#print(crawl.now_num)
mail = email()
mail.sendMail(crawl.newText,crawl.Imgs)
def getCurTime():
    return time.localtime(time.time())

#开启一个进程作业


#print(config.sections())
org_num = config.get('info','last_num')
timesleep= config.get('info','timeSleep')
def save(org_num):
    config.set('info','last_num',org_num)
    config.write(open('GetLiuMaibo.cfg','w'))
def ownCalcMail():
    crawl = crawlLiuMaibo()
    crawl.crawLastest()
    nw = getCurTime()
    print(nw.tm_hour)
    #当小时数大于16退出
    while nw.tm_hour <16 :
        global org_num
        #当id不同时需要发送内容
        if crawl.now_num != org_num:
            mail = email()
            mail.sendMail(crawl.newText,crawl.Imgs)
            #global org_num
            org_num = crawl.now_num
            print('发送新邮件...')
            save(org_num)
            time.sleep(int(timesleep)*30)
        else:
        #一样的,不需要发送
            print('无变化,进入15分钟睡眠')
            time.sleep(int(timesleep)*15)
        nw = getCurTime()
    print('当日的任务已经不需要继续采集')
    return False
#每天
isLoop=True
while isLoop:
    isLoop = ownCalcMail()
