'''
该文件主要作用:采集http://www.imaibo.net/space/1954702更新，
当发现有自上一次采集的新内容时,将新的内容采集下来并打印出来
'''
import time
import configparser
import os
import OwnTime as ot

config = configparser.ConfigParser()
config.read('GetLiuMaibo.cfg')
org_num = config.get('info','last_num')
timesleep= config.get('info','timeSleep')
def save(org_num):
    if config.get('info','last_num') !=org_num:
        config.set('info','last_num',org_num)
        config.write(open('GetLiuMaibo.cfg','w'))
def saveDate(date):
    if config.get('autoTotal','date') !=date:
        config.set('autoTotal','date',date)
        config.write(open('GetLiuMaibo.cfg','w'))
emailContext=None
#获取时间戳
def getNowTime():
    return time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
From='autocrawl'
Subject='直播'+getNowTime()
#print(getNowTime())
from bs4 import BeautifulSoup
import requests
from bs4 import SoupStrainer
class crawlLiuMaibo():
    url='http://www.imaibo.net/space/1954702'
    params={
        'app':'home',
        'mod':'Space',
        'act':'getSpaceWeibo300',
        'uid':1954702,
        'limit':20,
        'p':1,
        'lastId':0,
        'syncShareSpaceWeiboId':0
    }


    #返回编码方式
    #print(response.encoding)
    #打印内容
    #print(response.text)

    #print(py_obj)
    #import json
    #print('..........')
    #将json格式数据转换成python对象loads,类同于.json()
    #py_obj1 = json.loads(response.text)
    #print(json_obj)
    #print(py_obj == py_obj1)
    #其实已经是部分文档了
    now_nums=set()
    lastId=org_num
    newText=None
    Imgs=set([])
    #写入本地图片文件夹中
    def writeImg(self,imgurl):
        if imgurl !=None:
            filename=imgurl[-17:-4]
            #print(filename)
            suffix=imgurl[-4:]
            #   print(suffix)
            img = "WeiBoImg/"+filename+suffix
            self.Imgs.add(img)
            if os.path.exists(img):
                return
            else:
                newimg=requests.get(imgurl)
                with open(img,'wb') as file:
                    file.write(newimg.content)



    def crawLastest(self):
        #清空上一次的图nows记录
        self.Imgs.clear()
        self.now_nums.clear()
        #获取记录
        self.lastId = config.get('info','last_num')
        print("wenjian ",self.lastId)

        #self.params['lastId']=org_num
        response = requests.get(self.url,params=self.params)
        #内置json解析器,帮助处理json数据,返回python数据
        py_obj = response.json()
        #响应内容
        if response.status_code == requests.codes.ok:
            #响应成功将尝试采集内容
            lists = py_obj['data']['weibo_lists']
            soup = BeautifulSoup(lists,'html5lib')
            #print(soup.prettify())
            now_ids = soup.find_all('a',rel='commentFeed')
            #收集需要采集的消息队列
            for now_id in now_ids:
                if now_id['minid']!=2834108 and now_id['minid'] >self.lastId :
                    self.now_nums.add(now_id['minid'])
            print(self.now_nums)
            for now_num in self.now_nums:
                key_list='list_li_'+str(now_num)
                span_id = 'longText-'+str(now_num)
                #清空上一次的图记录
                self.Imgs.clear()

                #获取内容
                #如果limit>1时这里需要循环
                content = soup.find('li',class_='lineD_btm char_info',id=key_list)
                #仅仅解析content内容
                only_tags_with_key_list = SoupStrainer('li',class_='lineD_btm char_info',id=key_list)
                #缩小查找范围
                soup1 = BeautifulSoup(lists,'lxml',parse_only=only_tags_with_key_list)
                #解析部分文档
                if content !=None:
                    #获取长直播
                    element=soup1.find('span',id=span_id)
                    if element == None:
                        #获取短博文
                        i = 0
                        elements = soup1.find_all('div',class_='a_line')
                        for element in elements:
                            if i !=0:
                                #print(element)
                                break
                            i = i + 1
                    self.newText = element.get_text(strip=True)
                    self.newText = self.newText.strip('[刘鹏程SaiL直播]')
                    #追加时间
                    href='http://www.imaibo.net/weibo/'+str(now_num)
                    tim = soup1.find('a',href=href)
                    if tim is not None:
                        self.newText = tim.get_text()+'\n\r'+self.newText
                print('内容',self.newText)
                #查看原图
                img_child = soup1.find('img',class_='ico_original')
                if img_child != None:
                    img = img_child.parent
                    self.writeImg(img['href'])
                #print('查看原图',self.Imgs)
                #点击查看原图
                imgs = soup1.find_all('a',class_='check')
                for img in imgs:
                    self.writeImg(img['href'])
                print('图片',self.Imgs)

                #发送邮件
                mail = email()
                From='autocrawl'
                Subject='直播'+getNowTime()
                mail.sendMail(self.newText,self.Imgs)
                self.lastId = now_num
                #print(self.newText)
            #循环完成后自动将最后一个值保存到记录中
            save(self.lastId)
            #print('保存',self.lastId)

