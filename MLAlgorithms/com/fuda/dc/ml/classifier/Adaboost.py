#coding=utf-8

'''
Created on 2015年10月12日

@author: kevin

@description:
    a Adaboost classifier written by kevin

'''

import os
import sys
import math

class Adaboost(object):
    def __init__(self):
        self.alphaList = []
        self.thresholdList = []
        self.bList = []
        self.featureNum = 0
        self.samleNum = 0
        self.sampleData = []
        self.outputModelName = os.path.join(os.getcwd(), "model.txt")
    
    def loadData(self, dataFileName):
        with open(dataFileName) as fp:
            for line in fp.readlines():
                sample = [float(item) for item in line.split("\t")]
                self.sampleData.append(sample)
                
        self.samleNum = len(self.sampleData)
        if (self.samleNum == 0):
            raise ValueError('input sample num is 0!!!')
        
        self.featureNum = len(self.sampleData[0]) - 1
        if len(self.sampleData[0]) < 1:
            raise ValueError('input sample feature num is 0!!!')
        
    def train(self, stepLen = 100):
        self.alphaList = []
        self.thresholdList = []
        self.bList = []
        
        dt = [1.0 / self.samleNum for i in range(self.samleNum)]
        for t in range(self.featureNum):
            (error, threshold, b) = self._trainWeakClassifier(dt, t, stepLen)
            alpha = 0.5 * math.log((1 - error) / max(error, 1e-16))
            ztList = [dt[i] * math.exp(-alpha * self.sampleData[i][self.featureNum] * self._weakClasifier(self.sampleData[i][t], threshold, b)) for i in range(self.samleNum)]
            zt = sum(ztList)
            dtNext = [zti / zt for zti in ztList]
            dt = dtNext
            
            self.alphaList.append(alpha)
            self.thresholdList.append(threshold)
            self.bList.append(b)
    
    def outputModel(self, modelFileName = ''):
        if modelFileName == '':
            modelFileName = self.outputModelName 
        
        with open(modelFileName, 'w') as fp:
            fp.write(self._implodeList(self.alphaList) + "\n")
            fp.write(self._implodeList(self.thresholdList) + "\n")
            fp.write(self._implodeList(self.bList) + "\n")
        
    def loadModel(self, modelFileName = ''):
        if modelFileName != '':
            self.outputModelName = modelFileName
            
        with open(self.outputModelName) as fp:
            try:
                line = fp.readline()
                self.alphaList = [float(item) for item in line.split("\t")]
                line = fp.readline()
                self.thresholdList = [float(item) for item in line.split("\t")]
                line = fp.readline()
                self.bList = [float(item) for item in line.split("\t")]
            except:
                raise ValueError('model file format is wrong!')
        self.featureNum = len(self.alphaList)
        
    def predict(self, featureList):
        total = 0
        alphaSum = 0
        for i in range(self.featureNum):
            total += self.alphaList[i] * self._weakClasifier(featureList[i], self.thresholdList[i], self.bList[i])
            alphaSum += self.alphaList[i]
        #total -= 0.5 * alphaSum
        print total
        return self._sign(total)
    
    # TODO: find better method to get best threshold 
    def _trainWeakClassifier(self, dt, featuerNo, stepLen = 10):
        minimun = sys.float_info[0]
        maximum = -sys.float_info[0]
        for sample in self.sampleData:
            if minimun > sample[featuerNo]:
                minimun = sample[featuerNo]
            if maximum < sample[featuerNo]:
                maximum = sample[featuerNo]
            
        minError = sys.float_info[0]
        bestThreshold = minimun
        bestb = 1
        step = (maximum - minimun) / stepLen
        for n in range(stepLen):
            threshold = minimun + n * step
            errors = [dt[i] * self._isClassifyEqualSample(self.sampleData[i][featuerNo], self.sampleData[i][self.featureNum], threshold, 1) for i in range(self.samleNum)]
            error = sum(errors)
            if (minError > error):
                minError = error
                bestThreshold = threshold
                bestb = 1
                
            print "thres:%s, minError:%s, bestb: 1" %(threshold, minError)
                
            errors = [dt[i] * self._isClassifyEqualSample(self.sampleData[i][featuerNo], self.sampleData[i][self.featureNum], threshold, -1) for i in range(self.samleNum)]
            error = sum(errors)
            if (minError > error):
                minError = error
                bestThreshold = threshold  
                bestb = -1  
            print "thres:%s, minError:%s, bestb: -1" %(threshold, minError)
        return (minError, bestThreshold, bestb)
        
    def _weakClasifier(self, feature, threshold, b):
        if b == 1:
            if feature > threshold:
                return 1 
            else:
                return -1   
        else:
            if feature < threshold:
                return 1 
            else:
                return -1     
            
    def _isClassifyEqualSample(self, feature, y, threshold, b):
        result = self._weakClasifier(feature, threshold, b)
        if result == y:
            return 0
        else:
            return 1        
        
    def _sign(self, value):
        if value > 0:
            return 1
        else:
            return -1
        
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
    
if __name__=="__main__":
    adaboost = Adaboost()
    adaboost.loadData("E:\\sampledata.txt")
    adaboost.train()
    adaboost.outputModel("E:\\model.txt")
    adaboost.loadModel()
    print adaboost.predict([0.3, 0.6, 0.9])
    print adaboost.predict([0.8, 0.6, 0.9])
    print adaboost.predict([0.3, 0.2, 0.1])
    print adaboost.predict([0.55, 0.8, 0.7])
    print adaboost.predict([0.3, 0.2, 0.1])
    print adaboost.predict([0.9, 0.8, 0.6])