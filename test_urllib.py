import urllib
import urllib.request
import urllib.response


url = "http://androidxref.com/7.1.2_r36/raw/Android.bp"

def prase_dir(url):
    
    path = urllib.request.url2pathname(url)
    print("parse : ",path)
    path = path.split(':')[1]
    print("path : ",path)
    dirs = path.split("\\")
    print("dirs :",dirs)
    print("dirs[0] ",dirs[0])
    print("last dir ",dirs[len(dirs) - 1])
    l = len(dirs[len(dirs) - 1])
    print("filename :",dirs[len(dirs) - 1])
    print("path[:-1] ",path[:-l])
    return path[:-l]

op = urllib.request.urlopen(url)
path = urllib.request.url2pathname(url)
print("path : ",path)
print('op ')

print(urllib.request.urlsplit(url))
result = urllib.request.urlparse(url)
print(result)
print(result[2])

path =prase_dir(url)
print("return path ",path)
#print(" ",op.read())
#with open()