# -*- coding: utf-8 -*-
'''
Author: Jiaxi Zheng
Date: 2021-11-01 13:44:13
LastEditTime: 2021-11-23 13:13:07
LastEditors: Jiaxi Zheng
Description: 
FilePath: \标定上位机\Application.py
'''

import tkinter as tk
import os
import re
import numpy as np
from GPS2UTM import *
from findFromcsv import *
from Calculate import *

'''
description: 生成上位机，功能排版
param {*}
return {*}
'''
class Application(tk.Frame):
    def __init__(self):
        # 初始化root，面积
        self.root = tk.Tk()
        self.root.title('标定上位机')
        self.width = 800
        self.height = 400
        self.root.geometry(f'{self.width}x{self.height}')
        #self.root.resizable(False, False)
        
        # 整体框架pan
        self.frameAll = tk.Frame(self.root)
        self.frameAll.pack(fill='both', expand=1)

        # 上中下三个区域（Top, Mid, Bot）
        self.panTop = tk.LabelFrame(self.frameAll, relief='sunken', pady=5)
        self.panMid = tk.LabelFrame(self.frameAll, text='数据输入', relief='sunken', font=('宋体', 18), pady=5)
        self.panBot = tk.LabelFrame(self.frameAll, relief='sunken', pady=5)
        self.panTop.pack(fill='x')
        self.panMid.pack(fill='x')
        self.panBot.pack(fill='x')

        # Top区域——输入方式&功能选择&文件读取
        self.frameTargetInputType = tk.LabelFrame(self.panTop, text='目标输入方式', font=('宋体', 18), relief='sunken')
        self.frameFunc = tk.LabelFrame(self.panTop, text='计算选项', font=('宋体', 18), relief='sunken')
        self.frameFile = tk.LabelFrame(self.panTop, text='文件读取', font=('宋体', 18), relief='sunken')
        self.frameTargetInputType.pack(fill='both', expand=1, side=tk.LEFT)
        self.frameFunc.pack(fill='both', expand=1, side=tk.LEFT)
        self.frameFile.pack(fill='both', expand=1, side=tk.RIGHT)

        # Mid区域——数据输入
        # self.panMid = tk.LabelFrame(self.panMid, font=('宋体', 18), relief='sunken')
        # self.panMid.pack(fill='both', expand=1, side=tk.LEFT)

        # Bottom区域——结果&功能
        self.frameRes = tk.LabelFrame(self.panBot, text='结果', font=('宋体', 18), relief='sunken')
        self.frameBut = tk.LabelFrame(self.panBot, text='功能', font=('宋体', 18), relief='sunken')
        self.frameRes.pack(fill='none', expand=0, side=tk.LEFT)
        self.frameBut.pack(fill='both', expand=1, side=tk.RIGHT)
        
        self.SetFrameTargetInput()  # 目标输入方式布局
        self.SetFrameFunc()         # 计算选项布局
        self.SetFrameFile()         # 文件区域布局
        self.SetFrameData()         # 数据区域布局
        self.SetFrameRes()          # 结果区域布局
        self.SetFrameBut()          # 按钮区域布局  
        
        self.root.mainloop()
    
    '''
    description: 目标输入布局，目标数据输入方式
    param {*} self
    return {*}
    '''    
    def SetFrameTargetInput(self):
        #-------------------- 目标输入方式 --------------------#   
        # 方式值 
        self.targetInputVar = tk.IntVar()

        # 方式
        self.targetDirFunc = tk.Radiobutton(self.frameTargetInputType, text='直接输入', \
            font=('宋体', 15), padx=10, pady=8, variable=self.targetInputVar, value=1, command=self.TargetInputChange)
        self.targetFileFunc = tk.Radiobutton(self.frameTargetInputType, text='文件读取', \
            font=('宋体', 15), padx=10, pady=8, variable=self.targetInputVar, value=2, command=self.TargetInputChange)

        # 布局
        self.targetDirFunc.grid(row=0, column=0, sticky='w')
        self.targetFileFunc.grid(row=1, column=0, sticky='w')  
    
    '''
    description: 功能区域布局，北向夹角/距离/雷达平移量
    param {*} self
    return {*}
    '''
    def SetFrameFunc(self):
        #-------------------- 功能 --------------------#
        # 功能值
        self.funcVar = tk.IntVar()

        # 功能
        self.angleFunc = tk.Radiobutton(self.frameFunc, text='北向夹角', \
            font=('宋体', 15), padx=10, pady=8, variable=self.funcVar, value=1, command=self.TargetInputChange)
        self.disFunc = tk.Radiobutton(self.frameFunc, text='距离', \
            font=('宋体', 15), padx=10, pady=8, variable=self.funcVar, value=2, command=self.TargetInputChange)
        self.calibFunc = tk.Radiobutton(self.frameFunc, text='雷达平移量', \
            font=('宋体', 15), padx=10, pady=8, variable=self.funcVar, value=3, command=self.TargetInputChange)


        # 布局
        self.angleFunc.grid(row=0, column=0, sticky='w')
        self.disFunc.grid(row=0, column=1, sticky='w')  
        self.calibFunc.grid(row=1, column=0, sticky='w')

    '''
    description: 文件读取区域布局，ID和文件路径
    param {*} self
    return {*}
    '''    
    def SetFrameFile(self):      
        #-------------------- 文件读取 --------------------#
        # ID
        self.idLabel = tk.Label(self.frameFile, text='目标ID ', font=('宋体', 15), padx=10, pady=10)
        self.idEntry = tk.Entry(self.frameFile, font=('宋体', 15), width=15)

        # 文件路径
        self.pathLabel = tk.Label(self.frameFile, text=' 文件路径 ', font=('宋体', 15), padx=10, pady=10)
        self.pathEntry = tk.Entry(self.frameFile, font=('宋体', 15), width=15)

        # 布局
        self.idLabel.grid(row=0, column=0, sticky='e')
        self.idEntry.grid(row=0, column=1)
        self.pathLabel.grid(row=1, column=0)
        self.pathEntry.grid(row=1, column=1)

    '''
    description: 目标区域布局，直接输入/文件读取
    param {*} self
    return {*}
    '''    
    def SetFrameData(self):
        #-------------------- 直接输入 --------------------#
        # 目标经度/真值精度
        self.lonTargetLabel = tk.Label(self.panMid, text=' 真值经度', font=('宋体', 15), pady=5)
        self.lonTarEntry = tk.Entry(self.panMid, font=('宋体', 15), width=13)
        
        # 目标纬度/真值纬度
        self.latTargetLabel = tk.Label(self.panMid, text='  真值纬度', font=('宋体', 15), pady=5)
        self.latTarEntry = tk.Entry(self.panMid, font=('宋体', 15), width=13)
        
        # 目标横坐标/检测经度
        self.xTargetLabel = tk.Label(self.panMid, text='感知横坐标', font=('宋体', 15), pady=5)
        self.xTarEntry = tk.Entry(self.panMid, font=('宋体', 15), width=13)

        # 目标纵坐标/检测纬度
        self.yTargetLabel = tk.Label(self.panMid, text=' 感知纵坐标', font=('宋体', 15), pady=5)
        self.yTarEntry = tk.Entry(self.panMid, font=('宋体', 15), width=13)
        
        # 雷达经度/主基站北向夹角
        self.lonLidarLabel = tk.Label(self.panMid, text='  雷达经度', font=('宋体', 15), pady=8)
        self.lonLidarEntry = tk.Entry(self.panMid, font=('宋体', 15), width=15)

        # 雷达纬度/副基站北向夹角
        self.latLidarLabel = tk.Label(self.panMid, text='  雷达纬度', font=('宋体', 15), pady=8)
        self.latLidarEntry = tk.Entry(self.panMid, font=('宋体', 15), width=15)
        
        # 布局
        self.lonTargetLabel.grid(row=0, column=0, sticky=tk.constants.E)
        self.lonTarEntry.grid(row=0, column=1, sticky=tk.constants.E)
        self.latTargetLabel.grid(row=0, column=2, sticky=tk.constants.E)
        self.latTarEntry.grid(row=0, column=3, sticky=tk.constants.E)
        self.lonLidarLabel.grid(row=0,column=4, sticky=tk.constants.E)
        self.lonLidarEntry.grid(row=0,column=5, sticky=tk.constants.E)
        self.xTargetLabel.grid(row=1, column=0, sticky=tk.constants.E)
        self.xTarEntry.grid(row=1, column=1, sticky=tk.constants.E)
        self.yTargetLabel.grid(row=1, column=2, sticky=tk.constants.E)
        self.yTarEntry.grid(row=1, column=3, sticky=tk.constants.E)    
        self.latLidarLabel.grid(row=1,column=4, sticky=tk.constants.E)
        self.latLidarEntry.grid(row=1,column=5, sticky=tk.constants.E)

        
    '''
    description: 结果区域布局，显示计算结果
    param {*} self
    return {*}
    '''    
    def SetFrameRes(self):
        #-------------------- 结果 --------------------#
        # 结果框
        self.resultText = tk.Text(self.frameRes, width=30, font=('宋体', 15), state=tk.DISABLED)

        # 布局
        self.resultText.grid(row=0)

    '''
    description: 按钮区域布局，计算、清空、退出
    param {*} self
    return {*}
    '''
    def SetFrameBut(self):
        #-------------------- 按钮 --------------------#
        self.start = tk.Button(self.frameBut, text='计算', font=('宋体', 15), command=self.Cal)
        self.clear = tk.Button(self.frameBut, text='清空', font=('宋体', 15), command=self.Clear)
        self.QUIT = tk.Button(self.frameBut, text='退出', font=('宋体', 15), command=self.root.destroy)

        # 布局
        self.start.pack(fill='both', expand=1, side=tk.LEFT)
        self.clear.pack(fill='both', expand=1, side=tk.LEFT)
        self.QUIT.pack(fill='both', expand=1, side=tk.RIGHT)
    
    '''
    description: 更改输入项及输入框
    param {*} self
    return {*}
    '''
    def TargetInputChange(self):
        #-------------------- 根据不同选择放开不同输入框 --------------------#
        funcVar = self.funcVar.get()
        typeVar = self.targetInputVar.get()

        # 北向夹角
        if funcVar == 1:
            self.lonTargetLabel.configure(text=' 真值经度')
            self.latTargetLabel.configure(text='  真值纬度')
            self.lonLidarLabel.configure(text='  雷达经度')
            self.latLidarLabel.configure(text='  雷达纬度')
            self.xTargetLabel.configure(text='感知横坐标')
            self.yTargetLabel.configure(text=' 感知纵坐标')
            self.targetFileFunc.configure(state=tk.NORMAL)
        
        # 距离
        elif funcVar == 2:
            self.lonTargetLabel.configure(text=' 真值经度')
            self.latTargetLabel.configure(text='  真值纬度')
            self.lonLidarLabel.configure(text='主基站北向夹角')
            # self.latLidarLabel.configure(text='副基站北向夹角')
            self.xTargetLabel.configure(text='检测经度')
            self.yTargetLabel.configure(text='检测纬度')
            self.targetFileFunc.configure(state=tk.NORMAL)
        
        # 雷达平移量
        elif funcVar == 3:
            self.lonTargetLabel.configure(text='主基站经度')
            self.latTargetLabel.configure(text=' 主基站纬度')
            self.lonLidarLabel.configure(text=' 主基站北向夹角')
            self.latLidarLabel.configure(text=' 副基站北向夹角')
            self.xTargetLabel.configure(text='副基站经度')
            self.yTargetLabel.configure(text=' 副基站纬度')
            self.targetInputVar.set(1)
            self.targetFileFunc.configure(state=tk.DISABLED)
            typeVar = self.targetInputVar.get()

        if (typeVar == 1) & (funcVar == 1):
            self.latLidarEntry.config(state=tk.NORMAL)
            self.lonLidarEntry.config(state=tk.NORMAL)
            self.latTarEntry.config(state=tk.NORMAL)
            self.lonTarEntry.config(state=tk.NORMAL)
            self.xTarEntry.config(state=tk.NORMAL)
            self.yTarEntry.config(state=tk.NORMAL)
            self.idEntry.config(state=tk.DISABLED)
            self.pathEntry.config(state=tk.DISABLED)

        elif (typeVar == 1) & (funcVar == 2):
            self.latLidarEntry.config(state=tk.DISABLED)
            self.lonLidarEntry.config(state=tk.NORMAL)
            self.latTarEntry.config(state=tk.NORMAL)
            self.lonTarEntry.config(state=tk.NORMAL)
            self.xTarEntry.config(state=tk.NORMAL)
            self.yTarEntry.config(state=tk.NORMAL)
            self.idEntry.config(state=tk.DISABLED)
            self.pathEntry.config(state=tk.DISABLED)

        elif (typeVar == 1) & (funcVar == 3):
            self.latLidarEntry.config(state=tk.NORMAL)
            self.lonLidarEntry.config(state=tk.NORMAL)
            self.latTarEntry.config(state=tk.NORMAL)
            self.lonTarEntry.config(state=tk.NORMAL)
            self.xTarEntry.config(state=tk.NORMAL)
            self.yTarEntry.config(state=tk.NORMAL)
            self.idEntry.config(state=tk.DISABLED)
            self.pathEntry.config(state=tk.DISABLED)
            
        elif (typeVar == 2) & (funcVar == 1):
            self.latLidarEntry.config(state=tk.NORMAL)
            self.lonLidarEntry.config(state=tk.NORMAL)
            self.latTarEntry.config(state=tk.NORMAL)
            self.lonTarEntry.config(state=tk.NORMAL)
            self.xTarEntry.config(state=tk.DISABLED)
            self.yTarEntry.config(state=tk.DISABLED)
            self.idEntry.config(state=tk.NORMAL)
            self.pathEntry.config(state=tk.NORMAL)

        elif (typeVar == 2) & (funcVar == 2):
            self.latLidarEntry.config(state=tk.DISABLED)
            self.lonLidarEntry.config(state=tk.NORMAL)
            self.latTarEntry.config(state=tk.NORMAL)
            self.lonTarEntry.config(state=tk.NORMAL)
            self.xTarEntry.config(state=tk.DISABLED)
            self.yTarEntry.config(state=tk.DISABLED)
            self.idEntry.config(state=tk.NORMAL)
            self.pathEntry.config(state=tk.NORMAL)

    '''
    description: 数据读取，包含直接输入和文件读取
    param {*}
    return {*} 
    '''
    def DataRead(self):
        if self.targetInputVal == 1:
            #-------------------- 直接输入 --------------------#
            # 北向夹角：    目标经纬度,x,y                  
            # 距离：        目标真值经纬度和检测经纬度，北向夹角
            # 雷达平移量：  主基站经纬度，副基站经纬度，北向夹角
            #-------------------------------------------------#

            # 北向夹角
            if self.funcFlag == 1: 
                try:
                    self.truthLonTarget = float(self.lonTarEntry.get())     # 目标真值经纬度
                    self.truthLatTarget = float(self.latTarEntry.get())
                    self.xTarget = float(self.xTarEntry.get())              # 目标x,y位置/目标检测经纬度
                    self.yTarget = float(self.yTarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '目标输入数据有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)               # 结果框不可被修改 
                    return

                # 读取雷达经纬度
                try:
                    self.lonLidar = float(self.lonLidarEntry.get())         # 雷达经纬度
                    self.latLidar = float(self.latLidarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '雷达数据有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)     
                    return 
                    
            # 距离
            elif self.funcFlag == 2:
                try:
                    self.truthLonTarget = float(self.lonTarEntry.get())     # 目标真值经纬度
                    self.truthLatTarget = float(self.latTarEntry.get())
                    self.detLonTarget = float(self.xTarEntry.get())         # 目标检测经纬度
                    self.detLatTarget = float(self.yTarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '目标输入数据有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)               
                    return

                try:
                    self.angleNorth = float(self.lonLidarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '北向夹角有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)               
                    return

            # 雷达平移量
            elif self.funcFlag == 3:
                try:
                    self.lonFirst = float(self.lonTarEntry.get())           # 主基站经纬度
                    self.latFirst = float(self.latTarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '主基站经纬度有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)               
                    return

                try:
                    self.lonSecond = float(self.xTarEntry.get())            # 副基站经纬度
                    self.latSecond = float(self.yTarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '副基站经纬度有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)               
                    return

                try:
                    self.angleFirst = float(self.lonLidarEntry.get())       # 主基站北向夹角
                    self.angelSecond = float(self.latLidarEntry.get())      # 副基站北向夹角
                except:
                    self.resultText.insert(tk.INSERT, '北向夹角有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)     
                    return 
                    
        elif  self.targetInputVal == 2:
            #-------------------- 文件读取 --------------------#
            # 读取id
            try:
                idInput = self.idEntry.get()
                self.idList = re.split('[,，]',idInput)
                # idList = re.split('[,，]',idInput)
                # self.idList = [float(id) for id in idList]
                if self.idList == ['']:
                    self.resultText.insert(tk.INSERT, 'ID输入有误\n')
                    self.readFlag = 0
            except:
                self.resultText.insert(tk.INSERT, 'ID输入有误\n')
                self.readFlag = 0
                return

            # 读取文件
            self.path = self.pathEntry.get().strip()

            if os.path.isfile(self.path):
                try:
                    self.targetDic = findFromcsv(self.path, self.idList)    # x,y,lon,lat
                    for i in range(len(self.idList)-1, -1, -1):
                        if self.idList[i] not in list(self.targetDic.keys()):
                            self.resultText.insert(tk.INSERT, f'文件不含Id{self.idList[i]}数据\n')
                            self.idList.pop(i)
                    if len(self.idList) < 1:
                        self.readFlag = 0
                        return
                except:
                    self.resultText.insert(tk.INSERT, '文件格式有误\n')
                    self.readFlag = 0
                    return
            else:
                self.resultText.insert(tk.INSERT, '文件路径有误\n')
                self.readFlag = 0
                return

            if self.funcFlag == 1:
                # 读取目标真值经纬度
                try:
                    self.truthLonTarget = float(self.lonTarEntry.get())      # 目标经纬度
                    self.truthLatTarget = float(self.latTarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '目标输入数据有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)     
                    return

                # 读取雷达经纬度
                try:
                    self.lonLidar = float(self.lonLidarEntry.get())         # 雷达经纬度
                    self.latLidar = float(self.latLidarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '雷达数据有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)     
                    return 
            else:
                # 读取目标真值经纬度
                try:
                    self.truthLonTarget = float(self.lonTarEntry.get())      # 目标经纬度
                    self.truthLatTarget = float(self.latTarEntry.get())
                except:
                    self.resultText.insert(tk.INSERT, '目标输入数据有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)     
                    return

                # 读取北向夹角
                try:
                    self.angleNorth = float(self.lonLidarEntry.get())         # 北向夹角
                except:
                    self.resultText.insert(tk.INSERT, '北向夹角有误\n')
                    self.readFlag = 0
                    self.resultText.config(state=tk.DISABLED)     
                    return 
                
    '''
    description: 计算
    param {*} self
    return {*}
    '''    
    def Cal(self):
        self.resultText.config(state=tk.NORMAL)     # 结果框可被修改 
        self.resultText.delete(1.0, 'end')          # 清空输出结果
        self.readFlag = 1                           # 文件读取是否成功

        self.targetInputVal = self.targetInputVar.get()     # 目标输入方式
        self.funcFlag = self.funcVar.get()                  # 功能选择

        if self.targetInputVal == 0:
            self.resultText.insert(tk.INSERT, '未选择输入方式\n')
            self.resultText.config(state=tk.DISABLED)     
            return
        elif self.funcFlag == 0:
            self.resultText.insert(tk.INSERT, '未选择计算项\n')
            self.resultText.config(state=tk.DISABLED)     
            return
        else:
            self.DataRead()

        # 数据读取有误，不往下执行
        if not self.readFlag:
            return
                
        #-------------------- 计算北向夹角 --------------------#
        if self.funcFlag == 1:
            
            self.ELidar, self.NLidar = GPS2UTM(self.latLidar, self.lonLidar)                    # 雷达经纬度转xy
            self.ETarget, self.NTarget = GPS2UTM(self.truthLatTarget, self.truthLonTarget)      # 目标经纬度转xy

            if self.targetInputVal == 1:
                # 使用直接输入目标数据
                # 目标检测x、y,目标真值经纬度，雷达经纬度
                pos = [self.xTarget, self.yTarget, self.ETarget, self.NTarget, self.ELidar, self.NLidar] 
                self.angle = angleCal(pos)
                self.resultText.insert(tk.INSERT, f'北向夹角:{self.angle:1.2f}\n')
            else:
                # 使用文件数据
                self.angleList = []
                for id in self.idList:
                    pos = np.array([np.mean(self.targetDic[id][:, 0]), np.mean(self.targetDic[id][:, 1]), \
                        self.ETarget, self.NTarget, self.ELidar, self.NLidar])
                    self.angle = angleCal(pos)
                    self.angleList.append(self.angle)
                    self.resultText.insert(tk.INSERT, f'Id{id}北向夹角:{self.angle:1.2f}\n')

                if len(self.idList) > 1:
                    self.resultText.insert(tk.INSERT, f'平均北向夹角:{np.mean(self.angleList):1.2f}\n')

        #-------------------- 计算距离 --------------------#
        elif self.funcFlag == 2:

            self.TruthETarget, self.TruthNTarget = GPS2UTM(self.truthLatTarget, self.truthLonTarget)

            if self.targetInputVal == 1:
                # 直接输入
                self.ETarget, self.NTarget = GPS2UTM(self.detLatTarget, self.detLonTarget)
                pos = np.array([self.ETarget, self.NTarget, self.TruthETarget, self.TruthNTarget, self.angleNorth])
                self.dis = disCal(pos)
                self.resultText.insert(tk.INSERT, '距离误差:\n')
                self.resultText.insert(tk.INSERT, f'X方向:{float(self.dis[0]):1.2f}\n')
                self.resultText.insert(tk.INSERT, f'Y方向:{float(self.dis[1]):1.2f}\n')
            else:
                # 文件读取
                for id in self.idList:
                    posList = np.array([0, 0])
                    # 计算检测平均x,y
                    for i in range(self.targetDic[id].shape[0]):
                        posList = posList + np.array(GPS2UTM(self.targetDic[id][i,3], self.targetDic[id][i,2]))
                    posList = posList / self.targetDic[id].shape[0]
                    pos = np.array([posList[0], posList[1], self.TruthETarget, self.TruthNTarget, self.angleNorth])
                    self.dis = disCal(pos)
                    self.resultText.insert(tk.INSERT, f'Id{id}距离误差:\n')
                    self.resultText.insert(tk.INSERT, f'X方向:{float(self.dis[0]):1.2f}\n')
                    self.resultText.insert(tk.INSERT, f'Y方向:{float(self.dis[1]):1.2f}\n')

        #-------------------- 计算雷达 --------------------#
        elif self.funcFlag == 3:
            self.eFirst, self.nFirst = GPS2UTM(self.latFirst, self.lonFirst)
            self.eSecond, self.nSecond = GPS2UTM(self.latSecond, self.lonSecond)

            pos = np.array([[self.eFirst, self.nFirst, self.angleFirst], \
                [self.eSecond, self.nSecond, self.angelSecond]])
            
            self.param = calibCal(pos)
            self.resultText.insert(tk.INSERT, f'副雷达X方向平移:{float(self.param[0]):1.2f}\n')
            self.resultText.insert(tk.INSERT, f'副雷达Y方向平移:{float(self.param[1]):1.2f}\n')
            self.resultText.insert(tk.INSERT, f'副雷达Z轴旋转:{float(self.param[2]):1.2f}\n')
        
        
        self.resultText.config(state=tk.DISABLED)     # 结果框不可被修改 

    '''
    description: 清空输入内容
    param {*} self
    return {*}
    '''    
    def Clear(self):
        self.resultText.config(state=tk.NORMAL)     # 结果框可被修改 

        self.latLidarEntry.config(state=tk.NORMAL)
        self.lonLidarEntry.config(state=tk.NORMAL)
        self.latTarEntry.config(state=tk.NORMAL)
        self.lonTarEntry.config(state=tk.NORMAL)
        self.xTarEntry.config(state=tk.NORMAL)
        self.yTarEntry.config(state=tk.NORMAL)
        self.idEntry.config(state=tk.NORMAL)
        self.pathEntry.config(state=tk.NORMAL)
        
        self.latLidarEntry.delete(0, 'end')
        self.lonLidarEntry.delete(0, 'end')
        self.latTarEntry.delete(0, 'end')
        self.lonTarEntry.delete(0, 'end')
        self.xTarEntry.delete(0, 'end')
        self.yTarEntry.delete(0, 'end')
        self.idEntry.delete(0, 'end')
        self.pathEntry.delete(0, 'end')   
        self.resultText.delete(1.0, 'end')

        self.resultText.config(state=tk.DISABLED)     # 结果框不可被修改 

        self.TargetInputChange()


if __name__ == '__main__':

    Application()



