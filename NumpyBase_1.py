#- * - coding:utf - 8 -*-
from numpy import *

#产生随机数组
print random.rand(4,4)

#将数组转化为矩阵
randMat = mat(random.rand(4,4))

#.I 求逆矩阵
invRandMat = randMat.I

#应该得到单位矩阵，但是有很小的误差
myeye = invRandMat*randMat

#eye 创建单位矩阵，并得到误差
print myeye - eye(4)