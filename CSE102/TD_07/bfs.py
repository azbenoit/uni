#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:44:31 2022

@author: alixb1908
"""

 # shortest_route_len([[1, 2], [2], [3], []], 0, 3) should return 2

def shortest_route_len(G, s, t, count = None):
    if count is None:
        count = 1
    if not s is list:
        s = [s]
    
    # i = s[0]
    for i in s:
        if i == t:
            return count
    next_s = []
    print(s)
    for i in s:
        for k in G[i]:
            next_s.append(k)
    next_s = list(set(next_s))
    print(next_s)
    # return shortest_route_len(G, next_s, t, count+1)
        
        
        