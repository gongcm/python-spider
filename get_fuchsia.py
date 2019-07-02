import os
import sys
import re
import urllib
import urllib.request
import urllib.response
import urllib.error
import ssl
from bs4 import BeautifulSoup
#import html5lib
from collections import deque
import lxml
quene = deque()

#url = "https://mirrors.hexang.com/fuchsia/"
url  = "http://androidxref.com/7.1.1_r6/xref/"
cur_path = os.path.abspath('.') + "\\7.1.1_r6"
url_2 = "http://androidxref.com/7.1.2_r36/raw/Android.bp"
types = []

def add_type(str):

    if str not in types:
        types.append(str)
    return types

quene.append(url)
while quene:


    url_ = quene.popleft()
    print("url open : ",url_)
    try:
        op = urllib.request.urlopen(url_2)
    except urllib.error.HTTPError as e:
        print(" 404 Not found ")
    except urllib.error.URLError as e:
        print(e.code)
    finally:
        print("others exception")

     # 找不到的直接pass掉   
    if op.status != 200:
        continue

    data = op.read()
    print(data)

    input()
    soup = BeautifulSoup(data,"lxml")
    
    print("table : ",soup.table)
    print("tbody : ",soup.tbody)
    tag = soup.table
    print("type table : ",type(soup.table))
    print("tag name : ",tag.name)
    print("tag id : ",tag['id'])
    print("tag tag : ",tag.tbody)
    print("tbody tr : ",tag.tbody.find_all('tr'))

    for tr in tag.tbody.find_all('tr'):
        print("tr : ",tr)
        print("p class",tr.p['class'])
        if tr.p['class'] == 'r':
            
        #print("a href",tr.a['href'])

   # input()

    #if soup.table['id'] == 'dirlist':
        #for i in tag.
    #input()
    #print("")
    tbody = soup.tbody
    href = ''
    for href in tbody.find_all('a'):
        text = href.get_text()
        if text != "../":
            url_1 = url_+ href.get_text()
            if url_1:
                print(url_1)
                quene.append(url_1)

    #input()
    #解析url  路径
    split_str = url_.split('/')
    index = split_str.index("xref")
    split_str = split_str[index + 1:len(split_str)]
    
    sub_modules = []
    for i in split_str:
        if i !='':
            sub_modules.append(i)
        else:
            pass
        
    print("sub_moudles : ",sub_modules)
    sub_path = ''
    
    if len(sub_modules) != 0:
        for i in sub_modules:
            sub_path += i
            sub_path += "\\"
            print(sub_path)
    else:
        sub_path = ''

    print("sub_path : ",sub_path)
    tp = op.getheader("Content-type")
    print(tp)
    types = add_type(tp)
    print("types : ",types)

    is_text = 0
    is_html = 0
    #这里可以根据不同的数据类型进行不同数据处理
    if 'text' in op.getheader("Content-type"):
        is_text = 1
    if "html" in op.getheader("Content-type"):
        is_html = 1
    
    if (is_html == 1) and (is_text == 1):
        sub_path = sub_path[:-1]
        abs_path = cur_path + "\\" + sub_path
        print("save file ",abs_path)
        with open(abs_path,"wb") as f:
            f.write(data)
            f.close()
    elif is_html == 1:
        path = cur_path +"\\"+ sub_path
        print("mkdir : ",path)
        if not os.path.exists(path):
            os.makedirs(path)
    else:
        print("pass sub_path : ",sub_path)
        pass
