#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 14:50:42 2022

@author: alixb1908
"""

# required([[1], [2, 3], [], [2], [2]], 1) --> 3
def required_rec(G,c, count = None):
    if count is None: 
        count = {c}
    else:
        count = count.union({c})
    for i in G[c]:
        if i not in count:
            count = count.union(required_rec(G, i, count))
    return count

def required(G,c):
    return len(required_rec(G, c))

G = [[1],[0]]

def required_list(G, c):
    l = list(required_rec(G, c))
    l.sort()
    return l

def revert_edges(A):
    R = []
    for _ in range(len(A)):
        R.append([])
    for i in range(len(A)):
        for k in range(len(A[i])):
            j = A[i][k]
            R[j].append(i)
    return R


def needed_for(G, c):
    count = 0
    for i in range(len(G)):
        count += c in required_list(G, i)
    return count
      