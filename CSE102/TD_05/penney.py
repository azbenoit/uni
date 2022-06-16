#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:24:11 2022

@author: alixb1908
"""

import random

def experiment():
    C = 100_000                              # Number of trials
    N = sum(exploop() for _ in range(C)) # Number of successes
    return N / C  
    

def exploop(): #p1 wins: return True, else False (p2 wins)
    window = [random.choice([False,True]) for _ in range(3)]
    while True: #heads True
        if window == [True, True, False]:
            return True
        if window == [False,True,True]:
            return False
        heads = random.choice([False,True])
        window.remove(window[0])
        window.append(heads)

#Player 1 has a roughly 25% chance of winning
#This is counterintuitive, as one would expect a 50% chance of winning
            
            
    