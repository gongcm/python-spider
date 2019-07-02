# 英文验证码的登录方式
 
# 中文登录（点击倒立文字）
 
import requests,time,json
from hashlib import sha1
import hmac
 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Referer": "https://www.zhihu.com/signup?next=%2F",
    "origin": "https://www.zhihu.com",
    "Authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
    "Host": "www.zhihu.com"
}
 
# cookies的自动化管理。
# 获取的服务器的Set-Cookie用session直接自动解析并保存，在后续的请求中，会在请求头中自动携带这些cookie
# LWPCookieJar:对cookie进行自动操作，load() save()
# 英文验证码的登录方式
 
# 中文登录（点击倒立文字）
 
import requests,time,json
from hashlib import sha1
import hmac
 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
'''
authority: www.zhihu.com
:method: POST
:path: /api/v3/oauth/sign_in
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
content-length: 396
content-type: application/x-www-form-urlencoded
cookie: _xsrf=JS2TH6X5iqnK16Gt8U1f1FKcEAHU5z5v; _zap=9789dbba-b508-4901-bfa0-7637dfd23cc4; d_c0="AKDgVwQtAQ-PTvRzin9slQ-Y7aHP42wR9ds=|1550556947"; __utmv=51854390.100-1|2=registration_date=20140408=1^3=entry_date=20140408=1; tst=r; __gads=ID=77b5149e5a0010c4:T=1554104370:S=ALNI_MZ10901vo67rC_ZPQgfGiyhQ4aOGQ; q_c1=c7a30c4a34534c7e80193b195ef1859b|1554104382000|1550556954000; __utma=51854390.1794958275.1550557063.1554104384.1555646315.3; __utmz=51854390.1555646315.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; tgw_l7_route=a37704a413efa26cf3f23813004f1a3b; capsion_ticket="2|1:0|10:1556260640|14:capsion_ticket|44:MmE3NDBjYmU5Zjc2NDRiMGJlNmQ0YWM1ZTgyMDc3YmY=|e029244fc47bd6d5a51fac6a919017ce7f28a32f765922c7df4631d7a1403fe0"
origin: https://www.zhihu.com
referer: https://www.zhihu.com/signin?next=%2F
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36
x-ab-param: se_payconsult=0;se_zu_onebox=0;top_quality=0;top_user_cluster=0;se_colorfultab=0;se_likebutton=0;se_site_onebox=0;se_spb309=0;top_billupdate1=2;zr_art_rec=base;li_lt_tp_score=1;pf_noti_entry_num=0;top_ebook=0;top_native_answer=1;zr_article_rec_rank=truncate;top_recall_deep_user=1;ug_newtag=0;gw_guide=0;se_ad_index=10;se_amovietab=0;se_webmajorob=0;top_universalebook=1;top_zh_tailuser=1;ug_goodcomment_0=0;ug_zero_follow_0=0;se_expired_ob=0;se_whitelist=0;top_root=0;se_auto_syn=0;se_preset_tech=0;top_rank=0;tp_header_style=1;zr_video_rec_weight=close;top_gr_ab=0;top_new_feed=5;top_wonderful=1;pf_feed=1;se_page_limit_20=1;se_zu_recommend=0;tp_m_intro_re_topic=1;ug_follow_answerer_0=0;zr_km_material_buy=promotion;se_featured=0;top_recall_exp_v1=1;zr_ads_search=0;zr_answer_rec=close;top_hotcommerce=1;li_ts_sample=old;se_rewrite=0;se_websearch=3;soc_update=1;top_nucc=0;top_recall_exp_v2=1;top_vipoffice=1;zr_km_answer=base;ls_fmp4=0;se_billboardsearch=0;se_km_ad_locate=1;soc_bigone=0;top_vipconsume=1;li_se_ebook_chapter=1;se_agency= 0;se_movietab=0;se_p_slideshow=0;se_time_threshold=1.5;ug_goodcomment=0;se_click_wiki=0;se_ios_spb309=0;se_terminate=0;soc_bignew=1;top_reason=1;top_ydyq=X;tp_qa_metacard_top=top;pf_fuceng=1;top_new_user_rec=0;ug_zero_follow=0;zr_search_material=1;se_lottery=0;se_webtimebox=0;zr_feed_cf=1;qa_answerlist_ad=0;tp_sft_v2= a;tsp_childbillboard=1;ug_follow_topic_1=2;li_qa_cover=old;se_ltr_0419=0;se_webrs=1;se_search_feed=N;top_bill=0;top_v_album=1;tsp_lastread=0;ug_follow_answerer=0;li_es_new=new;li_tjys_ec_ab=0;qa_video_answer_list=0;top_ntr=1;pf_newguide_vertical=0;se_click_del=1;se_wannasearch=0;soc_special=0;tp_discussion_feed_type_android=2;tp_sft=a;tp_sticky_android=0;zr_ans_rec=gbrank;pf_creator_card=1;qa_web_answerlist_ad=1;se_title_only=0;zr_se_new_card=1;li_album_liutongab=0;li_se_intervene=1;li_se_new_card=1;pf_foltopic_usernum=50;qa_test=0;se_backsearch=0;tp_qa_metacard=1;ug_fw_answ_aut_1=0;se_famous= 0;se_rr=0;se_subtext=0;zr_infinity_topic=close;li_filter_ttl=2;se_se_index=1;top_test_4_liguangyi=1;zr_rel_search=base;zr_video_rec=zr_video_rec:base
x-requested-with: fetch
x-xsrftoken: JS2TH6X5iqnK16Gt8U1f1FKcEAHU5z5v
x-zse-83: 3_1.1
'''
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    "Referer": "https://www.zhihu.com/signup?next=%2F",
    "origin": "https://www.zhihu.com",
    "Authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
    "Host": "www.zhihu.com"
}
 
 
# cookies的自动化管理。
# 获取的服务器的Set-Cookie用session直接自动解析并保存，在后续的请求中，会在请求头中自动携带这些cookie
# LWPCookieJar:对cookie进行自动操作，load() save()
from http.cookiejar import LWPCookieJar
 
