#- * - coding: utf -8  -*-
from numpy import *
#运算符模块
import operator
import matplotlib
import matplotlib.pyplot as plt

'''创建数据'''
def createDataset():
    #创建二维数组
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels =['A','A','B','B']
    return group,labels

'''分类器'''
def classify0(inX,dataset,labels,k):
    #计算欧式距离
    datasetsize = dataset.shape[0]

    #tile，将输入向量 inX 在行方向上重复 datasize 次，减去 dataset，得到差值矩阵
    diffMat = tile (inX,(datasetsize,1)) - dataset

    #将差值矩阵平方
    sqDiffMat = diffMat **2

    #axis =1 将一个矩阵每一行向量相加
    sqDistances = sqDiffMat.sum(axis =1)
    #开根号
    Distances = sqDistances **0.5

    #argsort 返回从小大大的索引值
    sortedDistIndicies = Distances.argsort()

    #定义字典存储前 k 个标签和投票数
    classCount = {}
    # #选择距离最小的点
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount [voteIlabel] = classCount.get(voteIlabel,0)+1

    #iteritems 返回键值对元组(标签，次数)，sort 第二个参数，接受一个函数，指定使用哪个域进行排序
    # itemgetter(n)获取元素第 n 个域的值
    # reverse false 升序，True 降序
    sortedClassCount = sorted(classCount.iteritems(),
    key = operator.itemgetter(1),reverse = True)

    #输出 label 和次数的降序排列
    return sortedClassCount[0][0]

'''从文本中解析数据'''
def file2matrix(filename):
    fr = open(filename)
    arrayOfLines = fr.readlines() #读入数据，存入 array 中
    numberOfLines = len(arrayOfLines) #得到文件行数，样本数
    returnMat = zeros((numberOfLines,3)) #创建一个 n 行3列的零矩阵
    classLabelVector = []
    index = 0
    for line in arrayOfLines:
        #截取回车字符
        line = line.strip()
        #根据 tab 分割
        listFromLine = line.split('\t') # 每行的属性存为 listFromLine 临时 list
        returnMat[index,:] = listFromLine[0:3] # 将临时 list0-2的元素(三种属性)都放入矩阵第 index 行内
        classLabelVector.append(int(listFromLine[-1])) #list 中最后一个元素，lebel 放入 label 向量中
        index +=1 #迭代器+1

    #返回属性矩阵和标签向量
    return returnMat, classLabelVector

datingDataMat,datingLabels = file2matrix('./machinelearninginaction/Ch02/datingTestSet2.txt')

'''创建散点图'''
# fig = plt.figure()
# ax = fig.add_subplot(111)
# #使用2和3属性绘制散点图,第一个是 size value，第二个是 color value
# ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),
#            15.0*array(datingLabels)
#            )
# plt.show()

'''归一化数据'''
#归一化公式 (value-min)/(max-min)
def autoNorm(dataset):
    # 0 代表取每列中的最小值，1代表每行，存入 minvals 向量
    minVals = dataset.min(0)
    maxVals = dataset.max(0)

    #每列中的 ranges
    ranges = maxVals - minVals
    #创建一个和 dataset 一样大小的矩阵
    normDataset = zeros(shape(dataset))
    #取 dataset 的行数
    m = dataset.shape[0]
    #对于每一行 value - min
    normDataset = dataset - tile(minVals,(m,1))
    # 对每一行 (value - min）/ranges，这里的除是值相除，而不是矩阵相除
    normDataset = normDataset/tile(ranges,(m,1))
    return normDataset,ranges,minVals

'''归一化数据'''
normdataset,ranges,minvals = autoNorm(datingDataMat)
print normdataset,ranges,minvals

'''分类器测试代码'''
def datingClassTest():
    #训练集测试机划分
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('./machinelearninginaction/Ch02/datingTestSet2.txt')
    norMat, ranges,minvals =autoNorm(datingDataMat)
    m = norMat.shape[0]
    #测试及个数
    numTestVecs = int (m*hoRatio)
    #错误数
    errorCount =0.0
    #norMat中前 numTestVecs 作为测试集，后面作为训练集，输入 label 向量，k 取3
    for i in range(numTestVecs):
        classifierResult = classify0(norMat[i,:],norMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with :%d, the real answer is %d" % (classifierResult,datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount +=1.0

    print  "the total error rate is %f" % (errorCount/float(numTestVecs))

'''输入新数据测试'''
def classifyPerson():
    resultList = ["not at all","in small doses","in large doses"]
    #raw input 允许用户输入
    percentTats = float (raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumedper year?"))
    datingDataMat,datingLabels = file2matrix('./machinelearninginaction/Ch02/datingTestSet2.txt')
    norMat, ranges, minvals = autoNorm(datingDataMat)

    #将输入的属性存为 array 并且标准化
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr - minvals)/ranges,norMat,datingLabels,3)
    print "you will probably like this person:",resultList[classifierResult - 1]

# classifyPerson()