#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 09:18:01 2022

@author: alixb1908
"""

# import math


def matrix_to_adjlist(M):
    adj = []
    for i in range(len(M)):
        adj.append([])
        for j in range(len(M[i])):
            if M[i][j]:
                adj[i].append(j)
    return adj
                
G = [[1,2] , [] , [1]]
F = [[1,2] , [0] , [0]] 


def is_symmetric(A):
    for i in range(len(A)):
        for k in range(len(A[i])):
            j = A[i][k]
            if i not in A[j]:
                return False
    return True

def revert_edges(A):
    R = []
    for _ in range(len(A)):
        R.append([])
    for i in range(len(A)):
        for k in range(len(A[i])):
            j = A[i][k]
            R[j].append(i)
    return R
    





























