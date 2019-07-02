#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import sys
import io
import time

#消除 avx2 的警告
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf


#t10k-images.idx3-ubyte
#t10k-labels.idx1-ubyte
#train-images.idx3-ubyte
#train-labels.idx1-ubyte

train_data_filename = "train-images.idx3-ubyte"
train_labels_filename = "train-labels.idx1-ubyte"
test_data_filename = "t10k-images.idx3-ubyte"
test_labels_filename = "t10k-labels.idx1-ubyte"

IMAGE_SIZE = 28

def load_data(path,num_images):
    
    with open(path,"rb") as f: # 非文本文件用二进制形式打开文件，默认就是rb
        #f.read(16)
        buffer = f.read(IMAGE_SIZE * IMAGE_SIZE * num_images)
        data = np.frombuffer(buffer,dtype = np.uint8).astype(np.float32)
        print("data shape ",data.shape)
        data = (data -(255 / 2.0)) / 255
        data = data.reshape(num_images,IMAGE_SIZE,IMAGE_SIZE,1)
        return data

def load_label(path,num_images):
    
    with open(path,"rb") as f:
        #f.read(8)
        buffer = f.read(1 * num_images)
        data   = np.frombuffer(buffer,dtype = np.uint8).astype(np.float32)
        print("label shape ",data.shape)        
        data   = data.reshape(num_images,1)
        return data

def abs_path(filename):
    path = 'E:\\workspace\\source\\work\\mnist_test'
    return os.path.join(path,filename)



def test_softmax():

    ## Load mnist data

    mnist = input_data.read_data_sets("E:\\workspace\\source\\work\\mnist_test",one_hot= True)
    print(" ",mnist.train.images.shape," ",mnist.train.labels.shape)
    print(" ",mnist.test.images.shape," ",mnist.test.labels.shape)

    #train_data   = load_data(abs_path(train_data_filename),60000)
    #train_labels = load_label(abs_path(train_labels_filename),60000)
    #test_data    = load_data(abs_path(test_data_filename),10000)
    #test_labels  = load_label(abs_path(test_labels_filename),10000)
    
    #train_data   = train_data.reshape(60000,IMAGE_SIZE * IMAGE_SIZE)
    #train_labels = train_labels.reshape(60000,1)
    #print("train data shape : ",train_data.shape)
    #print("train label shape : ",train_labels.shape)

    #test_data   = test_data.reshape(10000,IMAGE_SIZE*IMAGE_SIZE)
    #test_labels = test_labels.reshape(10000,1)
    #print("test data shape : ",test_data.shape)
    #print("test label shape : ",test_labels.shape)
    ## plot show
    
    #plt.figure()
    #plt.imshow(train_data[1][1])
    
    ## softmax

    # 占位符 x，不是向量
    x = tf.placeholder(tf.float32,[None,IMAGE_SIZE * IMAGE_SIZE])

    w = tf.Variable(tf.zeros([784,10],dtype=tf.float32))
    b = tf.Variable(tf.zeros([10],dtype=tf.float32))

    ## 算法模型
    y = tf.nn.softmax(tf.matmul(x,w) + b)
    

    # G(x) 系数项，损失函数
    y_ = tf.placeholder(tf.float32,[None,10])
    # 所有交叉嫡相加
    cross_entropy = - tf.reduce_sum(y_ * tf.log(y))

    # o.o1 学习率，梯度下降法进行学习
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    
    init = tf.global_variables_initializer()
    session = tf.Session()
    session.run(init)

    for step in range(1,1000):

        x_batchs,y_batchs = mnist.train.next_batch(100) 
        if step % 100 == 0:
            print(" ",x_batchs.shape," ",y_batchs.shape)
        session.run(train_step,feed_dict={x:x_batchs,y_:y_batchs})
    
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
    # tf.cast 数据类型转换
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,"float"))
    print(" ",mnist.test.images.shape," ",mnist.test.labels.shape)
    print("accuracy : ",session.run(accuracy,feed_dict={x:mnist.test.images,y_:mnist.test.labels}))
    

'''
    for step in range(1,1000):

        offset  = np.random.randint(1,60000 - 100)
        #print(" offset : ",offset)
        x_train = train_data[ offset: offset + 100,...]
        offset = np.random.randint(1,10000 - 10)
        y_train = train_labels[offset:offset + 10,...]
        #print("x_train shape : ",x_train.shape)
        #print("y_train shape : ",y_train.shape)
        session.run(train_step,feed_dict={x:x_train,y_:y_train.reshape(1,10)})
    
    for i in range(1):
        correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction,"float"))
        print("accuracy : ",session.run(accuracy,feed_dict={x:test_data,y_:test_labels}))
'''


