# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 17:44:53 2019

@author: longjiaqi
"""

import matplotlib.pyplot as plt

decisionNode = dict(boxstyle = "sawtooth", fc = '0.8') #决策节点的样式
leafNode = dict(boxstyle = "round4",fc = '0.8') #叶节点的样式
arrow_args = dict(arrowstyle = '<-') #定义了箭头的指向

def plotNode(nodeTxt, conterPt, parentPt, nodeType):
    """
    目的：实际绘图函数，可绘制每个节点以及连线
    输入：
        nodeTxt：node的注释文本
        conterPt：注释文本的位置
        parentPt：父节点的位置
        nodeType：节点的显示类型
    输出：createPlot.ax1全局有效
    """
    createPlot.ax1.annotate(nodeTxt, 
                            xy = parentPt, xycoords = 'axes fraction',
                            xytext = conterPt, textcoords = 'axes fraction',
                            va = "center", 
                            ha = "center", 
                            bbox = nodeType, 
                            arrowprops = arrow_args)
    
def plotMidText(cntrPt, parentPt, txtString):
    """
    绘制线上文字
    输入
        坐标cntrPt、parentPt
        要显示的文字
    """
    xMid = (parentPt[0]-cntrPt[0])/2 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2 + cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

            
def plotTree(myTree, parentPt, nodeTxt):
    """
    目的：画整棵树的主要绘制函数
    输入：
        myTree：要绘制的树字典
        parentPt：初始位子
        nodeTxt：初始节点显示的文字
    """
    numLeafs = getNumLeafs(myTree)  
    depth = getTreeDepth(myTree)
    
    firstStr = next(iter(myTree))   
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff) # 将x轴分成若干部分
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD  # plotTree.yOff全局变量，记录已经绘制的节点位置
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))       
        else:   
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD


def createPlot(inTree):
    """
    目的：运行绘制树
    """
    from matplotlib.font_manager import FontProperties # 解决中文乱码的问题
    font = {'family' : 'SimHei',  
            'weight' : 'bold',
            'size'   : '12'}
    plt.rc('font', **font)      
    
    fig = plt.figure(1,facecolor='w')
    fig.clf() #清空绘图区
    axprops = dict(xticks = [], yticks = [])
    createPlot.ax1 = plt.subplot(111,frameon = False, **axprops) # 创建一个全局变量 createPlot.ax1
    
    plotTree.totalW = float(getNumLeafs(inTree)) # 创建一个全局变量记录宽度
    plotTree.totalD = float(getTreeDepth(inTree)) # 创建一个全局变量记录深度
    
    plotTree.xOff = -0.5/plotTree.totalW  # 创建一个全局变量 plotTree.xOff 记录已绘制的节点位置
    plotTree.yOff = 1.0  # 创建一个全局变量 plotTree.yOff 记录已绘制的节点位置
    
    plotTree(inTree, (0.5,1.0), '') # 初始位置
    
    plt.show()



def getNumLeafs(myTree):
    """
    目的：确定树的叶子数量，以方便得知图的x轴范围
    """
    numLeafs = 0
    firstStr = next(iter(myTree)) # In Python 3.x, dict.keys() does not return a list, it returns an iterable
    secondDict = myTree[firstStr]
    for key in secondDict.keys(): # 结果：type(secondDict[0]) -> str ; type(secondDict[1]) -> dict
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key]) # 每往深度推进一层，需要把所有的节点累加
        else:   numLeafs += 1
    return numLeafs 

def getTreeDepth(myTree):
    """
    目的：确定树的层数，以方便得知图的y轴范围
    """
    maxDepth = 0
    firstStr = next(iter(myTree)) # In Python 3.x, dict.keys() does not return a list, it returns an iterable
    secondDict = myTree[firstStr]
    for key in secondDict.keys(): # 结果：type(secondDict[0]) -> str ; type(secondDict[1]) -> dict
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])  # 每往深度推进一层，层数+1
        else:   thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth # 树在各个分支上的最深深度
    return maxDepth 

def retrieveTree(i):
    """
    保存了两棵树，0和1
    """
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: {'head':{0:'no',1:'yes'}},1:'no'}}]
    return listOfTrees[i]


    
  