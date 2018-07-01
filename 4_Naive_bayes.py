# -*- coding:utf-8 -*-
from numpy import *

'''此表到向量的转换函数'''
def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help',
                    'please'],
                   ['maybe','not','take','him','to','dog','park','stupid'],
                   ['my','dalmation','is','so','cute','I','love','him'],
                   ['stop','posting','stupid','worthless','garbage'],
                   ['mr','licks','ate','my','steak','how','to','stop','him'],
                   ['quit','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1]  #1侮辱性文字 0 正常文字
    return postingList,classVec
#获得词汇表
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        #创建并集
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

#输入词汇表和文档，输出文档的向量（和词汇表格式一样）
def setOfWords2Vec(vocabList,inputSet):
    returnVec =[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:print "the word: %s is not in my vocabulary!" % word
    return returnVec

#test
# listOPosts,listClasses = loadDataSet()
# myVocabList = createVocabList(listOPosts)
# print myVocabList
# vect = setOfWords2Vec(myVocabList,listOPosts[0])
# print vect

'''朴素贝叶斯分类器训练函数'''
def tainNBO(trainMatrix,trainCategory):
    #文档个数
    numTrainDocs = len(trainMatrix)
    #词个数
    numWords = len(trainMatrix[0])
    # class =1 代表侮辱性的言论，计算侮辱性言论的概率
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    #记录某个词在标签0和1的文档中出现的次数
    p0Num = zeros(numWords)
    p1Num = zeros(numWords)
    p0Denom =0.0
    p1Denom =0.0
    #对每一行（每一个文档）
    for i in range(numTrainDocs):
        if trainCategory[i] ==1:
            p1Num +=trainMatrix[i]
            p1Denom +=sum(trainMatrix[i])
        else:
            p0Num +=trainMatrix[i]
            p0Denom +=sum(trainMatrix[i])
    # 每一行是p(wi|0)和p(wi|1)
    p1Vect = p1Num/p1Denom
    p0Vec = p0Num/p0Denom
    return p0Vec,p1Vect,pAbusive