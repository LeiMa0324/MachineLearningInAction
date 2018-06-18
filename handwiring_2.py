#- * - coding: utf -8  -*-
from numpy import *
#运算符模块
import operator
import matplotlib
import matplotlib.pyplot as plt
import kNN_2
#可以列出给定目录的文件名
from os import listdir

'''向量化'''
def img2vector(filename):
    #zeros(shape) shape 为 int 或 int 序列
    returnVect = zeros((1,1024))
    fr =  open(filename)
    #一共32行
    for i in range(32):
        #读入一行的32个字符
        lineStr = fr.readline()
        #存入 returnVect 1*1024 向量中
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

testVector = img2vector('./machinelearninginaction/Ch02/digits/testDigits/0_13.txt')
print testVector[0,32:64]

'''调用 kNN中的分类器，测试手写识别算法'''
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('./machinelearninginaction/Ch02/digits/trainingDigits')
    #训练集个数
    m = len (trainingFileList)
    #构造训练集矩阵
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        #文件名第一个数字为 label
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        #存入训练集矩阵
        trainingMat[i,:] = img2vector('./machinelearninginaction/Ch02/digits/trainingDigits/%s'%fileNameStr)


    testFileList = listdir('./machinelearninginaction/Ch02/digits/testDigits')
    errorCount = 0.0
    #测试集个数
    mTest = len(testFileList)
    #构造测试集矩阵
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        #获得标签
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('./machinelearninginaction/Ch02/digits/trainingDigits/%s'%fileNameStr)
        #对每一个测试案例都训练一遍
        classifierResult = kNN_2.classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with :%d,the real answer is %d" %(classifierResult,classNumStr)
        if classifierResult!=classNumStr:
            errorCount +=1.0
    print "\nthe total nuber if errors is:%d" % errorCount
    print "\nthe total error rate is ：%f" %(errorCount/mTest)

handwritingClassTest()