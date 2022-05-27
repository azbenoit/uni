#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 14:21:34 2022

@author: alixb1908
"""

import sys
sys.setrecursionlimit (10 ** 6)

def catalan(n):
    if n == 0:
        return 1
    else:
        s = 0
        for i in range(n):
            s+=catalan(i)*catalan((n-1)-i)
        return s

def catalan_td(n, cache = None):
    cache = {} if cache is None else cache
    if n not in cache:
        # This is the first time we compute `catalan(n)`
        # Compute it and store the result in `cache[n]`
        if n == 0:
            cache[0] = 1
        else:
            s = 0
            for i in range(n):
                s+=catalan_td(i,cache)*catalan_td(n-1-i,cache)
            cache[n] = s
    # At that point, we know that `cache[n]` exists and
    # is exactly the n-th Catalan number
    #
    # We simply return it.
    return cache[n]

def next_catalan(cs):
    if len(cs) == 0:
        return 1
    else:
        s = 0
        for i in range(len(cs)):
            s+=cs[i]*cs[len(cs)-1-i]
        return s
    
def catalan_bu(k):
    cs = []
    for i in range(k+1):
        cs.append(next_catalan(cs))
    return cs[k] 





