'''
最基本的CNN
卷积神经网络：  input data ---> conv layer ---> pool layer ----> 激励层 ----> full layer
'''

def weight_variable(shape):
    init = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(init)

def bias_variable(shape):
    init = tf.constant(0.1,shape=shape)
    return tf.Variable(init)

def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding="SAME")

''' 
 池化一般使用： max pool 和 avrange pool
'''
def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

def test_mnist_CNN():

    sess = tf.InteractiveSession()

    # 输入数据图片大小： 28 * 28 * 1(1 表示图片的通道数)
    mnist = input_data.read_data_sets("E:\\workspace\\source\\work\\mnist_test",one_hot= True)
    
    x = tf.placeholder(tf.float32,[None,784])
    x_ = tf.reshape(x,[-1,28,28,1])
    #print("shape ",x.eval().shape)
    y_ = tf.placeholder(tf.float32,[None,10])
    
    # covn layer 1 ,input 28*28*1 
    W_conv1 = weight_variable([5,5,1,32]) # 32 个 不同的5*5 * 1滤波器 
    b_conv1 = bias_variable([32])

    conv_1  = conv2d(x_,W_conv1)
    h_conv_1 = tf.nn.relu(conv_1 + b_conv1) # output: 28 * 28 * 32
    h_pool_1  = max_pool_2x2(h_conv_1) # output : 14 * 14 * 32

    #covn layer 2, input : 14 * 14 * 32
    W_conv2 = weight_variable([5,5,32,64])
    b_conv2 = bias_variable([64])

    conv_2 = conv2d(h_pool_1,W_conv2)
    h_conv_2 = tf.nn.relu(conv_2 + b_conv2) # output : 14*14*64

    h_pool_2 = max_pool_2x2(h_conv_2) # output : 7 * 7 * 64

    # full connection layer,input : 7 * 7 * 64
    W_fcl = weight_variable([7 * 7 * 64,1024])
    b_fcl = bias_variable([1024])

    i_fcl = tf.reshape(h_pool_2,[-1,7*7*64])
    h_fcl = tf.nn.relu(tf.matmul(i_fcl,W_fcl) + b_fcl) # output : 1 * 1024

    #Dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fcl_drop = tf.nn.dropout(h_fcl,keep_prob)

    #output
    W_fc2 = weight_variable([1024,10])
    b_fc2 = bias_variable([10])

    # 算法模型
    y_conv = tf.nn.softmax(tf.matmul(h_fcl_drop,W_fc2) + b_fc2)

    #loss function
    cross_entropy = - tf.reduce_sum( y_ * tf.log(y_conv))
    
    # 优化算法
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,'float'))

    sess.run(tf.initialize_all_variables())

    for i in range(20000):
        batch = mnist.train.next_batch(50)
        if i%100 == 0:
            train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
            print("step ",i," train_accuracy ",train_accuracy)
        # input 50 * [ 28 * 28 * 1],y_ 50 * [1 * 1]
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
    
    print("test accuracy ",accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))


def test_linear_regression():

   # 随机数据集
    x_data = np.float32(np.random.rand(2,100))
    y_data = np.dot([0.100,0.200],x_data) + 0.300

    #print("x_data ",x_data.shape)
    #print("y_data ",y_data.shape)
    #print("x_data reshape : ",x_data.reshape(1,200).shape)
    
    #plt.plot(x_data.reshape(1,200),y_data)
    b = tf.Variable(tf.zeros([1]),name="bias")
    W = tf.Variable(tf.random_uniform([1,2],-1.0,1.0),"weights")
    y = tf.matmul(W,x_data) + b

    #loss
    loss = tf.reduce_mean(tf.square(y - y_data))
    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)

    #init = tf.initialize_all_variables()
    init = tf.global_variables_initializer()

    sess = tf.Session()
    save = tf.train.Saver()

    sess.run(init)

    if not os.path.exists('./model'):
        os.mkdir("./model")
    for i in range(1,201):
        
        sess.run(train)

        if i % 20 == 0: # 每20次打印一次
            print(" ",i,sess.run(W),sess.run(b))
    
    save.save(sess,os.path.join("./model","model.cpkt"))

    sess.close()


def test_time():

    print("tensorflow cpu start ...")
    start = time.time()
    with tf.device("/cpu:0"):
        test_linear_regression()
    end = time.time()

    t1 = end - start 

    print("tensorflow gpu 0 start ...")
    start = time.time()
    with tf.device("/gpu:1"):
        test_linear_regression()
    end = time.time()
    t2 = end - start 


    print("cpu cost ",t1," s")
    print("gpu 0 cost ",t2," s")

if __name__ == "__main__":
    print("main start ... \n")
    print("tensorflow version ",tf.__version__)
    
    #test_time()
    test_linear_regression()