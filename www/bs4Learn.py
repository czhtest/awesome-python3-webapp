from bs4 import BeautifulSoup
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
soup = BeautifulSoup(html_doc)
print(soup.prettify())
print(soup.title)

for link in soup.find_all('a'):
    print(link.get('href'))

print(soup.get_text())

import urllib.request

#获取网页
url='https://www.python.org/events/python-events/'
#req = urllib.request.Request(url)
#f = urllib.request.urlopen(req)
#contexts = f.read()
#urllib.request.urlretrieve(url,'test.html')
soup = BeautifulSoup(open('test.html'))
#print(soup.prettify())
print ('.............................................................')
names=[]
times=[]
locations=[]
for name in soup.find_all('h3',class_='event-title'):
    print('name:',name.string)
    names.append(name.get_text())
for time in soup.find_all('time',datetime=True):
    print('Time:',time.get_text())
    times.append(time.get_text())
for loc in soup.find_all('span',class_='event-location'):
    print('Location:',loc.get_text())
    locations.append(loc.get_text())
i=0
for name in names:
    print('Name:',name,'\r\nTime:',times[i],'\r\nLoc:',locations[i])
    i = i + 1

