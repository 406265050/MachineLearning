#coding=utf-8

'''
Created on 2015年10月18日

@author: kevin
'''

import os
import sys
import math
import random

class Kmeans(object):
    def __init__(self):
        self.vecLen = 0
        self.catagoryNum = 0
        self.sampleNum = 0
        self.dataSet = []
        self.curCentroids = []
        self.outputModelName = os.path.join(os.getcwd(), "model.txt")

    '''
    load sample data
    '''
    def loadData(self, dataFileName):
        fp = open(dataFileName, "rb")
        if fp is None:
            raise "data file: %s can not find!" %dataFileName
        for line in fp.readlines():
            items = line.strip().split("\t")
            # if len(items) != self.vecLen:
            #    raise ValueError('feature length is not right: %s, lenght should be %d' %(line.strip(), self.vecLen))
            self.vecLen = len(items)
            data = [float(i) for i in items]
            self.dataSet.append(data)

        self.sampleNum = len(self.dataSet)
        if self.sampleNum < self.catagoryNum:
            raise ValueError('sample num %d can not less than catagory num %d' %(self.sampleNum, self.catagoryNum))

    '''
    initiate every cluster centroids, the samplist method: randomly select
    '''
    def _initCentroids(self):
        seedDict = {}
        for j in range(self.catagoryNum):
            while True:
                index = int(random.uniform(0, self.sampleNum))
                if seedDict.get(index, 0) == 0:
                    seedDict[index] = 1
                    break

        for key, value in seedDict.items():
            centroid = self.dataSet[key]
            self.curCentroids.append(centroid)

    '''
    euclidean distance calaculate
    '''
    def _euclideanDistance(self, vector1, vector2):
        distance = 0
        for j in range(len(vector1)):
            distance += (vector1[j] - vector2[j]) * (vector1[j] - vector2[j])
        return math.sqrt(distance)

    '''
    vector addition
    '''
    def _vectorAdd(self, vector1, vector2):
        j = 0
        for i in range(len(vector1)):
            vector1[i] += vector2[j]
            j += 1
        return vector1

    '''
    belong to which cluster
    '''
    def _belongToCluser(self, data, curCentroids):
        minDistance = sys.float_info[0]
        minIndex = 0
        for j in range(self.catagoryNum):
            distance = self._euclideanDistance(curCentroids[j], data)
            if minDistance > distance:
                minDistance = distance
                minIndex = j
        return minIndex

    def _calcCentroid(self, dataSet, catagoryList):
        centroid = [0.0 for j in range(self.vecLen)]
        for i in catagoryList:
            data = self.dataSet[i]
            for j in range(self.vecLen):
                centroid[j] += data[j]
        for j in range(self.vecLen):
            centroid[j] = centroid[j] / len(catagoryList)

        return centroid

    '''
    cluster method: iteration
    '''
    def train(self, catagoryNum, maxIterNum = 1000000, e = 0.000001):
        self.catagoryNum = catagoryNum
        self._initCentroids()

        maxIterNum = 0
        while maxIterNum < self.maxIterNum:
            catagoryStaticList = [[] for k in range(self.catagoryNum)]
            nextCentroids = [[0.0 for k in range(self.vecLen)] for j in range(self.catagoryNum)]
            
            for i in range(self.sampleNum):
                classNo = self._belongToCluser(self.dataSet[i], self.curCentroids)
                #centroid calculation step one: add
                #nextCentroids[classNo] = self._vectorAdd(nextCentroids[classNo], self.dataSet[i])
                #print "%s %s %s" %(classNo, nextCentroids[classNo], self.dataSet[i])
                #catagoryCount[classNo] += 1
                catagoryStaticList[classNo].append(i)
                print catagoryStaticList
            
            #centroid calculation step two: mean
            for j in range(self.catagoryNum):
                nextCentroids[j] = self._calcCentroid(self.dataSet, catagoryStaticList[j])
                    
            self.curCentroids = nextCentroids
            print "cur:%s" %self.curCentroids
            maxIterNum += 1
    
    def outputModel(self, modelFileName):
        if modelFileName == '':
            modelFileName = self.outputModelName 
        
        with open(modelFileName, 'w') as fp:
            i = 0
            for curCentroid in self.curCentroids:
                fp.write(self._implodeList(i, curCentroid) + "\n")
                i += 1
    
    def loadModel(self, modelFileName):
        if modelFileName != '':
            self.outputModelName = modelFileName
        
        self.curCentroids = []
        with open(self.outputModelName) as fp:
            try:
                i = 0
                for line in fp.readlines():
                    items = [float(item) for item in line.split("\t")]
                    self.curCentroids[i] = items[1:]
                    i += 1
            except:
                raise ValueError('model file format is wrong!')
    
    def predict(self, featureList):
        return self._belongToCluser(featureList, self.curCentroids)
    
    def _implodeList(self, index, dataList):
        length = len(dataList)
        if length == 0:
            return ""
        if length == 1:
            return "%d\t%f" %(index, dataList[0])
        
        line = str(index)
        length = len(dataList)
        for i in range(0, length):
            line += "\t" + str(dataList[i])
        return line
    
    def printOutput(self):
        for j in range(self.catagoryNum):
            print self.curCentroids[j]

if __name__=="__main__":
    kmeans = Kmeans(3, 3, 1)
    kmeans.loadData('test.txt')
    kmeans.train(8)
    kmeans.outputModel('')
    kmeans.predict([])