#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:52:06 2022

@author: alixb1908
"""
import sys
sys.setrecursionlimit (10 ** 6)

# 1, 3, 7, 9
def transacts_num(n, cache = None):
    cache = {} if cache is None else cache
    l = [1,3,7,9]
    if n in l:
        return 1
    if n == 0:
        return 0
    if n not in cache:
        s = []
        for d in l:
            if d < n:
                s.append(1 + transacts_num(n-d,cache))  
        cache[n] = min(s)
    return cache[n]
    