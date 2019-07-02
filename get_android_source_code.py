import os
import sys
import time
import signal

import _thread
import threading

from collections import deque

from bs4 import BeautifulSoup
import lxml
import urllib
import urllib.request
import urllib.response
import urllib.parse
import urllib.error

quene = deque()
temp_quene = deque()
download_urls = deque()
is_stop = 0
url = "http://androidxref.com/7.1.1_r6/xref/"
headers ={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
            "Referer": "http://androidxref.com/",
            "Upgrade-Insecure-Requests": 1
        } 

modules = ["frameworks","system","ndk"]
lock = threading.Lock()

downdload_lock = threading.Lock()

start = 0

#quene.append(url)
quene.append(url+"frameworks/")
#quene.append("http://androidxref.com/7.1.1_r6/xref/frameworks/compile/mclinker/lib/Support/")
# 保存为下载完的文件
def save_file(is_stop,url):
    with open("download_url.txt","wb") as f:
        if url:
            f.write(url +'\n')
            

        while download_urls:
            url = download_urls.popleft()
            f.write(url + '\n')

        f.close()

#def save_download_urls(url):


def signal_handle(signum,t):

    global is_stop
    if signum == signal.SIGINT:
        is_stop = 1
        # save urls into file
        with open("parser_urls.txt","wb") as f :
            while quene:
                f.write(quene.popleft())
                f.write('\n')
            f.close()
        with open("download_urls.txt","wb") as f:
            while temp_quene:
                f.write(temp_quene.popleft())
                f.write('\n')
            f.close()
        with open("file_urls.txt","wb"):
            while download_urls:
                f.write(download_urls.popleft())
                f.write('\n')
            f.close()
        
            
        
    
def prase_dir(url):
    #.\\androidxref.com\7.1.1_r6\raw\
    p = []
    path = urllib.request.url2pathname(url)
    path = path.split(':')[1]
    # windows path //, linux  path \
    dirs = path.split('\\')

    l = len(dirs[len(dirs) - 1])
    p.append(path[:-l])
    p.append(dirs[len(dirs)-1])
    return p


def paser_urls(name):
    
    url_ = ""
    url_1 = ""
    data  = []
    while is_stop == 0:
       # lock.acquire()
        if quene:
            url_ = quene.popleft()
        else:
            continue
        #lock.release()

        print("url : ",url_)
        if len(url_) == 0:
            continue
        # 请求 url
        try:
            request = urllib.request.Request(url_,headers=headers)
            op = urllib.request.urlopen(request)
            print(op.status)
            data = op.read()
        except urllib.error.HTTPError as e:
            print("url_",url_,"Http error : ",e.code,e.reason)

            #所有http error 重新加入连接
            quene.append(url_)
            with open("http_err.txt","wb") as f:
                f.write(str(e.reason))
                f.write(" url :")
                f.write(str(url_))
                f.write('\n')
                f.close()

        except urllib.error.URLError as e:
            print("Url error : ",e.reason)
            with open("url_err.txt","wb") as f:
                f.write(str(url_))
                f.write(str(e.reason))
                f.write('\n')
                f.close()
        finally :
           #print("others exception")
           pass

        if op.status != 200:
            quene.append(url_)
            continue
    
        headers['Referer'] = url
    
    
        soup = BeautifulSoup(data,"lxml")
        
        #divs = soup.find_all('div')
        tables = soup.find_all('table',id="dirlist")

        # 解析页面所有页面url
        for table in tables:
            if table['id'] == "dirlist": 
                tbody = table.tbody
                for tr in tbody.find_all('tr'):
                    p = tr.p 
                    a = tr.a               
                    if p['class'][0] == 'r':
                        if ".." == a.get_text():
                            pass
                        else:
                            url_1 = url_ +a.get_text() + "/"
                            quene.append(url_1)

                    elif p['class'][0] == 'p':
                        url_1 = url_ + a.get_text() + "/"
                        temp_quene.append(url_1)
                    else:
                        pass
   
    print("Parser url thread exit : ",name)
    ''' 
        is_download = soup.find_all('span',id='download')
        if len(is_download) <= 0:
            continue

        # 下载文件                   
        for div in divs:
            if div['id'] == 'bar':
                lis = div.find_all('li')
                for li in lis:
                    hrefs = li.find_all('a')
                    for a in hrefs:
                        href = a['href']
                        spans = a.find_all('span')

                        for span in spans:
                            if span.get('id') == "download":

                                download_url = "http://androidxref.com" + href
                                download_urls.append(download_url)
    '''
       


def parser_download_url(name):
    
    global is_stop
    while is_stop == 0:
       # lock.acquire()
        if temp_quene:
            url_ = temp_quene.popleft()
        else:
            continue
        #lock.release()

        print("url : ",url_)
        if len(url_) == 0:
            continue
        # 请求 url
        try:
            request = urllib.request.Request(url_,headers=headers)
            op = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print("url_",url_,"Http error : ",e.code,e.reason)

            #所有http error 重新加入连接
            #if e.code == 404
            temp_quene.append(url_)
            with open("http_err.txt","wb") as f:
                f.write(e.msg + " url: ")
                f.write(url_)
                f.write('\n')
                f.close()

        except urllib.error.URLError as e:
            print("Url error : ",e.reason)
            with open("url_err.txt","wb") as f:
                f.write(url_)
                f.write(e.msg)
                f.write('\n')
                f.close()
        finally :
           #print("others exception")
           pass

           soup = BeautifulSoup(op.read(),"lxml")

           divs = soup.find_all("div",id="bar")
           #print(divs)
           # 下载文件                   
           for div in divs:
                if div['id'] == 'bar':
                    lis = div.find_all('li')
                    for li in lis:
                        hrefs = li.find_all('a')
                        for a in hrefs:
                            href = a['href']
                            spans = a.find_all('span')

                            for span in spans:
                                if span.get('id') == "download":

                                    download_url = "http://androidxref.com" + href
                                    download_urls.append(download_url)
        

