# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 07:42:51 2019
@author: longjiaqi
朴素贝叶斯
假设：
    特征之间相互独立。实际中往往不独立
    每个特征同等重要，贝努利模型，不计算词频。实际上特征对分类效果的重要性肯定不同，即多项式模型

"""
from numpy import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 侮辱性的, 0 非侮辱性的
    return postingList,classVec #一个list的list，一个分类向量

def dataSet2VocabList(dataSet):
    """
    输入一个dataSet（要求由list组成的list），返回一个list类型的词典集合
    """
    vocabSet = set([]) # 初始化一个list词典集合
    for line in dataSet: # 将dataSet的每一行元素（该元素仍为一个list）生成集合
        vocabSet = set(line) | vocabSet # 将该集合与原词典集合取并集
    return list(vocabSet) # 返回 list 类型的词典集合

def ListOfWord2Vec(vocabSet,dataList):
    """
    输入词典、list数据。输出一个词向量，即词典中每个词出现的分布
    """
    returnVec = [0]*len(vocabSet) # 创建一个要返回的词向量，其长度与词典的长度一致
    for word in dataList: # 在输入的数据中做循环
        if word in vocabSet: # 如果循环元素在词典中
               returnVec[vocabSet.index(word)] = 1 # 将词向量中的对应位置[vocabSet.index(word)]的值设为1
        else: print("单词%s不在词典中" % word)# 否则输出该词不在字典中
    return returnVec

    
postingList,classVec = loadDataSet() 
vocabSet = dataSet2VocabList(postingList)
vocabVec = ListOfWord2Vec(vocabSet,postingList[3])







