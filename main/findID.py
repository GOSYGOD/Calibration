'''
Author: Jiaxi Zheng
Date: 2021-11-02 15:11:00
LastEditTime: 2021-11-02 15:40:23
LastEditors: Jiaxi Zheng
Description: 
FilePath: \相关软件\findID.py
'''
# coding:utf-8
import csv
import time
import argparse
import os 
import sys
from datetime import datetime
from datetime import timedelta

# find car from CSV according to ID
def findFromcsv(filepath, idList):

    csvreader = csv.reader(open(filepath))
    dic = {}            # All col
    dicExam = {}        # Exam format

    first = True
    for row in csvreader:
        if first:
            for id in idList:
                dic.setdefault(id, [])
                dicExam.setdefault(id, [])
                dic[id].append(row)
                num = ['帧序号']
                num.extend(['t0时间戳', 't1时间戳', '厂商编号', '目标ID', '类型', '经度', '纬度', '速度', '航向角', '长度', '宽度', '高度'])
                dicExam[id].append(num)
            first = False
        if str(row[4]) in idList:
            dic[str(row[4])].append(row)
            #print(dicExam)
            #print([len(dicExam[row[3]]), row[0], row[1], 1, 1, 1, row[15], row[16], row[11], row[12], row[9], row[8], row[10]])
            dicExam[row[4]].append([len(dicExam[row[4]]), row[0], row[1], 1, row[4], row[13], row[15], row[16], row[11], row[12], row[9], row[8], row[10]])

    return dic, dicExam

# save info in CSV
def saveListTocsv(filepath, listData):
    with open(filepath, "w+", newline="") as f:
        writer = csv.writer(f)
        if len(listData) > 0:
            if type(listData[0]) != list:
                writer.writerow(listData)
                return
        for data in listData:
            writer.writerow(data)

if __name__ == '__main__':

    # Parsing id and path
    parser = argparse.ArgumentParser(description="parameter help")
    parser.add_argument("-path", "--filepath", type=str, help="设置csv文件路径")
    parser.add_argument("-id", "--targetId", type=str, help="查找的目标ID")
    args = parser.parse_args()
    targetId = args.targetId
    filepath = args.filepath

    if targetId == None:
        print('请输入目标ID')
    if filepath == None:
        print('请输入CSV文件路径')
    if (targetId == None) | (filepath == None):
        sys.exit()

    # path prepare
    idList = targetId.split(',')

    originPath, originFile = os.path.split(filepath)
    AllBox, fileType= os.path.splitext(originFile)
    examPath = os.path.join(originPath, 'exam') # 给检测中心
    savePath = os.path.join(originPath, 'BoxInfo')
    try:
        os.mkdir(examPath)
        os.mkdir(savePath)
    except:
        pass

    # find and save
    dic, dicExam = findFromcsv(filepath, idList)
    for id in idList:
        print('ID ' + id + ' is processing')
        #saveName = '交通参与者感知数据—万集'
        saveName = AllBox + '_{}.csv'.format(id)
        saveListTocsv(os.path.join(savePath, saveName), dic[id])
        print('ID ' + id + ' is saving as ' + os.path.join(savePath, saveName))
        saveListTocsv(os.path.join(examPath, saveName), dicExam[id])
        print('ID ' + id + ' is saving as ' + os.path.join(examPath, saveName))
        print('---------------------------------------------------')