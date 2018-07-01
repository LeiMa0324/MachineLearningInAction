# -*- coding:utf-8 -*-
from math import log
#操作排序
import operator

'''计算给定数据集的信息熵'''
def calcShannonEnt(dataset):
    numEntries = len(dataset)
    labelCounts = {}
    for featVec in dataset:
        currentLabel = featVec[-1]
        # labelCount字典记录标签和出现频率
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
            labelCounts[currentLabel] +=1
    shannonEnt =0.0
    #计算每个标签的香农熵之和，仅仅表现数据集的分散程度，熵越高，混合的数据越多
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -=prob * log(prob,2)
    return  shannonEnt

'''构造鱼分类数据集'''
def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels


#test
# myDat ,labels = createDataSet()
# myDat[0][-1] = 'maybe'
# print myDat
# print calcShannonEnt(myDat)

'''按照给定特征划分数据集，将第axis个属性值等于value的数据抽取出来，返回retDataSet'''
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            #extend将列表中所有元素加入原列表，append只增加一个数据，该数据中存在加入的向量（二维）
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet
#test
# myDat ,labels = createDataSet()
# #输出第一个属性为1的数据（除了第一个属性）
# print splitDataSet(myDat,0,1)
# print splitDataSet(myDat,0,0)

'''选择最好的数据划分方式 信息增益 = 标签划分的熵-根据属性i的划分的熵'''
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    #根据标签划分的熵
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    #提取第i个属性的列向量
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        #提取该属性所有的属性值，set方法是最快的提取唯一值的方法
        uniqueVals = set(featList)
        newEntropy = 0.0
        #针对每个属性值划分数据集，得到subDataSet
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            #计算根据该属性值划分后的熵
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDataSet)
        # 信息增益 = 标签划分的熵-属性值划分的熵
        infoGain = baseEntropy - newEntropy
        #信息增益最大的为划分效果最好的属性
        if (infoGain>bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i

    return bestFeature

myDat ,labels = createDataSet()
# print myDat
# print chooseBestFeatureToSplit(myDat)

'''投票选举法'''
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote] = 0
        classCount[vote] +=1
    sortedClassCount = sorted(classCount.iteritems(),
                                  key=operator.itemgetter(1),reverse=True)
    return sortedClassCount

'''创建树的代码'''
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    #递归中止条件1，如果该分支下都是一个类型，则停止划分
    if classList.count(classList[0] == len(classList)):
        return classList[0]
    #递归中止条件2，遍历完所有属性，停止划分，返回投票最多的
    if len(dataSet[0]) ==1:
        return majorityCnt(classList)

    #选择最佳属性，建立树的根节点
    bestFeat = chooseBestFeatureToSplit(dataSet)
    print bestFeat
    print labels
    bestFeatLabel = labels[bestFeat]
    #使用字典类型储存树的信息
    myTree = {bestFeatLabel:{}}
    del (labels[bestFeat])

    #获取该最佳属性的所有值（根节点的所有分支）
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)

    #针对bestfeature所有分支value，分割数据集（splitDataSet），递归调用创建树的函数
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

myTree = createTree(myDat,labels)
print myTree