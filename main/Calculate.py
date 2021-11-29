# -*- coding: utf-8 -*-
'''
Author: Jiaxi Zheng
Date: 2021-11-02 16:17:39
LastEditTime: 2021-11-29 13:23:25
LastEditors: Jiaxi Zheng
Description: 
FilePath: \标定上位机\Calculate.py
'''

import math
import numpy as np
from GPS2UTM import *

# 角度转弧度
def Angle2Rad(angle):
    return angle * math.pi / 180

# 弧度转角度
def Rad2Angle(rad):
    return rad * 180 / math.pi
    
'''
description: 计算两点之间距离和方位角，以真值为原点，正北方向为y轴
param {mat} 位置矩阵，目标经度，目标纬度，雷达经度，雷达纬度
return {angle} 距离，方位弧度，方位角度
'''
def TwoPointsCal(mat):
    earthRad = 6371004
    # earthRad = 6378137

    radLonTar = Angle2Rad(mat[0])
    radLatTar = Angle2Rad(mat[1])
    radLonTru = Angle2Rad(mat[2])
    radLatTru = Angle2Rad(mat[3])

    lonDis = radLonTru - radLonTar
    latDis = radLatTru - radLatTar

    dst = 2 * math.asin(math.sqrt(math.pow(math.sin(latDis / 2), 2) + math.cos(radLatTru) * math.cos(radLatTar) * \
        math.pow(math.sin(lonDis / 2), 2)))

    dst = abs(dst * earthRad)

    # 计算两点方位角，以真值为原点，正北方向为y轴
    x = math.sin(radLonTar - radLonTru) * math.cos(radLatTar)
    y = math.cos(radLatTru) * math.sin(radLatTar) - math.sin(radLatTru) * math.cos(radLatTar) * math.cos(radLonTar - radLonTru)
    rad = math.atan2(y, x)
    angle = (90 - Rad2Angle(rad)) % 360

    return dst, rad, angle

'''
description: 北向夹角计算
param {mat} 位置矩阵，目标x，y，经度，纬度，雷达经度，纬度
return {angle} 北向夹角
'''
def NorthAngleCal(mat):
    '''
    x' = x * cos + y * sin
    y' = y * cos - x * sin
    逆时针旋转为正
    '''
    inputMat = np.array([mat[2], mat[3], mat[4], mat[5]])
    dis, rad, angle = TwoPointsCal(inputMat)

    xCoor = dis * math.cos(rad)
    yCoor = dis * math.sin(rad)   

    northRad = math.atan2(mat[0] * yCoor - xCoor * mat[1], \
        mat[0] * xCoor + mat[1] * yCoor)
    
    northAngle = (360 - Rad2Angle(northRad)) % 360

    return northAngle

'''
description: 距离误差计算——检测中心
param {mat} 位置矩阵，目标检测经纬度, 目标真值经纬度, 主基站北向夹角
return {dis} x,y方向距离误差
'''
def DisCal(mat):
    inputMat = np.array([mat[0], mat[1], mat[2], mat[3]])
    dis, rad, angle = TwoPointsCal(inputMat)

    xDis = dis * math.cos(rad)
    yDis = dis * math.sin(rad)

    rotAngle = 360 - mat[4]
    rotRad = Angle2Rad(rotAngle)
    rotMat = np.array([[math.cos(rotRad), math.sin(rotRad)], [-math.sin(rotRad), math.cos(rotRad)]])    # 坐标系旋转矩阵
    newCoor = np.matmul(rotMat, np.array([[xDis], [yDis]]))

    return newCoor

'''
description: 标定参数计算
param {mat} 2行3列，第1行：主基站经度，纬度，北向夹角
                    第2行：副基站经度，纬度，北向夹角
return {副基站} x平移量，y平移量，角度差
'''
def CalibCal(mat):
    angleDis = (mat[0,2] - mat[1,2])

    inputMat = np.array([mat[1,0], mat[1,1], mat[0,0], mat[0,1], mat[0,2]])
    result = DisCal(inputMat)
    
    return np.array([result[0], result[1], angleDis])

'''
--------------------------------------------------------
### 经纬度转UTM坐标系，再计算距离、角度方法，暂时不使用 ###
--------------------------------------------------------
'''
# description: 北向夹角计算
# param {mat} 位置矩阵，目标x,y,E,N;雷达E,N
# return {angle} 航向角
# '''
# def angleCal(mat):
#     '''
#     x' = x * cos + y * sin
#     y' = y * cos - x * sin
#     逆时针旋转为正
#     '''
#     xEarth = mat[2] - mat[4]
#     yEarth = mat[3] - mat[5]

#     rad = math.atan2(yEarth * mat[0] - mat[1] * xEarth, \
#         yEarth * mat[1] + xEarth * mat[0])
#     angle = 360 - (rad / math.pi * 180) % 360
#     # angle = (90 - Rad2Angle(rad)) % 360

#     return angle

# '''
# description: 标定参数计算
# param {mat} 2行3列，第1行：主基站X，主基站Y，主基站北向夹角
#                     第2行：副基站X，副基站Y，副基站北向夹角
# return {副基站} x平移量，y平移量，角度差
# '''
# def calibCal(mat):
#     angleDis = (mat[0,2] - mat[1,2])
#     rad = (360 - mat[0,2]) / 180 * math.pi

#     coor = np.array([[mat[1,0] - mat[0,0]], [mat[1,1] - mat[0,1]]])                         # 以主基站为原点，副基站xy坐标
#     rotMat = np.array([[math.cos(rad), math.sin(rad)], [-math.sin(rad), math.cos(rad)]])    # 坐标系旋转矩阵
#     newCoor = np.matmul(rotMat, coor)
#     xDis = newCoor[0] 
#     yDis = newCoor[1] 
#     result = [xDis, yDis, angleDis]
#     return result

# '''
# description: 距离误差计算
# param {mat} 位置矩阵，目标x,y方向, 真值x,y方向, 主基站北向夹角
# return {dis} x,y方向距离误差
# '''
# def disCal(mat):

#     rad = Angle2Rad(360 - mat[4])
    
#     coor = np.array([[mat[0] - mat[2]], [mat[1] - mat[3]]])                                 # 以真值为原点，检测结果相对真值位置
#     rotMat = np.array([[math.cos(rad), math.sin(rad)], [-math.sin(rad), math.cos(rad)]])    # 坐标系旋转矩阵
#     newCoor = np.matmul(rotMat, coor)
#     print('------------------')
#     print(newCoor)
#     xDis = newCoor[0] 
#     yDis = newCoor[1] 
#     result = [xDis, yDis]
#     # return result
#     return result

if __name__ == '__main__':
    lonLidar = 116.2869783345294
    latLidar = 40.0516953302213

    lonTar = 116.2867578256973
    latTar = 40.0520586730172

    # lonTar = 116.2869783345294
    # latTar = 40.0516953302213

    angleLidar = 159.43
    angleTar = 163

    ELidar, NLidar = GPS2UTM(latLidar, lonLidar)                    # 雷达经纬度转xy
    ETar, NTar = GPS2UTM(latTar, lonTar)


    mat = np.array([-18,40, lonTar, latTar, lonLidar, latLidar])
    mat2 = np.array([-18,40, ETar, NTar, ELidar, NLidar])

  
    mat1 = np.array([[ELidar, NLidar, angleLidar], [ETar, NTar, angleTar]])
    mat2 = np.array([[lonLidar, latLidar, angleLidar], [lonTar, latTar, angleTar]])
    # result1 = calibCal(mat1)
    result2 = CalibCal(mat2)

    # print(result1)
    print(result2)