'''
发送QQ邮箱通知
'''

#print(config.sections())
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
    #生成MIME文档

    def attach_img(self,img):
        if img != None:
            ctype,encoding = mimetypes.guess_type(img)
            if ctype is None or encoding is not None:
                ctype='application/octet-stream'
            maintype,subtype=ctype.split('/',1)
            #print(subtype)
            with open(img,'rb') as file:
                return MIMEImage(file.read(),_subtype=subtype)
    def sendMail(self,content,imgs,subtype='plain'):
        msg = MIMEMultipart()
        msg['From']=From
        #文件主题
        msg['Subject']=Subject
        #date
        msg['Date']=formatdate()
        #文本内容

        msg.attach(MIMEText(_text=content,_charset='utf-8',_subtype=subtype))
        #图片
        for img in imgs:
            file_msg=self.attach_img(img)
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
        to_addr=config.get('emailInfo','to_addr').split(',')
        #开始服务端口
        server =smtplib.SMTP(stmp_server,25)
        #server.set_debuglevel(1)
        #登陆
        server.login(fromaddr,password)
        #发送
        server.sendmail(fromaddr,to_addr,msg.as_string())
        #退出
        server.quit()

'''
crawl = crawlLiuMaibo()
crawl.crawLastest()
#print(crawl.newText)
'''
import MySqlTest as mst
import DBOperation as db

#获取最新的日线各种统计
def GetLastestTotal():
    #尝试下载最新数据
    org_date=config.get('autoTotal','date')
    db.DownLoadlastest()
    #获取最近天的数据从DB
    date,dayframe=mst.GetMyDBDate()
    #写入本地文件
    if org_date !=date:
        mst.WriteDataToExcel(date,dayframe)
        mail = email()
        From='autoTotal'
        Subject= date+'统计'

        m = dayframe.to_html('a.html')
        with open('a.html') as file:
            text = file.read()
            mail.sendMail(text,[],subtype='html')
        saveDate(date)

#mail.sendMail(text,[])



def getCurTime():
    return time.localtime(time.time())

#开启一个进程作业


#print(config.sections())

def ownCalcMail():
    crawl = crawlLiuMaibo()
    #crawl.crawLastest()
    nw = getCurTime()
    print(nw.tm_hour)
    #当小时数大于16退出
    while nw.tm_hour <16 and nw.tm_hour > 8:
        global org_num
        #当id不同时需要发送内容
        print(ot.GetNowHmDate(),'检查当前crawl.now_num ',crawl.lastId,'org_num',org_num)

        crawl.crawLastest()

        print('睡一会儿15分钟')
        time.sleep(int(timesleep)*15)
        nw = getCurTime()
    print('当日的微博任务已经不需要继续采集')
    #当小时数等于16
    while nw.tm_hour == 16:
        print('开始采集日期的统计情况...',ot.GetNowHmDate())
        GetLastestTotal()
        print('已经采集完全.....需要退出')
        break
        nw = getCurTime()
    return False
#每天

isInnerLoop=True
while isInnerLoop:
    isInnerLoop = ownCalcMail()
