#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 14:39:30 2022

@author: alixb1908
"""

def binom_td(n, k, cache = None):
    cache = {} if cache is None else cache
    if (n,k) in cache:
        return cache[n,k]
    if (k == 0):
        cache[n,k]=1
        return 1
    if (k > n):
        cache[n,k]=0
        return 0
    else:
        cache[n,k]= binom_td(n-1,k,cache) + binom_td(n-1,k-1,cache)
        print(f'calculating n: {n} k: {k}')
        return cache[n,k]
    
def parts_td(n, k = None, cache = None):
    cache = {} if cache is None else cache
    if k is None:
        s = 0 
        for i in range(n+1):
            s+= parts_td(n,i,cache)
        return s
        
    if (n,k) in cache:
        return cache[n,k]
    
    if k == 1 or k==n:
        return 1
    if k > n or k <=0:
        return 0
    cache[n,k] = parts_td(n-1,k-1,cache) + parts_td(n-k, k,cache)
    return cache[n,k]



def parts_bu(n):
    cache = [[0 for _ in range(n+1)] for _ in range(n+1)]
    for i in range(n+1):
        cache[i][1] = 1
    for j in range(n+1):
        for k in range(j+1):
            if j > 0 and k > 0:
                cache[j][k] = cache[j-1][k-1] + cache[j-k][k]
    print(cache)
    return sum([x for x in cache[n]])
                
        
        











