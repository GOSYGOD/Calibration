# -*- coding: utf-8 -*-
'''
Author: Jiaxi Zheng
Date: 2021-11-02 14:57:25
LastEditTime: 2021-11-16 17:32:56
LastEditors: Jiaxi Zheng
Description: 
FilePath: \标定上位机\findFromcsv.py
'''

import csv
import argparse
import numpy as np
import re

# find car from CSV according to ID
def findFromcsv(filepath, idList):

    csvreader = csv.reader(open(filepath))
    dic = {}            # All col

    for id in idList:
        dic.setdefault(id, [])

    for row in csvreader:
        if str(row[4]) in idList:
            dic[str(row[4])].append([float(row[5]), float(row[6]), float(row[15]), float(row[16])]) # x,y,lon,lat
    
    for key in list(dic.keys()):
        if len(dic[key]) < 1:
            del dic[key]
        else:
            dic[key] = np.array(dic[key])

    return dic

if __name__ == '__main__':
    # Parsing id and path
    parser = argparse.ArgumentParser(description="parameter help")
    parser.add_argument("-path", "--filepath", type=str, help="设置csv文件路径")
    parser.add_argument("-id", "--targetId", type=str, help="查找的目标ID")
    args = parser.parse_args()
    targetId = args.targetId
    filepath = args.filepath

    targetId = re.split('[,，]', targetId)

    result = findFromcsv(filepath, targetId)
    data = result['28577'][:,0]
    print(np.mean(data))
