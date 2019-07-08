# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 20:44:35 2019

@author: longjiaqi
"""
#加载模块
import sys
sys.path.append("D:\项目\代码学习\my_code")
from kNN import *

#导入数据
datingDataMat, datingLabels = file2Matrix('data_datingTestSet2.txt')

#绘图
import matplotlib
import matplotlib.pyplot as plt

#%matplotlib # 单独窗口显示图片
#%matplotlib inline # 在console中显示图片

# 解决中文字体问题
from matplotlib.font_manager import FontProperties 
font = {'family' : 'SimHei',
       'weight' : 'bold',
         'size'   : '16'}
plt.rc('font', **font)               # 步骤一（设置字体的更多属性）
plt.rc('axes', unicode_minus=False)  # 步骤二（解决坐标轴负数的负号显示问题）

# 
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
plt.xlabel('每年飞行常旅客里程数') 
plt.ylabel('玩游戏的时间占比')
plt.legend()
plt.show()