session = requests.Session()
session.cookies = LWPCookieJar(filename='zhihucookie.txt')
 
try:
    session.cookies.load(filename='zhihucookie.txt', ignore_expires=True, ignore_discard=True)
except Exception as e:
    print('暂时没有Cookie')
 
# res = session.get('https://www.zhihu.com/', headers=headers, verify=False)
# print(res)
 
def decode():
    str='T__pNKpx8hfrJlRvspv2QGoh02euKtuzu6epNKpx8hfrJlRv4tA1QGohIlu4NsMxvdezQGohclbf66Qwl-vw8X5k0g8bTkrkslQxcDoh9hBtRlR1w-BlMK-lP1bbO_Nlj9rlLW_mahbbMsapisqxH60zMtAqPx8k118l7DtmOkNuQ_Nl-oukQOowSgua6-8l_grwPG5kA68b928l-wexK5_pNsavMtf2wTQxDD9lMsMu02Bjk6uyCl9jHXAuclrh1lA1PxP1QgbfRo8kks8lKW5kQsbbLoOk1_vz6PO10PesOx8k1oA1JTO1Nduqclrh1-v3Oxe2IdQqBx8k1_8k005lLkbvLcAl10rwNGdmAlrbScrwnwNwRWtx8l8uclrh20QvO2txDLAu:'

    base64_encode = base64.decodestring(str)
    print(" ",base64_encode)

    #hm = hmac.new(str.encode('d1b964811afb40118a12068ff74a12f4'), msg=None, digestmod=sha1)
    


