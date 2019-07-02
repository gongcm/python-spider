import  sys
import cv2 as cv

'''
python 基本数据类型：
    1. 数字  a = 1;
    2. 布尔
    3. 字符串 str = 'hello'
    4. 元组  就是不可以修改的list，但是与list 有区别就是表示的时候用圆括号来， tplue =("hello","world"),其值不可以修改。
    5. 列表  列表就是 list = ['aaa','bbb','ccc'],可以删除，也可以增加
    6. 字典   键值对，其中key可以是数字，布尔，元组，字符串，而且值value可以是任意的数据的类型，键值key是不可以变的,一个键值key对应一个value，dict = { 1:"aaa",("aaa"):"bbb",Flase:}
    7. 集合  集合就是一些重复，没有顺序的数据组成，这些数据的值是不可以改变的。一个集合可以由多种不同的数据类型的数据来组成。
'''

'''
 OCR 文字识别一般分为两步： 定位和识别。
 1. 定位： 主要判断出哪里是文字相应的像素值先提取出来。
 2. 识别： 对提取出来的文字进行识别。
'''

'''
定位 ： 需要对图像数据进行相应的处理才能得到有效的识别信息。
    1. 一般对图像进行灰度转换，进行一些滤波操作，过滤掉一些噪点。
    2. 图像边缘查找。
    '''

def get_roi(w,h):
    if w <=0 or h <= 0 :
        return -1



def process_image(path):
    img = cv.imread(path,cv.IMREAD_COLOR)
    #图像灰度转换
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #图像滤波
    cv.blur(gray,)


