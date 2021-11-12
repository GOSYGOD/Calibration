# -*- coding: utf-8 -*-
'''
Author: Jiaxi Zheng
Date: 2021-11-01 13:44:13
LastEditTime: 2021-11-02 10:53:14
LastEditors: Jiaxi Zheng
Description: 
FilePath: \相关软件\angle.py
'''

import tkinter as tk
import math
from GPS2UTM import *

'''
description: 生成上位机，功能排版
param {*}
return {*}
'''
class Application(tk.Frame):
    def __init__(self):
        # 初始化root，面积
        self.root = tk.Tk()
        self.root.title('航向角计算')
        self.width = 600
        self.height = 300
        self.root.geometry(f'{self.width}x{self.height}')
        #self.root.resizable(False, False)

        # 整体框架pan
        self.frameAll = tk.Frame(self.root)
        self.frameAll.pack(fill='both', expand=1)
        
        # 上中下三个区域（Top, Mid, Bot）
        self.panTop = tk.PanedWindow(self.frameAll, orient=tk.VERTICAL, sashrelief='sunken')
        self.panMid = tk.PanedWindow(self.frameAll, orient=tk.VERTICAL, sashrelief='sunken')
        self.panBot = tk.PanedWindow(self.frameAll, orient=tk.HORIZONTAL, sashrelief='sunken')
        self.panTop.pack(fill='x', side=tk.TOP)
        self.panMid.pack(fill='x', side=tk.TOP)
        self.panBot.pack(fill='both', expand=1)

        # Top区域——雷达数据
        self.frameLidar = tk.LabelFrame(self.panTop, text='雷达', height=self.height / 3, relief='sunken')
        self.panTop.add(self.frameLidar)
        self.frameLidar.propagate(0)

        # Mid区域——目标数据
        self.frameTarget = tk.LabelFrame(self.panMid, text='目标', height=self.height / 3, relief='sunken')
        self.panMid.add(self.frameTarget)
        self.frameTarget.propagate(0)
        
        # Bottom区域——结果
        self.frameRes = tk.LabelFrame(self.panBot, text='结果', relief='sunken', width=self.width / 3)
        self.panBot.add(self.frameRes)
        self.frameRes.propagate(0)

        # Bottom区域——按钮
        self.frameBut = tk.LabelFrame(self.panBot, text='功能', relief='sunken')
        self.panBot.add(self.frameBut)
        self.frameBut.propagate(0)
        
        self.setframeLidar()   # 雷达区域布局
        self.setframeTarget()  # 目标区域布局
        self.setframeRes()     # 结果区域布局
        self.setframeBut()     # 按钮区域布局
        
        self.root.mainloop()
    
    '''
    description: 雷达区域布局，雷达经纬度
    param {*} self
    return {*}
    '''    
    def setframeLidar(self):
        # 雷达经度
        self.lonLidarLabel = tk.Label(self.frameLidar, text='   经度', font=('宋体', 15), pady=5)
        self.lonLidarEntry = tk.Entry(self.frameLidar, font=('宋体', 15))
        
        # 雷达纬度
        self.latLidarLabel = tk.Label(self.frameLidar, text='     纬度', font=('宋体', 15), pady=5)
        self.latLidarEntry = tk.Entry(self.frameLidar, font=('宋体', 15))
        
        # 布局
        self.lonLidarLabel.grid(row=0,column=0)
        self.lonLidarEntry.grid(row=0,column=1)
        self.latLidarLabel.grid(row=0,column=2)
        self.latLidarEntry.grid(row=0,column=3)

    '''
    description: 目标区域布局，目标经纬度、横纵坐标
    param {*} self
    return {*}
    '''    
    def setframeTarget(self):
        # 目标经度
        self.lonTargetLabel = tk.Label(self.frameTarget, text=' 经度', font=('宋体', 15), pady=5)
        self.lonTarEntry = tk.Entry(self.frameTarget, font=('宋体', 15))
        
        # 目标纬度
        self.latTargetLabel = tk.Label(self.frameTarget, text='   纬度', font=('宋体', 15), pady=5)
        self.latTarEntry = tk.Entry(self.frameTarget, font=('宋体', 15))
        
        # 目标横坐标
        self.xTargetLabel = tk.Label(self.frameTarget, text=' 横坐标', font=('宋体', 15), pady=5)
        self.xTarEntry = tk.Entry(self.frameTarget, font=('宋体', 15))

        # 目标纵坐标
        self.yTargetLabel = tk.Label(self.frameTarget, text='   纵坐标', font=('宋体', 15), pady=5)
        self.yTarEntry = tk.Entry(self.frameTarget, font=('宋体', 15))
        
        # 布局
        self.lonTargetLabel.grid(row=0, column=0, sticky=tk.constants.E)
        self.lonTarEntry.grid(row=0, column=1)
        self.latTargetLabel.grid(row=0, column=2, sticky=tk.constants.E)
        self.latTarEntry.grid(row=0, column=3)
        self.xTargetLabel.grid(row=1, column=0)
        self.xTarEntry.grid(row=1, column=1)
        self.yTargetLabel.grid(row=1, column=2)
        self.yTarEntry.grid(row=1, column=3)    
    
    '''
    description: 结果区域布局，显示正北夹角
    param {*} self
    return {*}
    '''    
    def setframeRes(self):
        # 结果框
        self.resultLabel = tk.Label(self.frameRes, text='正北夹角', font=('宋体', 15), pady=30)
        self.resultText = tk.Text(self.frameRes, width=10, height=1, font=('宋体', 15), state=tk.DISABLED)

        # 布局
        self.resultLabel.pack()
        self.resultText.pack()

    '''
    description: 按钮区域布局，计算、清空、退出
    param {*} self
    return {*}
    '''    
    def setframeBut(self):
        self.start = tk.Button(self.frameBut, text='计算', command=self.Cal)
        self.clear = tk.Button(self.frameBut, text='清空', command=self.Clear)
        self.QUIT = tk.Button(self.frameBut, text='退出', command=self.root.destroy)

        # 布局
        self.start.pack(fill='both', expand=1, side=tk.LEFT)
        self.clear.pack(fill='both', expand=1, side=tk.LEFT)
        self.QUIT.pack(fill='both', expand=1, side=tk.RIGHT)

    '''
    description: 正北夹角计算
    param {*} self
    return {*}
    '''    
    def Cal(self):
        self.resultText.delete(1.0, 'end')          # 清空输出结果
        self.resultText.config(state=tk.NORMAL)     # 结果框可被修改 

        try:
            # 读取输入数据
            self.lonLidar = float(self.lonLidarEntry.get())     # 雷达经纬度
            self.latLidar = float(self.latLidarEntry.get())
            self.lonTarget = float(self.lonTarEntry.get())      # 目标经纬度
            self.latTarget = float(self.latTarEntry.get())
            self.xLidar = float(self.xTarEntry.get())           # 雷达检测的目标相对位置
            self.yLidar = float(self.yTarEntry.get())

            # 经纬度转xy
            self.ELidar, self.NLidar = GPS2UTM(self.latLidar, self.lonLidar)
            self.ETarget, self.NTarget = GPS2UTM(self.latTarget, self.lonTarget)

            # 北向夹角计算
            '''
            x' = x * cos + y * sin
            y' = y * cos - x * sin
            逆时针旋转为正
            '''
            self.xEarth = self.ETarget - self.ELidar
            self.yEarth = self.NTarget - self.NLidar
            self.rad = math.atan2(self.xEarth * self.yLidar - self.xLidar * self.yEarth, \
                self.yEarth * self.yLidar + self.xEarth * self.xLidar)
            self.angle = (self.rad / math.pi * 180) % 360
            self.resultText.insert(tk.INSERT, self.angle)
        except:
            self.resultText.insert(tk.INSERT, 'Error')
            
    '''
    description: 清空输入内容
    param {*} self
    return {*}
    '''    
    def Clear(self):
        self.latLidarEntry.delete(0, 'end')
        self.lonLidarEntry.delete(0, 'end')
        self.latTarEntry.delete(0, 'end')
        self.lonTarEntry.delete(0, 'end')
        self.xTarEntry.delete(0, 'end')
        self.yTarEntry.delete(0, 'end')
        self.resultText.delete(1.0, 'end')

Application()