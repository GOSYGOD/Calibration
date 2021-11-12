# -*- coding: utf-8 -*-
'''
Description: 
Version: 1.0
Author: 郑加希
Date: 2021-04-02 14:32:55
LastEditors: Jiaxi Zheng
LastEditTime: 2021-11-01 16:44:20
'''

import math
import numpy as np

def GPS2UTM(lat, lon):

    a = 6378.137; e = 0.0818192; k0 = 0.9996; E0 = 500; N0 = 0
    
    #position = zip(latitude, longitude)
    
    zonenum = np.fix(lon / 6) + 31
    lamda0 = ((zonenum - 1) * 6 - 180 + 3) * math.pi / 180
    phi = lat * math.pi / 180
    lamda = lon * math.pi / 180

    v = 1 / math.sqrt(1 - e * e * math.sin(phi) * math.sin(phi))
    A = (lamda - lamda0) * math.cos(phi)
    T = math.tan(phi) * math.tan(phi)
    C = e * e * math.cos(phi) * math.cos(phi) / (1 - e * e)
    s = (1 - e * e / 4 - 3 * math.pow(e, 4) / 64 - 5 * math.pow(e, 6) / 256) * phi - \
        (3 * e * e / 8 + 3 * math.pow(e, 4) / 32 + 45 * math.pow(e, 6) / 1024) * math.sin(2 * phi) + \
        (15 * math.pow(e, 4) / 256 + 45 * math.pow(e, 6) / 1024) * math.sin(4 * phi) - \
        35 * math.pow(e, 6) / 3072 * math.sin(6 * phi)
    UTME = (E0 + k0 * a * v * (A + (1 - T + C) * math.pow(A, 3) / 6 + (5 - 18 * T + T * T) * math.pow(A, 5) / 120)) * 1000
    UTMN = (N0 + k0 * a * (s + v * math.tan(phi) * (A * A / 2 + (5 - T + 9 * C + 4 * C * C) * math.pow(A, 4) / 24 + \
        (61 - 58 * T + T * T) * math.pow(A, 6) / 720))) * 1000
    
    return UTME, UTMN

if __name__ == '__main__':
    x = 40.0465080
    y = 116.2906580
    res = GPS2UTM(x,y)
    print(res[0])
    print(res[1])