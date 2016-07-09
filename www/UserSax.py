'''
操作xml有两种方法dom和sax,dom比较耗费内存,解析慢
sax是流模式，边读边解析，
start_element ,end_element,char_data
'''
from xml.parsers.expat import ParserCreate

class DefaultSaxHandler(object):
    def start_element(self,name,attrs):
        print('sax:start_element:%s,attrs:%s' % (name,str(attrs)))
    def end_element(self,name):
        print('sax:end_element:%s' % name)

    def char_data(self,text):
        print('sax:char_data:%s' % text)


xml = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''
handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)

'''
html解析用html parser
'''
from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print('start<%s %s>' % (tag,attrs))
        for k,v in attrs:
            print(k,'=',v)
    def handle_endtag(self, tag):
        print('end<%s>' % tag)
    def handle_startendtag(self, tag, attrs):
        print('sted<%s>' % tag)

    def handle_data(self, data):
        print('data',data)
    def handle_comment(self, data):
        print('<!--',data,'--!>')
    def handle_entityref(self, name):
        print('%s &#%s ' % ('entityref',name))
    def handle_charref(self, name):
        print(' &#%s' % name)

parser = MyHTMLParser()
parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
    <p class="give-me-more"><a href="?page=2" title="More Events">More</a></p>
</body></html>''')
parser.close()
'''
feed()方法可以多次调用，也就是不一定一次把整个HTML字符串都塞进去，可以一部分一部分塞进去。

特殊字符有两种，一种是英文表示的&nbsp;，一种是数字表示的&#1234;，这两种字符都可以通过Parser解析出来
'''
var = '/events/python-events/427/'
print(var[-4:-1].isdigit())