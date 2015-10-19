#coding=utf-8

'''
Created on 2015年10月14日

@author: kevin
'''

import math
import cmath
import numpy
import scipy
import sympy
import xlrd
import xlwt
import pandas
import twisted
import MySQLdb
import sqlalchemy
import matplotlib

from comcom.fuda.dc.ml.classifieraboost import Adaboost
from comcom.fuda.dc.ml.classifiergicRegression import LogicRegression

def test1(fileName):
    a = 2
    b = 3
    c = 6
    d = -30
    postive = 0
    negtive = 0
    with open(fileName, 'w') as fp:
        for i in range(-10, 0):
            for j in range(10):
                for k in range(10):
                    if a * i + b * j + c * k + d > 0:
                        postive += 1
                        fp.write("%d\t%d\t%d\t1\n" %(i, j, k))
                        #fp.write("1 1:%d 2:%d 3:%d\n" %(i, j, k))
                        print "%d %d %d 1 %f" %(i, j, k, math.sqrt(i * i + j * j + k * k))
                    else:
                        negtive += 1
                        fp.write("%d\t%d\t%d\t-1\n" %(i, j, k))
                        #fp.write("-1 1:%d 2:%d 3:%d\n" %(i, j, k))
                        print "%d %d %d -1 %f" %(i, j, k, math.sqrt(i * i + j * j + k * k))
    print "postive:%s, negtive:%s" %(postive, negtive)
    
def test2(fileName):
    postive = 0
    negtive = 0
    with open(fileName, 'w') as fp:
        for i in range(-6, 6):
            for j in range(-6, 6):
                if i > j:
                    postive += 1
                    fp.write("%d\t%d\t1\n" %(i, j))
                    print "%d %d 1 %f" %(i, j, math.sqrt(i * i + j * j))
                elif i < j:
                    negtive += 1
                    fp.write("%d\t%d\t-1\n" %(i, j))
                    print "%d %d -1 %f" %(i, j, math.sqrt(i * i + j * j))
    print "postive:%s, negtive:%s" %(postive, negtive)
    
def test5(fileName1, fileName2):
    fp1 = open(fileName2, 'w')
    pos = 0
    neg = 0
    total = 0
    with open(fileName1) as fp:
        for line in fp.readlines():
            outline = ''
            items = line.strip().split(' ')
            total += 1
            if items[0] == '0':
                outline = '-1'
                neg += 1
            elif items[0] == '1':
                outline = '1'
                pos += 1
            else:
                continue
            
            for i in range(1, len(items)):
                if i > 112:
                    break
                outline += " %s" %items[i]
                i += 1
            fp1.write(outline + "\n")
            print "pos:%d, neg:%d, total:%d" %(pos, neg, total)
            
def test6(fileName1, fileName2):
    fp1 = open(fileName2, 'w')
    pos = 0
    neg = 0
    total = 0
    with open(fileName1) as fp:
        for line in fp.readlines():
            outline = ''
            items = line.strip().split(' ')
            total += 1
            
            for i in range(1, len(items)):
                if i > 112:
                    break
                arr = items[i].split(':')
                outline += "%s\t" %arr[1]
                i += 1
            if items[0] == '0':
                outline += '0'
                neg += 1
            elif items[0] == '1':
                outline += '1'
                pos += 1
            else:
                continue
            
            fp1.write(outline + "\n")
            print "pos:%d, neg:%d, total:%d" %(pos, neg, total)
            
def test3(fileName1, fileName2):
    fp1 = open(fileName2, 'w')
    with open(fileName1) as fp:
        for line in fp.readlines():
            items = line.strip().split(' ')
            items1 = []
            for item in items:
                if item != '':
                    items1.append(item)
            if items1[-1] == '0':
                items1[-1] = '-1'
            fp1.write(items1[-1] + '\t1:' + items1[0] + "\t2:" + items1[1] + "\n")
   
   
    
def sample_test_ada(fileName):
    adaboost = Adaboost()
    adaboost.loadModel('E://model.txt')
    
    with open(fileName) as fp:
        count = 0
        for line in fp.readlines():
            items = [float(item) for item in line.split('\t')]
            predict_result = adaboost.predict(items[:-1])
            if predict_result != items[-1]:
                print '%s:%f' %(line.strip(), predict_result)
                count += 1
        print 'count: %d' %count
    
    #print adaboost.predict([-1, 9, 4])


def sample_test_lr(fileName):
    logicRegression = LogicRegression()
    logicRegression.loadModel('E://model.txt')
    
    with open(fileName) as fp:
        count = 0
        for line in fp.readlines():
            items = [float(item) for item in line.split('\t')]
            predict_result = logicRegression.predict(items[:-1])
            
            print '%s:%f' %(line.strip(), predict_result)
            if predict_result != items[-1]:
                count += 1
        print 'count: %d' %count
    

if __name__=="__main__":
#     test1("E://sampledata.txt")
    # test2("E://sampledata.txt")
    # test3('E://sample_2.txt', 'E://sampledata.txt')
    # test5('E://english.dat', 'E://sampledata.txt')
    test6('E://english.dat', 'E://sampledata.txt')
    # sample_test_ada('E://sampledata.txt')
    sample_test_lr('E://sampledata.txt')
    
    