def zhihu_login():
 
    global session
    has_captcha = is_captcha()
    if has_captcha:
        # 获取验证码
        captcha = get_captcha()
        # 在提交登陆之前，还需要对输入的验证码的正确性进行单独验证
        is_true = check_captcha(captcha)
        if is_true == False:
            print("验证码验证失败 ！！！！")
            return
    else:
        captcha = ''
 
    # 1528450244046.0112
    # print(time.time())
    #https://www.zhihu.com/api/v3/oauth/sign_in
    login_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
 
    # key(配合着加密数据而使用的Key:d1b964811afb40118a12068ff74a12f4),
    # msg = None, 要加密的重要数据。（适合一个数据加密）
    # digestmod = None, 采用的加密方式, md5, sha1
 
    # 1. 创建哈希加密对象
    hm = hmac.new(str.encode('d1b964811afb40118a12068ff74a12f4'), msg=None, digestmod=sha1)
 
    tm = str(int(time.time() * 1000))
    print('tm = ',tm)
 
    # 2. 开始向加密对象中传入需要加密的数据
    # 注意添加顺序。。。
    hm.update(str.encode('password'))
    hm.update(str.encode('c3cef7c66a1843f8b3a9e6a1e3160e20'))
    hm.update(str.encode('com.zhihu.web'))
    hm.update(str.encode(tm))
 
    # 3. 获取加密后的结果(就是signature签名。)
    res = hm.hexdigest()
 
    print('signature = ',res)
 
    post_params = {
        "client_id":"c3cef7c66a1843f8b3a9e6a1e3160e20",
        "grant_type": "password",
        "timestamp": tm,
        "source": "com.zhihu.web",
        "signature": res,
        "username": "***",
        "password": "***",
        "captcha": captcha,
        "lang": "cn",
        "ref_source": "homepage",
        "utm_source": "",
    }
 
    try:
        response = session.post(login_url, data=post_params, headers=headers, verify=False)
        if response.status_code == 201:
            print('登录成功')
            session.cookies.save(ignore_discard=True, ignore_expires=True)
            print(response.text)
        else:
            print('登录失败')
            print("Response header :  \n\t\t",response.headers)
            print(response.text)
        print("Cookies : ",session.cookies)
    except Exception as e:
        print('请求失败',e)
    
    print (" " ,session.headers)
    print(session.head)
def is_captcha():
    global COOKIE
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    try:
        response = session.get(url=captcha_url, headers=headers,verify=False)
        if response.status_code == 200:
            show_captcha = json.loads(response.text)['show_captcha']
            if show_captcha:
                print('有验证码')
                return True
            else:
                print('没有验证码')
                return False
    except Exception as e:
        print('')
 
import base64
from PIL import Image
from io import BytesIO
 
 
def get_captcha():
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
 
    # set-cookie: capsion_ticket="2|1:0|10:1528448404|14:capsion_ticket|44:MjIyMTdjMDNlNWQ0NDU4NDk3YWJiYTJhMGNhYzdhMGU=|27fc1b86cbb52d627f270fdc6ee72f58f88ae09b76483d30ff1026418d83bfce"; Domain=zhihu.com; expires=Sun, 08 Jul 2018 09:00:04 GMT; httponly; Path=/
 
    try:
        # 索取验证码图片，在保证有验证码的前提下才会发送PUT
        response = session.put(url=captcha_url, headers=headers,verify=False)
        if response.status_code == 202:
            captcha_url = json.loads(response.text)['img_base64']
            # 解码captcha_url
 
            url = base64.b64decode(captcha_url)
            url = BytesIO(url)
            image = Image.open(url)
            image.show()
 
            captcha = input('请输入验证码：')
            return captcha
    except Exception as e:
        print('')
 
 
def check_captcha(captcha):
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    post_params = {
        'input_text': captcha
    }
 
    # verify=False: 在发送https请求的时候，关闭证书认证
    response = session.post(url=captcha_url, data=post_params, headers=headers, verify=False)
    json_obj = json.loads(response.text)
    if 'success' in json_obj:
        print('输入验证码正确')
        return True
    else:
        print('输入验证码不正确')
        return False
 
 
if __name__ == '__main__':
    zhihu_login()
    # res = session.get('https://www.zhihu.com/', headers=headers, verify=False).text
    # print(res)
 
 
