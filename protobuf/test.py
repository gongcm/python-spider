import os
import test_pb2
import threadpool

test = test_pb2.Test()

test.id = 1
test.name = 'hello'
test.extra = 'test'

# 序列化
data = test.SerializeToString()

target = test_pb2.Test()
#反序列化
target.ParseFromString(data)

print(target.id)
print(target.name)
print(target.extra)

def test(args):
    print(args,'\n\n')

pool = threadpool.ThreadPool(4)
print("workers : ",pool.workers)

args = []
s = dict()
s['url'] = 'hello'
s['title'] = 'world'
args.append(s)
req = threadpool.makeRequests(test,args)
print(len(req))
for i in req:
    pool.putRequest(i)
w = pool.createWorkers(1)
#print("workers : ",pool.workers)

#pool.poll()

pool.wait()