def download_file(name):

    global is_stop
    while is_stop == 0: 

        time.sleep(0.05)
        
        if(is_stop):
            print("download thread  exit ...")
            break
        
        if download_urls:
            download_url = download_urls.popleft()


            print("download url : ",download_url)
            #download_url = download_urls.popleft()
            #解析url 得到文件路径和名字
            p = prase_dir(download_url)
        
            dir = p[0]
            file_name = p[1]
            dir = os.path.curdir +"\\"+dir
                            
            # 解析url 得到文件路径
            if not os.path.exists(dir):
                os.makedirs(dir)

            file_name = dir + file_name
            if os.access(file_name,os.F_OK):
                continue    
            print("saved  file : ",os.path.abspath("."),file_name)
            
            try:
                request = urllib.request.urlopen(download_url)
                pass
            except urllib.error.HTTPError as e:
                print("code ",e.code,"reason ",e.reason)
                with open("download-urls.txt","w+") as f :
                    f.write(str(download_url))
                    f.write('\n')
                    f.close()
                pass
                    


            with open(file_name,"wb") as f :
                f.write(request.read())
                f.close()
        else :
            continue
    

if __name__ == "__main__":
    
    #_thread.start_new_thread(paser_urls,("thread-1",))
    #_thread.start_new_thread(download_file,("thread-2",))

    # 对 ctrl + c 进行处理 
    threads = []
    signal.signal(signal.SIGINT,signal_handle)
    
    for i in range(0,5):
        t = threading.Thread(target=paser_urls,name="url",args=("Thread",))
        t.setDaemon(True)
        t.start()
        threads.append(t)
        time.sleep(0.5)
    
    time.sleep(5)

    for i in range(0,2):
        t = threading.Thread(target=parser_download_url,name="parser_url",args=("download_q",))
        t.setDaemon(True)
        t.start()
        threads.append(t)


    time.sleep(3)
    for i in range(3):
        t = threading.Thread(target=download_file,args=("download",))
        t.setDaemon(True)
        t.start()
        threads.append(t)

        time.sleep(1)
    

    while is_stop == 0:
        pass
    
    print("main exit ... ")


'''
quene.append(url)

while quene:

    #url_ = quene.popleft()
    url_ = quene.popleft()
    print("get url : ",url_)
    # 请求 url
    try:
        request = urllib.request.Request(url_,headers=headers)
        #print("headers refer:  ",request.get_header("Referer"))
        #print("Request : ",request.data)
        op = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        print(e.msg)
    except urllib.error.URLError as e:
        print(e.msg)
    #finally:
     #   print("others exception")
    if op.status != 200:
        quene.append(url_)
        continue
    headers['Referer'] = url
    #op = urllib.request.urlopen(url_)

    data = op.read()

    soup = BeautifulSoup(data,"lxml")
    divs = soup.find_all('div')
    tables = soup.find_all('table')

    #print("divs : ",divs)
    #print("tables :",tables)
    #input()

    # 解析页面路径

    for table in tables:
        if table['id'] == "dirlist": 
            tbody = table.tbody
            #print("tbody :",tbody)
            for tr in tbody.find_all('tr'):
                p = tr.p 
                a = tr.a               
                if p['class'][0] == 'r':
                    if ".." == a.get_text():
                        pass
                    else:
                        url_1 = url_ +a.get_text() + "/"
                elif p['class'][0] == 'p':
                    url_1 = url_ + a.get_text() + "/"
                else:
                    pass

                quene.append(url_1)

    is_download = soup.find_all('span',id='download')
    if len(is_download) <= 0:
        continue

    # 下载文件                   
    for div in divs:
        if div['id'] == 'bar':
            lis = div.find_all('li')
            #print("lis : ",lis)
            for li in lis:
                hrefs = li.find_all('a')
                for a in hrefs:
                    href = a['href']
                    #print("href : ",a['href'])
                    spans = a.find_all('span')

                    #print("span :",spans)
                    for span in spans:
                        #print('span ',span)
                        if span.get('id') == "download":
                     
                            download_url = "http://androidxref.com/" + href 
                            #quene.append(download_url)
                            request = urllib.request.urlopen(download_url)
                    
                            #解析url 得到文件路径和名字
                            p = prase_dir(download_url)
                            #print("dir ",p[0])
                            #print("filename ",p[1])
                            dir = p[0]
                            file_name = p[1]
                            dir = os.path.curdir +"\\"+dir
                            #print('path : ',dir)
                            # 解析url 得到文件路径
                            if not os.path.exists(dir):
                                os.makedirs(dir)

                            file_name = dir + file_name
                            print("saved ",file_name)
                            with open(file_name,"wb") as f :
                                f.write(request.read())
                                f.close()
        else:
            #print("div['id'] = ",div["id"])
            pass
'''
    

    
