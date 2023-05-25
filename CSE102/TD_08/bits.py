#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:31:06 2022

@author: alixb1908
"""

def uint16_to_bitstring(x):
    byte = [0]*16
    for i in range(16):
        byte[i] = x // 2**(15-i)
        x -= byte[i]*2**(15-i)
    return byte

def bitstring_to_uint16(bs):
    x = 0
    for i in range(len(bs)):
        x += bs[i] * 2**(15-i)
    return x

def mod_pow2(x, k):
    res = x >> k
    # print(res)
    return x - (res<<(k))
    
def is_pow2(x):
    if x == 0:
        return False
    if x == 1:
        return True
    x -= 1
    while True:
        y = x >> 1
        if y<<1 == x:
            return False
        if y == 0:
            return True 
        x = x >>1

# def set_mask(w, m):
#     """set every bit position which is 1 in m, to 1 in w"""
#     return w | ((1 << m+1)-1)
# def toggle_mask(w, m):
#     """toggle every bit position which is 1 in m, in w"""
#     return w ^ ((1 << m+1)-1)

# def clear_mask(w, m):
#     """set every bit position which is 1 in m, to 0 in w"""
#     return w & (~ ((1 << m+1)-1))

def set_mask(w, m):
    """set every bit position which is 1 in m, to 1 in w"""
    return w | m
def toggle_mask(w, m):
    """toggle every bit position which is 1 in m, in w"""
    return w ^ m

def clear_mask(w, m):
    """set every bit position which is 1 in m, to 0 in w"""
    return w & ~ m




























