# -*- coding: utf-8 -*-
'''
Author: Jiaxi Zheng
Date: 2021-11-02 14:57:25
LastEditTime: 2021-11-04 10:24:29
LastEditors: Jiaxi Zheng
Description: 
FilePath: \相关软件\findFromcsv.py
'''

import csv
import argparse

# find car from CSV according to ID
def findFromcsv(filepath, idList):

    csvreader = csv.reader(open(filepath))
    dic = {}            # All col
    first = True
    for row in csvreader:
        if first:
            for id in idList:
                dic.setdefault(id, [])
            first = False
        if str(row[4]) in idList:
            dic[str(row[4])].append([row[5], row[6], row[15], row[16]]) # x,y,lon,lat
    
    for key in list(dic.keys()):
        if len(dic[key]) < 1:
            del dic[key]

    return dic

if __name__ == '__main__':
    # Parsing id and path
    parser = argparse.ArgumentParser(description="parameter help")
    parser.add_argument("-path", "--filepath", type=str, help="设置csv文件路径")
    parser.add_argument("-id", "--targetId", type=str, help="查找的目标ID")
    args = parser.parse_args()
    targetId = args.targetId
    filepath = args.filepath
    
    result = findFromcsv(filepath, targetId)
    print(result)