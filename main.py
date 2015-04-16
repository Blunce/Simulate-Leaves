# coding=gbk
'''
Created on 2015年4月6日

@author: Blunce
'''

import random
import math
import pickle
from math import sqrt

WORLD_LENGTH = 1000
WORLD_WIDTH = 1000
WORLD_HEIGHT = 1000000

LEAF_R = 1  # 叶子半径
LEAF_L = 5  # 叶子长度

'''
树叶圆柱体

一根树叶有左右两端

树叶以均匀分布降落
'''

class State(object):
    # 每增加一次落叶的状态
    def __init__(self, num=0):
        self.num = num
        self.leaves = []
        
    
    def showState(self):
        # 将当前状态显示出来
        pass
    
    def save(self, filename):
        # 保存当前状态
        with open(filename, 'w') as fw:
            pickle.dump(self, fw)
    
    def loadState(self, filename):
        # 载入状态
        with open(filename) as fr:
            return pickle.load(fr)
    
    def pointHeight(self, x, y):
        # 搜索（x,y）点的最高位置
        # 可优化
        height = 0
        for item in self.leaves:
            if item.left[0] > x - LEAF_R & item.left < x - LEAF_R & item.left[1] > y - LEAF_R & item.left[1] < y + LEAF_R:
                if item.left[2] > height:
                    height = item.left[2]
            if item.right[0] > x - LEAF_R & item.right < x - LEAF_R & item.right[1] > y - LEAF_R & item.right[1] < y + LEAF_R:
                if item.right[2] > height:
                    height = item.right[2]
        return height

    def pointHeightReal(self, left, right):
        # 搜索左端和右端范围内的最高点
        # a = left[1] - right[1]
        # b = -(left[0] - right[0])
        # c = (left[0] - right[0]) * right[1] - (left[1] - right[1]) * right[0]
        height = []
        for item in self.leaves:
            if PointToLine(left[0], left[1], right[0], right[1], item.left[0], item.left[1]) <= 1 & (PointToPoint(left[0], left[1], item.left[0], item.left[1]) + PointToPoint(right[0], right[1], item.left[0], item.left[1])) <= (LEAF_L ** 2 + LEAF_R ** 2) ** 0.5:
                height.append(item.left[2])
            if PointToLine(left[0], left[1], right[0], right[1], item.right[0], item.right[1]) <= 1 & (PointToPoint(left[0], left[1], item.right[0], item.right[1]) + PointToPoint(right[0], right[1], item.right[0], item.right[1])) <= (LEAF_L ** 2 + LEAF_R ** 2) ** 0.5:
                height.append(item.left[2])
        return max(height)

    
    def addLeaf(self, leaf):
        self.leaves.append(leaf)
        self.num += 1
    
class Leaf(object):
    # 一根树叶的状态或位置
    def __init__(self):
        # 初始位置
        self.left = [0, 0, 0]
        self.right = [0, 0, 0]
    
    def setLocationLeft(self, x, y, z):
        # 设置树叶左端位置
        self.left = [x, y, z]
    
    def setLocationRight(self, x, y, z):
        # 设置树叶右端位置
        self.right = [x, y, z]
        
def NextState(state):
    # 由当前状态产生下一个状态
    if state.num == 0:
        leaf = Leaf()
        leaf.setLocationLeft(random.uniform(0, WORLD_LENGTH), random.uniform(0, WORLD_WIDTH), LEAF_R)
        deg = random.uniform(0, 360)  # 产生降落方向;
        leaf.setLocationRight(leaf.left[0] + LEAF_L * math.sin(math.radians(deg)), leaf.left[1] + LEAF_L * math.cos(math.radians(deg)), LEAF_R)
        state.addLeaf(leaf)
    else:
        lx, ly = random.uniform(0, WORLD_LENGTH), random.uniform(0, WORLD_WIDTH)
        leaf = Leaf()
        leaf.setLocationLeft(lx, ly, state.pointHeight(lx, ly))
        deg = random.uniform(0, 360)  # 产生降落方向
        rx, ry = leaf.left[0] + LEAF_L * math.sin(math.radians(deg)), leaf.left[1] + LEAF_R * math.cos(math.radians(deg))
        leaf.right = [rx, ry, 0]
        # 可优化
        leaf.right[2] = state.pointHeightReal(leaf.left, leaf.right) + LEAF_R
        # 可优化
        
        state.addLeaf(leaf)
    return state

def PointToLine(x0, y0, x1, y1, x2, y2):
    a = y0 - y1
    b = -(x0 - x1)
    c = (x0 - x1) * y1 - (y0 - y1) * x1
    return abs(a * x2 + b * y2 + c) / sqrt(a ** 2 + b ** 2)

def PointToPoint(x0, y0, x1, y1):
    return sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

    
    
        