'''
# [SSL: CERTIFICATE_VERIFY_FAILED]: 在requests发送https请求时，出现的证书认证失败，解决办法：verify=False
# InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
#   InsecureRequestWarning)from http.cookiejar import LWPCookieJar
 
session = requests.Session()
session.cookies = LWPCookieJar(filename='zhihucookie.txt')
 
try:
    session.cookies.load(filename='zhihucookie.txt', ignore_expires=True, ignore_discard=True)
except Exception as e:
    print('暂时没有Cookie')
 
# res = session.get('https://www.zhihu.com/', headers=headers, verify=False)
# print(res)

def test_list():

    str = ["hello","china","hello","world"]
    print(str[0:-1])
    print(str[:-1])

    str.append("me")
    str.extend(["list"])

    print(str[0:-1])


def zhihu_login():
 
    global session
    has_captcha = is_captcha()
    if has_captcha:
        # 获取验证码
        captcha = get_captcha()
        # 在提交登陆之前，还需要对输入的验证码的正确性进行单独验证
        is_true = check_captcha(captcha)
        if is_true == False:
            return
    else:
        captcha = ''
 
    # 1528450244046.0112
    # print(time.time())
    login_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
 
    # key(配合着加密数据而使用的Key:d1b964811afb40118a12068ff74a12f4),
    # msg = None, 要加密的重要数据。（适合一个数据加密）
    # digestmod = None, 采用的加密方式, md5, sha1
 
    # 1. 创建哈希加密对象
    hm = hmac.new(str.encode('d1b964811afb40118a12068ff74a12f4'), msg=None, digestmod=sha1)
 
    tm = str(int(time.time() * 1000))
    print('tm = ',tm)
 
    # 2. 开始向加密对象中传入需要加密的数据
    # 注意添加顺序。
    hm.update(str.encode('password'))
    hm.update(str.encode('c3cef7c66a1843f8b3a9e6a1e3160e20'))
    hm.update(str.encode('com.zhihu.web'))
    hm.update(str.encode(tm))
 
    # 3. 获取加密后的结果(就是signature签名。)
    res = hm.hexdigest()
 
    print('signature = ',res)
 
    post_params = {
        "client_id":"c3cef7c66a1843f8b3a9e6a1e3160e20",
        "grant_type": "password",
        "timestamp": tm,
        "source": "com.zhihu.web",
        "signature": res,
        "username": "15927045754",
        "password": "gcm139723972.",
        "captcha": captcha,
        "lang": "cn",
        "ref_source": "homepage",
        "utm_source": "",
    }
   # print("post param" + post_params)
    try:
        response = session.post(login_url, data=post_params, headers=headers, verify=False)
        if response.status_code == 201:
            print('登录成功')
            session.cookies.save(ignore_discard=True, ignore_expires=True)
            print(response.text)
        else:
            print('登录失败')
            print(response.text)
    except Exception as e:
        print('请求失败',e)
 
def is_captcha():
    global COOKIE
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    try:
        response = session.get(url=captcha_url, headers=headers,verify=False)
        if response.status_code == 200:
            show_captcha = json.loads(response.text)['show_captcha']
            if show_captcha:
                print('有验证码')
                return True
            else:
                print('没有验证码')
                return False
    except Exception as e:
        print('')
 
import base64
from PIL import Image
from io import BytesIO
 
 
def get_captcha():
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
 
    # set-cookie: capsion_ticket="2|1:0|10:1528448404|14:capsion_ticket|44:MjIyMTdjMDNlNWQ0NDU4NDk3YWJiYTJhMGNhYzdhMGU=|27fc1b86cbb52d627f270fdc6ee72f58f88ae09b76483d30ff1026418d83bfce"; Domain=zhihu.com; expires=Sun, 08 Jul 2018 09:00:04 GMT; httponly; Path=/
 
    try:
        # 索取验证码图片，在保证有验证码的前提下才会发送PUT
        response = session.put(url=captcha_url, headers=headers,verify=False)
        if response.status_code == 202:
            captcha_url = json.loads(response.text)['img_base64']
            # 解码captcha_url
 
            url = base64.b64decode(captcha_url)
            url = BytesIO(url)
            image = Image.open(url)
            image.show()
 
            captcha = input('请输入验证码：')
            return captcha
    except Exception as e:
        print('')
 
 
def check_captcha(captcha):
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
    post_params = {
        'input_text': captcha
    }
 
    # verify=False: 在发送https请求的时候，关闭证书认证
    response = session.post(url=captcha_url, data=post_params, headers=headers, verify=False)
    json_obj = json.loads(response.text)
    if 'success' in json_obj:
        print('输入验证码正确')
        return True
    else:
        print('输入验证码不正确')
        return False
 
 
if __name__ == '__main__':
    test_list()
    zhihu_login()
    # res = session.get('https://www.zhihu.com/', headers=headers, verify=False).text
    # print(res)
 
 
 
# [SSL: CERTIFICATE_VERIFY_FAILED]: 在requests发送https请求时，出现的证书认证失败，解决办法：verify=False
# InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
#   InsecureRequestWarning)
'''