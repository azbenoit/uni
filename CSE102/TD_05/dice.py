#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:24:36 2022

@author: alixb1908
"""

import random


def roll(D):
    k = len(D)
    r = random.random()
    brackets = list(D)
    for i in range(1,k):
        brackets[i] += brackets[i-1]
    for i in range(k):
        if r < brackets[i]:
            return i+1

def rolls(D,N):
    k = len(D)
    tup = [0]*k
    for _ in range(N):
        n = roll(D) - 1
        tup[n] += 1
    return tuple(tup)

import matplotlib.pyplot as plt

def plot(ns):
    N  = sum(ns)
    ns = [float(x) / N for x in ns]
    plt.bar(range(len(ns)), height=ns)
    plt.xticks(range(len(ns)), [str(i+1) for i in range(len(ns))])
    plt.ylabel('Probability')
    plt.title('Biased die sampling')
    plt.show()

