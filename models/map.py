# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-18
"""

import pandas as pd
import numpy as np


class Map():
    def __init__(self, x, y, z):
        self.map = np.zeros((x, y, z), dtype=np.int)
        self.map[0,0,0] = 4
        self.map[0,1,0] = 1
        self.map[0,2,0] = 8
        self.map[0,0,1] = 2
        print(self.map)
        print("****************")
    
    def view_from_y(self):
        return np.max(self.map, axis=1)

class Land():
    def __init__(self, x, y, z, **kwargs):
        pass
        

if __name__ == "__main__":
   print(Map(4,4,4).view_from_y())