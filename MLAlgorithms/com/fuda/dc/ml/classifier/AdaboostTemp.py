#coding=utf-8

'''
Created on 2015年10月15日

@author: aa
'''

from numpy import *

def loadSimDat():  
    dataMat = matrix([[1, 2.1],  
                      [2.0, 1.1],  
                      [1.3, 1.0],  
                      [1.0, 1.0],  
                      [2.0, 1.0]])  
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]  
    return dataMat, classLabels  
  
# 单层决策树生成函数  
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):#just classify the data  
    retArray = ones((shape(dataMatrix)[0],1))  
    if threshIneq == 'lt':  
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0  
    else:  
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0  
    return retArray  
  
  
def buildStump(dataArr, classLabels, D):  
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T  
    m,n = shape(dataMatrix)  
    numSteps = 10.0; bestStump = {}; bestClassEst = mat(zeros((m,1)))  
    minError = inf  
    for i in range(n):  
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();  
        stepSize = (rangeMax - rangeMin)/numSteps  
        for j in range(-1, int(numSteps)+1):  
            for inequal in ['lt','gt']:  
                threshVal = (rangeMin + float(j)*stepSize)  
                predictedVals = stumpClassify(dataMatrix, i, threshVal, inequal)  
                errArr = mat(ones((m,1)))  
                errArr[predictedVals == labelMat] = 0  
                weightedError = D.T * errArr           #这里的error是错误向量errArr和权重向量D的相应元素相乘得到的即加权错误率  
                #print "split: dim %d, thresh %.2f, thresh inequal: %s, the weighted error is %.3f" %(i, threshVal, inequal, weightedError)  
                if weightedError < minError:  
                    minError = weightedError  
                    bestClassEst = predictedVals.copy()  
                    bestStump['dim'] = i  
                    bestStump['thresh'] = threshVal  
                    bestStump['ineq'] = inequal  
    return bestStump, minError, bestClassEst 

def adaBoostTrainDS(dataArr, classLabels, numIt = 40):  
    weakClassArr = []  
    m = shape(dataArr)[0]  
    D = mat(ones((m,1))/m)  
    aggClassEst = mat(zeros((m,1)))  
    for i in range(numIt):  
        bestStump, error, classEst = buildStump(dataArr, classLabels, D)  
       # print "D:", D.T  
        alpha = float(0.5 * log((1.0 - error)/max(error, 1e-16)))   #确保在没有错误时不会发生除零溢出  
        bestStump['alpha'] = alpha  
        weakClassArr.append(bestStump)  
        #print "classEst:", classEst.T  
        expon = multiply(-1 * alpha * mat(classLabels).T, classEst)    #乘法用于区分是否正确或者错误样本  
        D = multiply(D, exp(expon))  
        D = D/D.sum()            # 归一化用的  
        aggClassEst += alpha * classEst    #累加变成强分类器  
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m,1)))  
        errorRate = aggErrors.sum()/m  
        print "total error: ", errorRate, "\n"  
        if errorRate == 0.0: break  
        
    return weakClassArr, aggClassEst  

dataMat, classLabels = loadSimDat()
adaBoostTrainDS(dataMat, classLabels)

