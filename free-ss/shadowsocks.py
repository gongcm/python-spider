import os
import urllib3

http = urllib3.PoolManager()

res = http.request("GET","https://www.youneed.win/free-ss")
print(res.status)