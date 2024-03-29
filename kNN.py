# -*- coding: utf-8 -*-
from numpy import *
import operator #运算符
#import pysnooper #自动debug工具

def creatDataSet():
    """
    生成数据
    """
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1],[0.2,0.4]])
    labels = ['A','A','B','B','B']
    return group,labels

#@pysnooper.snoop(prefix='ZZZ ') # 以某个前缀开始，更容易定位和找到
#@pysnooper.snoop('D:/项目/基础数据/kNN/file.log') #也可输出log文件
def classify0(inX, dataSet, labels, k):
    """
    最近邻基本思想：新成员根据广义距离或相似性，寻找归属群的过程
    适用性：成员间必须有可被定义的广义距离
    入参出参：输入待分类的inX向量，计算该向量与训练集中前k个最近元素的个数，返回出现频率最多的标签作为该输入向量的类别标签
    :param inX: 期望分类的数据
    :param dataSet: 训练样本集
    :param labels: 类的标签向量
    :param k: 选取与输入点距离最小的k个点
    :return: 对inX进行分类的结果标签
    """
    dataSetSize = dataSet.shape[0] #元素的个数等于训练样本的行数
    diffMat = tile(inX,(dataSetSize,1)) - dataSet  #在列方向上重复inX，dataSetSize次，行1次
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis = 1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()  # numpy的函数argsort返回的是数组值从小到大的索引值
    
    classCount = {} #创建一个字典，用来统计各个标签类型的个数
    for i in range(k): 
        votIbel = labels[sortedDistIndicies[i]] #距离inX最新的labels记为votIbel
        classCount[votIbel] = classCount.get(votIbel,0) + 1 #在classCount字典中寻找key为votIbel的值，如果没有返回0,有的话将该key的值+1
    
    sortedClassCount = sorted(classCount.items(), # items返回可遍历的(键, 值) 元组数组
                              key = operator.itemgetter(1), #itemgetter可得到 获取对象classCount.items() 的第2个值，即字典的值，即按照各个类别的次数降序
                              reverse = True) #降序
    
    return sortedClassCount[0][0] # 返回频率最高的类别
    
    
def file2Matrix(filename):
    """
    将数据转换为矩阵与标签向量
    """
    file = open(filename) #开发文件
    arrayLines = file.readlines() #逐行读入，得到一个array数组
    numsOfLines = len(arrayLines) #行数
    
    Matrix = zeros((numsOfLines,3)) # 创建一个矩阵，与arraylines行数一直，列数为3
    Label = [] # 创建一个标签向量
    index = 0 # 定义初始的index索引
    
    for line in arrayLines:  # 逐行进行循环，将0到2列的值赋值给矩阵，将最后一列赋值给标签向量
        line = line.strip() # 将每一行去除前后的空格
        listFromLine = line.split('\t') # 将每一行按照空格分割，得到一个列表
        Matrix[index,:] = listFromLine[0:3] #将列表的[0:3]列赋值给准备好的矩阵的第index行
        Label.append(int(listFromLine[-1])) #将列表的最后一列取整数后追加到标签向量里
        index += 1 #index索引值+1
    
    return Matrix,Label #返回一个矩阵和标签向量

def autoNorm(dataSet):
    """
    数据归一化
    """
    minVals = dataSet.min(0) # 0表示从每列中选择最小值，而不是行
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet)) # 初始化矩阵
    m = shape(dataSet)[0] # dataSet的行数
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet / tile(ranges,(m,1))

    return normDataSet,ranges,minVals

def datingClassTest(normMat,datingLabels):
    """
    定义一个测试准确率工具
    """
    normMat = normMat
    datingLabels = datingLabels
    m = shape(normMat)[0] #数据总行数
    
    testRatio = 0.1
    numTestVecs = int(m*testRatio) #测试数据的个数
    
    errorCount = 0.0 #初始化
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],\
                                     datingLabels[numTestVecs:m],15)
        #print("预测的结果是：%d,真实的结果是：%d" %(classifierResult,datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1
    print("预测的总误差是： %f" %(errorCount/float(numTestVecs)))


    
if __name__ == '__main__':
    
    flyMiles = float(input("这个人每年的飞行距离大约多少米:"))#输入数据
    percentGames = float(input("这个人玩游戏的时间占比大约多少:"))#输入数据
    iceCream = float(input("这个人每年吃多少升的冰淇淋:"))#输入数据
    inArray = array([flyMiles,percentGames,iceCream])#数据转换为入参格式
    datingDataMat,datingLabels = file2Matrix('data_datingTestSet2.txt')#导入分类器训练数据与格式整理
    normMat,ranges,minVals = autoNorm(datingDataMat)#数据数值整理
    classifierResult = classify0((inArray-minVals)/ranges,normMat,datingLabels,5)#分类器工作
    resultList = ['不喜欢','一般','很喜欢'] #定义结果出参形式
    print("你对这个人的喜爱程度可能是：", resultList[classifierResult-1])#分类器结果转化为出参形式
    datingClassTest(normMat,datingLabels) #预测的误差分析
    

    

    