'''
找一个网页，例如https://www.python.org/events/python-events/，
用浏览器查看源码并复制，然后尝试解析一下HTML，输出Python官网发布的会议时间、名称和地点。
'''
from html.parser import HTMLParser
from html.entities import name2codepoint
import gobal


'''
这里利用文件分析找出会议的名称，时间，地点
缺点是:1.文件应该是分段打开的，比如一次打开20行
2.这里处理事情使用了全局变量，存在不安全使用
3.没有进一步优化匹配算法导致效率不高
'''
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        #print('%s %s',tag,attrs)

        if tag=='a' and len(attrs) > 0:
            for k,v in attrs:
                if k=='href' and '/events/python-events/' in v:
                    if v[-4:-1].isdigit():
                        gobal.IsMeeting = True
        elif tag=='time' and len(attrs) >0:
            for k,v in attrs:
                if k =='datetime':
                    #print(v)
                    gobal.IsMeeting = True
        elif tag=='span' and len(attrs) > 0:
            for k,v in attrs:
                if k == 'class' and v=='event-location':
                    gobal.IsMeeting = True
                else:
                    gobal.IsMeeting = False
                    #print('is meeting',ISMEETING)
        else:
            gobal.IsMeeting = False
    def handle_charref(self, name):
        print(name)
    def handle_data(self, data):

        #print('is meeting',ISMEETING)
        if gobal.IsMeeting == True:
            print(data)
    def handle_entityref(self, name):
        print('&#%s ' % name)

'''
改进版本不使用全局变量__is_meeting前面__代表该变量是私有变量
'''

class MyHTMLParser1(HTMLParser):
    __is_meeting = False
    #self表示创建的实例本身
    def handle_starttag(self, tag, attrs):
        #print('%s %s',tag,attrs)

        if tag=='a' and len(attrs) > 0:
            for k,v in attrs:
                if k=='href' and '/events/python-events/' in v:
                    if v[-4:-1].isdigit():
                        self.__is_meeting = True
        elif tag=='time' and len(attrs) >0:
            for k,v in attrs:
                if k =='datetime':
                    #print(v)
                    self.__is_meeting = True
        elif tag=='span' and len(attrs) > 0:
            for k,v in attrs:
                if k == 'class' and v=='event-location':
                    self.__is_meeting = True
                else:
                    self.__is_meeting = False
                    #print('is meeting',ISMEETING)
        else:
            self.__is_meeting = False
    def handle_charref(self, name):
        print(name)
    def handle_data(self, data):

        #print('is meeting',ISMEETING)
        if self.__is_meeting == True:
            print(data)
    def handle_entityref(self, name):
        print('&#%s ' % name)
'''
生成dict{'meeting name':'',...}
'''
class MyHTMLParser2(HTMLParser):
    is_meeting = False
    __Meetings =[]
    #self表示创建的实例本身
    def handle_starttag(self, tag, attrs):
        #print('%s %s',tag,attrs)

        if tag=='a' and len(attrs) > 0:
            for k,v in attrs:
                if k=='href' and '/events/python-events/' in v:
                    if v[-4:-1].isdigit():
                        self.is_meeting = True
                    else:
                        self.is_meeting = False
                else:
                       self.is_meeting = False
        elif tag=='time' and len(attrs) >0:
            for k,v in attrs:
                if k =='datetime':
                    #print(v)
                    self.is_meeting = True
                else:
                    self.is_meeting = False
        elif tag=='span' and len(attrs) > 0:
            for k,v in attrs:
                if k == 'class' and v=='event-location':
                    self.is_meeting = True
                else:
                    self.is_meeting = False


        else:
            self.is_meeting = False
    def handle_charref(self, name):
        print(name)
    def handle_data(self, data):

        #print('is meeting',ISMEETING)
        if self.is_meeting == True:
            self.__Meetings.append(data)
            #print(data)
    def handle_entityref(self, name):
        print('&#%s ' % name)
    def Show(self):

        for k in self.__Meetings:

            print( k)

        #print('self meetings %s...' % self.__Meetings)
import urllib.request,io,os,sys
url='https://www.python.org/events/python-events/'
req = urllib.request.Request(url)
f = urllib.request.urlopen(req)
s = f.read()
s = s.decode('utf-8')
with open('admint.txt','w',100,'utf-8') as file:
    file.write(s)


parser = MyHTMLParser2()
for line in open('admint.txt','r'):
    parser.feed(line.strip())
parser.Show()
parser.close()
