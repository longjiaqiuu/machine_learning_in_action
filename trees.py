# -*- coding: utf-8 -*-
"""
决策树

基本思想：通过数据在不同层次上的集合归属来对数据进行分类。
实现方案：由于原数据不可直接量化，因此采用信息论的方法量化为广义距离
关键问题：哪些特征在划分数据分类时重要性高，因此需要对各个特征进行评估


适用性：适用于非数值型、数据间比较性较弱的数据，可不关心数据间的广义距离
缺点：数据间相对量化的关系仍然未知，不同类之间仍不具有可比性，信息并没有被深层次的理解，只是从不同层次上进行了归属判断
"""

from math import log
import operator

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels

def calcShannonEnt(dataSet):
    """
    目的：计算数据的信息熵
    步骤：
        输入dataSet
        将最后一列的值定义为所有的微观状态
        计算该微观状态出现的频次，并计算出现的概率
        输出该数据集的熵值
    """
    numEntries = len(dataSet)
    labelCountDict = {} # 创建字典来计算dataSet中每个label出现的频率
    for featVec in dataSet: 
        currentLabel = featVec[-1]
        if currentLabel not in labelCountDict.keys(): labelCountDict[currentLabel] = 0
        labelCountDict[currentLabel] += 1  # labelCountDict -> {'yes': 2, 'no': 3}

    shannonEnt = 0.0 # 计算香农熵值
    for key in labelCountDict:
        prob = float(labelCountDict[key])/numEntries #当前key，即当前label的概率
        shannonEnt -= prob * log(prob,2) 
    return shannonEnt
    
def splitDataSet(dataSet, axis, value):
    """
    目的：当我们按照某个特征axis划分数据集dataSet时，需要将所有符合要求（featVec[axis] == value）的元素抽取出来
    输入：
        dataSet：待划分的数据集
        axis：划分数据的特征，比如axis = 1，即第二列
        value：需要满足的特征的值，比如 value = 1
    输出：不满足特征的特征值的数据集retDataSet
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis] #将axis列以外的数据赋值给 reducedFeatVec
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)  # retDataSet即为不符合featVec[axis] == value的数据集
    return retDataSet
    
def chooseBestFeatureToSplit(dataSet):
    """
    目的：选择最好的划分方法，即选择哪个特征axis进行划分使得香农熵最大
    步骤：输入dataset，对每个特征的每个值都进行熵计算，将熵最大的方案所对应特征返回
    """
    numFeatures = len(dataSet[0]) - 1      #最后一列用作分类标签
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):  
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)      
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)     
        infoGain = baseEntropy - newEntropy     # infoGain：按特征i划分后的总信息熵
        if (infoGain > bestInfoGain):       
            bestInfoGain = infoGain        
            bestFeature = i
    return bestFeature                   

def majorityCnt(classList):
    """
    目的：将类别的列表按照出现的次数进行降序，输出
    """
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    """
    目的：主要函数，通过递归的方法创建完整树
    输入：创建一个树只需要一个数据集，和一个labels用来作为解释标识
    要求：数据集的最后一列必须是类别标签，数据集必须是由列表元素组成的列表
    """
    classList = [example[-1] for example in dataSet] #将dataSet每行的最后一列赋值给classList
    if classList.count(classList[0]) == len(classList):  #如果 classList[0]对象在classList中出现的次数==类列表的长度
        return classList[0]#stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1: #stop splitting when there are no more features in dataSet
        return majorityCnt(classList) #如果 dataSet 只剩一个特征了，那个就返回该数据集出现最大频次key的值
    
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}} #创建一个大tree的起点
    del(labels[bestFeat])
    
    featValues = [example[bestFeat] for example in dataSet] #找到最佳特征的所有特征值
    uniqueVals = set(featValues) # 去重，即在该节点下的所有可能的树枝
    for value in uniqueVals: # 每个树枝做一个循环
        subLabels = labels[:]   #拷贝一份labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)#通过两个key检索后的value即是下一个分支树
    return myTree                            
    
def classify(inputTree,featLabels,testVec):
    """
    目的：测试算法
    
    """
    firstStr = next(iter(inputTree))
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    
    if isinstance(valueOfFeat, dict): # 判断valueOfFeat的类型是不是字典类型
        classLabel = classify(valueOfFeat, featLabels, testVec) # 如果是字典类型，则继续下探
    else: classLabel = valueOfFeat #如果不是字典类型，即叶子节点，则返回当前节点的分类标签
    return classLabel

def storeTree(inputTree,filename):
    import pickle #可将对象序列化
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()
    
def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

if __name__ == '__main__':

    fr = open('data_lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age', 'perscript', 'astigmatic', 'tearRate']
    lensesTree = createTree(lenses,lensesLabels)
    lensesTree # 生成树
    import treePlotter 
    treePlotter.createPlot(lensesTree) # 绘制树图




