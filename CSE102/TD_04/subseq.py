#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:14:22 2022

@author: alixb1908
"""

def choose_gen(s,k):
    if k == 0:
        yield []
    elif k <= len(s):     
        #first element is in the list
        x = s[0]
        for sub in choose_gen(s[1:],k-1):
            subset = [x] + sub
            yield subset
        for sub in choose_gen(s[1:],k):
            #first element not in the list
            yield sub

def subseq(s):
    for k in range(len(s)+1):
        yield from choose_gen(s, k)