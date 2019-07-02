# -*- coding: utf-8 -*-
#coding: utf-8

import os,sys,re,json,argparse,brotli,urllib3,base64
from urllib3 import HTTPResponse

from urllib import parse as urlencode
from bs4 import BeautifulSoup

import selenium
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
import selenium.common 


# 这个应该是广告接口
#https://www.zhihu.com/api/v4/search/preset_words?w=

# 知乎查询某个人的账户信息
#https://api.zhihu.com/people/bd5b8b010bfd51a86a60c87d7cfa810a

#查询某篇文章
#https://api.zhihu.com/articles/65142588

# 某个话题
#https://api.zhihu.com/topics/19551147

# 获取某个视频
#https://lens.zhihu.com/api/v4/videos/1115623205829926912

# 获取某个问题
#https://www.zhihu.com/api/v4/questions/323976342/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset=5&platform=desktop&sort_by=default
# 知乎文章评论
#https://www.zhihu.com/api/v4/articles/21711639/root_comments?order=normal&limit=20&offset=0&status=open
# 21711639 专栏id
# order 排序方式
# limit 每页的评论数量 必须小于 20
# offset += limit
#https://zhuanlan.zhihu.com/p/68443139 知乎专栏

urllib3.disable_warnings()

class Zhihu(object):
    def __init__(self):

        self.download_headers = {
            'Accept-Encoding': 'identity;q=1, *;q=0',
            'chrome-proxy': 'frfr',
            'Range': 'bytes=0-',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        } 

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        
        self.path = os.path.curdir+'/data'
        self.author = ''
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.http = urllib3.PoolManager()

        self.index = 0
        self.totals = 0
        self.author = ''

        self.question = ''
        #self.driver = Chrome()
        #self.options = self.driver.create_options()
        
        self.is_end = False
        pass

    def title(self,t):
        t = str(t)
        if t is None:
            self.index  = self.index + 1
            return self.index 

        for i in u"《》 ，？！。 【】（）%￥~‘’“”、|*：；\"',:!?|()$*&;.--「」～":
            t = t.replace(i,'')
        return t
    
    def genarate_path(self,author,):
        
        author.replace(' ','')

        path = self.path + "/" + author
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def downlaod_video(self,url,title):
        path = self.path + '/' + self.author
        if  not os.path.exists(path):
            os.mkdir(path)
        
        if title is None:
            file_name = self.path +'/'+ self.author +'/'+ str(self.totals) + '.mp4'
        else:
            title = self.title(title)
            file_name = self.path +'/'+ self.author +'/' + title + '.mp4'
        #print(file_name)
        if os.path.exists(file_name):
            return

        response =self.http.request("GET",url,self.download_headers)
        #print(response.status)

        with open(file_name,"wb") as f:
            size = f.write(response.data)
            f.flush()
            f.close()
            self.totals += 1
        
        print(self.totals,"\t",file_name,"\nFile size : \t%d MB" %(int(size/1024/1024)))
              
   
    def download_text(self,content):
        bs = BeautifulSoup(content,"lxml")
        p = bs.find('p')
        #Ebs.next_element
        #print("p : \t",p.text,"\n\n")
        #print(" \t",bs.next_element)     
        pass

    def search_video_url(self,video_id):
        '''
            https://lens.zhihu.com/api/v4/videos/1115623205829926912
            搜索某个视频地址根据视频 id
        '''
        url = "https://lens.zhihu.com/api/v4/videos/{}".format(video_id)

        response = self.http.request("GET",url)

        try:
            data = json.loads(response.data.decode())
            playlist = data['playlist']
            #print("data: \t",data,"\nplaylist : \t",playlist,'\n','title: \t',data['title'])
            title = self.title(data['title'])
            #print('title : \t',title,'\n')
            if "SD" in playlist.keys():
                video_url = playlist['SD']['play_url']
            else:
                video_url = playlist['LD']["play_url"]
                
            #print("status : \t",response.status,"\ncontent-type: \t" ,response.headers["content-type"],"\nurl : \t",url,'\nvideo_url : \t',video_url)
            self.downlaod_video(video_url,title)
        except:
            pass

    def search_people_v1(self,keyword):

        pattern = re.compile(r"https\://www\.zhihu\.com/people/(.*)",re.S)
        search_url = "https://www.zhihu.com/search?type=people&q=%s" %(str(urlencode.quote(keyword)))
        data = ''
        try:
            self.driver.get(search_url)
            a_list = self.driver.find_elements_by_xpath("//a[@class='UserLink-link']")
            cookie = self.driver.execute_script('return document.cookie')
            print(cookie)
            data = pattern.findall(a_list[0].get_attribute('href'))

        except Exception as e:
            print(e)
            pass
        return data[0]
    
    def search_people_v2(self,people):
        search_url = "https://www.zhihu.com/api/v4/search_v3?t=people&q={}&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0".format(urlencode.quote(people))
        self.author = str(people)
        response = self.http.request("GET",search_url,headers=self.headers)
    
        if 'br' in response.headers['content-encoding']:
            data = brotli.decompress(response.data).decode()
            data = json.loads(data)
            for per in data['data']: 

                if 'object' in per.keys():
                    obejct = per['object']
                    person_url = obejct['url']
                    url_token  = obejct['url_token']
                    name = obejct['name']
                    print('name : \t',name,'\nurl: \t',person_url,"\nurl_token : \t",url_token)
                    if self.author in name:
                        print("attach_info : \n\t",base64.standard_b64decode(obejct['attached_info_bytes']),'\n')
                        return person_url,url_token
                    else:
                        search_url = data['paging']['next']
        else:
            print("status : \t",response.status,"\ncontent-encoding : \t",response.headers['content-encoding'],"\ncontent-type: \t",response.headers['content-type'])

        return None,None

    def search_page_v1(self,url_token):
        # session_id 1023617413325172736
        #            1081194882223087616
        url = "https://www.zhihu.com/api/v4/members/{}/activities?limit=7&session_id=1081194882223087616&after_id=1557624320&desktop=true".format(url_token)

        while True:

            if self.is_end:
                print("Not data response,exiting ... \n")
                #self.driver.close()
                break
            
            try:
                #self.driver.get(url)
                #res = self.driver.find_elements_by_xpath("//pre")
                #response = res[0].text
                response = self.http.request("GET",url,self.headers)
            except KeyError as e: 
                print("The Header Not has keyword=",e)
            
            if 'json' in response.headers['content-type']:
                data =  response.data #brotli.decompress(response.data).decode()
                try:
                    jsons = json.loads(data)

                    page = jsons['paging']
                    self.is_end = bool(page['is_end'])
                    url = page['next']
                    
                    page_data = jsons['data']
                    for i in page_data:
                        
                        target = i['target']
                        if 'title' in target.keys():
                            title = target['title']
                        elif 'question' in target.keys():
                            # 这里是发表在别人的提问中的。
                            title = target['question']['author']['name']+ str(target['created_time'])
                            continue

                        if 'thumbnail_extra_info' in target.keys():
                            thumbs = target['thumbnail_extra_info'] 

                            playlist = thumbs['playlist']
                        
                            video_url = playlist['sd']['url']
                            title = self.title(title)
                        
                            if video_url :
                                self.downlaod_video(video_url,title)
                        else:
                            content = target['content']
                            #print(content)
                            # 保存为markdown
                            self.download_text(content)
                except Exception as e:
                    #elf.driver.close()
                    pass
            else:
                print("\n===================================================")
                print("status : \t",response.status)
                print('----------------HLEP ME ----------------------------\n')
        pass


    def search_video_quetions(self,search_url):
        '''
            搜索某个问题下的所有发的视频
        '''
        #search_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset=5&platform=desktop&sort_by=default".format(question_id)
        pattern = re.compile(r"//www\.zhihu\.com/video/([0-9]+)")
        response = self.http.request("GET",search_url)
        print("status : \t",response.status,"\ncontent-type: \t" ,response.headers["content-type"],"\nurl : \t",search_url,'\n')

        if 'json' in response.headers['content-type']:
            data = json.loads(response.data.decode())
            try:
                page = data['paging']
                is_end = page['is_end']
                is_start = page['is_start']
                if is_end or is_start:
                    self.is_end = True
                    return
                search_url = page['next']

                data = data['data']

                #for d in data:
                #print(data)

                for anwser in data:
                    #print(anwser)
                    self.author = anwser['author']['name']
                    self.question = anwser['question']['title']
                    self.question = self.title(self.question)
                    if "content" in anwser.keys():
                        content = anwser['content']
                            #print("content : \t",content,'\n')
                        videos = pattern.findall(content)
                        #print("video : \t",videos,'\n')
                        for id in videos:
                            self.search_video_url(id)

                
                self.search_video_quetions(search_url)
            except Exception as e:
                print(e)
                pass

    def start_app(self,keyword,enable):
        if not os.path.exists(self.path + "/" + str(keyword)):
            os.mkdir(self.path + "/" + str(keyword))
        self.author = str(keyword)
        person_url,user_token = self.search_people_v2(keyword)
        if user_token is not None:
            self.search_page_v1(user_token)
        else:
            print("author : \t",self.author,"\nperson_url : \t",person_url,"\nuser_token: \t",user_token)
        pass 

    def exit_app(self):
        while True:
            if self.is_end:
                break


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    
    parse = argparse.ArgumentParser()
    parse.add_argument("-type",'--type',required=True,help=("Search type : question = 1,articel = 2,people = 3"),type=int)
    parse.add_argument('-enable-video','--video',help=('download video'),type=bool,default=True)
    parse.add_argument('-q','--question',help=("Input question id"))
    parse.add_argument('-k','--keyword',help=('-k author name'))
    
    args = parse.parse_args()
    
    app = Zhihu()

    if args.type == 1:
        #args = parse.parse_args()
        search_url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled,is_recognized,paid_info;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics&limit=5&offset=5&platform=desktop&sort_by=default".format(args.question)
        app.search_video_quetions(search_url)
    elif args.type == 2:
        pass
    elif args.type == 3:
        #args = parse.parse_args()        
        app.start_app(args.keyword,args.video)

    #app.exit_app()
    