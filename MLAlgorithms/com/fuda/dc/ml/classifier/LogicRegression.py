#coding=utf-8

'''
Created on 2015年10月12日

@author: kevin

@description:
    a LogicRegression classifier written by kevin

'''

import os
import math

from numpy import exp
from numpy import mat
from numpy import ones
from numpy import shape
from numpy import array

class LogicRegression(object):
    def __init__(self):
        self.thetaList = []
        self.dataMat = []
        self.labelMat = []
        self.outputModelName = os.path.join(os.getcwd(), "model.txt")
    
    def loadData(self, dataFileName):
        with open(dataFileName) as fp:
            for line in fp.readlines():
                items = line.strip().split()
                featureList = [float(item) for item in items]
                self.labelMat.append(int(items[-1]))
                featureList[-1] = 1.0
                self.dataMat.append(featureList)
        
    def train(self, alpha = 0.00001, maxIterNum = 1000000, e = 0.000001):
        dataMatrix = mat(self.dataMat)             #convert to NumPy matrix
        labelMat = mat(self.labelMat).transpose() #convert to NumPy matrix
        (m, n) = shape(dataMatrix)
        weights = ones((n, 1))
    
        iterNum = 1
        squareError = 1.0
        while iterNum < maxIterNum:              #heavy on matrix operations
            h = self._sigmoid(dataMatrix * weights)     #matrix mult
            error = (h - labelMat)     
            squareError = 0.5 * math.pow(sum(array(error).flatten(1)), 2) / m       #vector subtraction
            weights = weights - alpha * dataMatrix.transpose() * error #matrix mult
            print 'maxIterNum:%d, error:%f' %(iterNum, squareError)
            if squareError < e:
                break
            iterNum += 1
        self.thetaList = array(weights).flatten(1)
    
    def outputModel(self, modelFileName = ''):
        if modelFileName == '':
            modelFileName = self.outputModelName 
        
        with open(modelFileName, 'w') as fp:
            fp.write(self._implodeList(self.thetaList) + "\n")
        
    def loadModel(self, modelFileName = ''):
        if modelFileName != '':
            self.outputModelName = modelFileName
            
        with open(self.outputModelName) as fp:
            try:
                line = fp.readline()
                self.thetaList = [float(item) for item in line.split("\t")]
            except:
                raise ValueError('model file format is wrong!')
        
    def predict(self, featureList):
        featureList.append(1.0)
        total = sum([self.thetaList[i] * featureList[i] for i in range(len(self.thetaList))])
        result = self._sigmoid(total)
        print "predict value: %f" %result
        if result > 0.5:
            return 1
        else:
            return 0
    
    def _sigmoid(self, x):
        return 1.0 / (1 + exp(-x)) 
        
    def _implodeList(self, dataList):
        length = len(dataList)
        if length == 0:
            return ""
        if length == 1:
            return dataList[0]
        
        line = str(dataList[0])
        length = len(dataList)
        for i in range(1, length):
            line += "\t" + str(dataList[i])
        return line
    
# def trainLogRegres(train_x, train_y, opts):  
#     # calculate training time  
#     startTime = time.time()  
#   
#     numSamples, numFeatures = shape(train_x)  
#     alpha = opts['alpha']; maxIter = opts['maxIter']  
#     weights = ones((numFeatures, 1))  
#   
#     # optimize through gradient descent algorilthm  
#     for k in range(maxIter):  
#         if opts['optimizeType'] == 'gradDescent': # gradient descent algorilthm  
#             output = sigmoid(train_x * weights)  
#             error = train_y - output  
#             weights = weights + alpha * train_x.transpose() * error  
#         elif opts['optimizeType'] == 'stocGradDescent': # stochastic gradient descent  
#             for i in range(numSamples):  
#                 output = sigmoid(train_x[i, :] * weights)  
#                 error = train_y[i, 0] - output  
#                 weights = weights + alpha * train_x[i, :].transpose() * error  
#         elif opts['optimizeType'] == 'smoothStocGradDescent': # smooth stochastic gradient descent  
#             # randomly select samples to optimize for reducing cycle fluctuations   
#             dataIndex = range(numSamples)  
#             for i in range(numSamples):  
#                 alpha = 4.0 / (1.0 + k + i) + 0.01  
#                 randIndex = int(random.uniform(0, len(dataIndex)))  
#                 output = sigmoid(train_x[randIndex, :] * weights)  
#                 error = train_y[randIndex, 0] - output  
#                 weights = weights + alpha * train_x[randIndex, :].transpose() * error  
#                 del(dataIndex[randIndex]) # during one interation, delete the optimized sample  
#         else:  
#             raise NameError('Not support optimize method type!') 
    
if __name__=="__main__":
    logicRegression = LogicRegression()
    logicRegression.loadData("E:\\sampledata.txt")
    logicRegression.train(0.01, 1000)
    logicRegression.outputModel("E:\\model.txt")
    logicRegression.loadModel()
    print logicRegression.predict([0.3, 0.6, 0.9])
    print logicRegression.predict([0.8, 0.6, 0.9])
    print logicRegression.predict([0.3, 0.2, 0.1])
    print logicRegression.predict([0.55, 0.8, 0.7])
    print logicRegression.predict([0.3, 0.2, 0.1])
    print logicRegression.predict([0.9, 0.8, 0.6])
