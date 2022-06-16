#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 12:40:43 2022

@author: alixb1908
"""


def fibs():
    r0,r1 = 0,1
    while True:
        yield r0
        r0,r1 = r1, r0+r1
        
def prefix_sums(k):
    r0, i = k, 0
    while True:
        yield r0
        i += 1
        r0 += k + i 
        
    
# def choose_gen(s,k):
#     # stop = k-1
#     if k == 0:
#         return []
#     elif k > len(s):
#         return None
#     elif k == len(s):
#         return s
#     else:
#         # for x in s:
#         #     i = s.index(x)
#         #     prevl = choose(s[:i] + s[i+1:],k-1)
#         #     if prevl != []:
#         #         for sub in prevl:
#         #             subset = [x] + sub
#         #             subset.sort()
#         #             if subset not in l: 
#         #                 yield subset
#         #     elif [x] not in l: #if previous list is []
#         #         yield [x]
# def test(s,k):
    
    

        

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

            
            
            
            
            
            
            
            