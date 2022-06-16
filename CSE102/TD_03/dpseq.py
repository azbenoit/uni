#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:14:49 2022

@author: alixb1908
"""

def next_seq(alphas, us):
    s = 0
    for i in range(len(us)):
        s+=alphas[i]*us[i]
    return s

def u(alphas, us, n):
    for i in range(n):
        us.append(next_seq(alphas, us))
        us.remove(us[0])
    return us[0]

