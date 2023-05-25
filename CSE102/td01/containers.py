#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:24:40 2022

@author: alixb1908
"""

class Rdict:
    def __init__(self, A=None , B=None):
        if A is None or B is None:
            self.__bwd = {}
            self.__fwd = {}
        self.__bwd = {B[i]:A[i] for i in range(len(A))}
        self.__fwd = {A[i]:B[i] for i in range(len(A))}   
        
    def associate(self,a,b):
        if a in self.__fwd.keys() or b in self.__bwd.keys():
            raise ValueError
        else:
            self.__fwd[a] = b
            self.__bwd[b] = a
    def __len__(self):
        return len(self.__fwd)
    
    def __getitem__(self,p):
        (k,m) = p
        if k > 0 and m in self.__fwd.keys():
            return self.__fwd[m]
        elif k < 0 and m in self.__bwd.keys():
            return self.__bwd[m]
        else:
            return None
        
    def __setitem__(self, p,q):
        (k,m) = p
        if k > 0 and m not in self.__fwd.keys():
            self.__fwd[m] = q
        elif k < 0 and m not in self.__bwd.keys():
            self.__bwd[m] = q