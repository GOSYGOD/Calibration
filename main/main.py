# -*- coding: utf-8 -*-
'''
Author: Jiaxi Zheng
Date: 2021-11-01 11:28:59
LastEditTime: 2021-11-01 13:44:59
LastEditors: Jiaxi Zheng
Description: 
FilePath: \相关软件\main.py
'''

import argparse
from Application import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameter help')
    parser.add_argument('-p', '--filepath', type=str, help='')