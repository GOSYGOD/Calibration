# -*- coding: utf-8 -*-
'''
Author: Jiaxi Zheng
Date: 2021-11-02 16:17:39
LastEditTime: 2021-11-17 15:58:45
LastEditors: Jiaxi Zheng
Description: 
FilePath: \标定上位机\Calculate.py
'''
import math
import numpy as np
from GPS2UTM import *
'''
description: 北向夹角计算
param {mat} 位置矩阵，目标x,y,E,N;雷达E,N
return {angle} 航向角
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

'''
description: 距离误差计算
param {mat} 位置矩阵，目标x,y方向, 真值x,y方向, 主基站北向夹角
return {dis} x,y方向距离误差
'''
def disCal(mat):

    rad = (360 - mat[4]) / 180 * math.pi

    coor = np.array([[mat[2] - mat[0]], [mat[3] - mat[1]]])     # 以主基站为原点，副基站xy坐标
    rotMat = np.array([[math.cos(rad), math.sin(rad)], [-math.sin(rad), math.cos(rad)]])    # 坐标系旋转矩阵
    newCoor = np.matmul(rotMat, coor)
    xDis = newCoor[0] 
    yDis = newCoor[1] 
    result = [xDis, yDis]
    return result

'''
description: 标定参数计算
param {mat} 2行3列，第1行：主基站X，主基站Y，主基站北向夹角
                    第2行：副基站X，副基站Y，副基站北向夹角
return {副基站} x平移量，y平移量
'''
def calibCal(mat):
    angleDis = (mat[0,2] - mat[1,2])
    rad = (360 - mat[0,2]) / 180 * math.pi

    coor = np.array([[mat[1,0] - mat[0,0]], [mat[1,1] - mat[0,1]]])     # 以主基站为原点，副基站xy坐标
    rotMat = np.array([[math.cos(rad), math.sin(rad)], [-math.sin(rad), math.cos(rad)]])    # 坐标系旋转矩阵
    newCoor = np.matmul(rotMat, coor)
    xDis = newCoor[0] 
    yDis = newCoor[1] 
    result = [xDis, yDis, angleDis]
    return result

if __name__ == '__main__':
    lonLidar = 116.2869783345294
    latLidar = 40.0516953302213

    lonTar = 116.2867578256973
    latTar = 40.0520586730172

    angleLidar = 100
    angleTar = 40

    ELidar, NLidar = GPS2UTM(latLidar, lonLidar)                    # 雷达经纬度转xy
    ETar, NTar = GPS2UTM(latTar, lonTar)

    mat = np.array([[ELidar, NLidar, angleLidar], [ETar, NTar, angleTar]])
    result = calibCal(mat)
    print(result)