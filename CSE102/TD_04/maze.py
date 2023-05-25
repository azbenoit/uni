#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:28:23 2022

@author: alixb1908
"""

 

def maze(m,n,i,j,cache = None):
    cache = {} if cache is None else cache
    # print(cache)
    if i == n-1 == j:
        return [(i,j)]
    if (i,j) in cache:
        return cache[i,j]
    if j != n-1 and m[i][j+1] == 1:
        sol = maze(m,n,i,j+1,cache)
        if sol != False:
            # print([(i,j)] + maze(m,n,i,j+1))
            cache[i,j] = [(i,j)] + maze(m,n,i,j+1,cache)
            return cache[i,j]
    if i != n-1 and m[i+1][j] == 1:
        sol = maze(m,n,i+1,j,cache)
        if sol != False:
            # print([(i,j)] + maze(m,n,i+1,j))
            cache[i,j] = [(i,j)] + maze(m,n,i+1,j,cache)
            return cache[i,j]
    cache[i,j] = False
    return cache[i,j]
    
        
    
        