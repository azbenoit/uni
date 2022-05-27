#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:23:45 2022

@author: alixb1908
"""
import random

def experiment(N,K):
    C = 100_000                              # Number of trials
    S = sum(exploop(N,K) for _ in range(C)) # Number of successes
    return S / C  
    

def exploop(N,K):
    streak = 0
    for _ in range(N):
        heads = random.choice([False,True])
        if heads:
            streak += 1
        else:
            streak = 0
        if streak == K:
            return True
    return False
            
        