'''
Author: Jiaxi Zheng
Date: 2021-11-02 16:17:39
LastEditTime: 2021-11-04 11:05:11
LastEditors: Jiaxi Zheng
Description: 
FilePath: \相关软件\calculate.py
'''
import math

'''
description: 北向夹角计算
param {*} mat: 位置矩阵，目标x,y,E,N;雷达E,N
return {*} angle: 航向角
'''
def angleCal(mat):
    '''
    x' = x * cos + y * sin
    y' = y * cos - x * sin
    逆时针旋转为正
    '''
    xEarth = mat[2] - mat[4]
    yEarth = mat[3] - mat[5]
    rad = math.atan2(xEarth * mat[1] - mat[0] * yEarth, \
        yEarth * mat[1] + xEarth * mat[0])
    angle = (rad / math.pi * 180) % 360
    return angle