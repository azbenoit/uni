#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 15:12:57 2022

@author: alixb1908
"""

def binom(n,k):
    if k == 0:
        return 1
    elif k > n:
        return 0
    else:
        return binom(n-1,k) + binom(n-1,k-1)
    
def choose(s, k):
    if k <= len(s)//2:
        return small_choose(s, k)
    else:
        ch = small_choose(s, len(s)-k)
        # l = [s]*len(ch)
        l = []
        for _ in range(len(ch)):
            l.append([])
        for i in range(len(ch)):
            for e in s:
                l[i].append(e)
        
        n = len(l)
        for i in range(n):
            for c in ch[i]:
        #         print(f'i: {i}')
        #         print(f'c: {c}')
        #         print(l[i])
        #         print(l)
                l[i].remove(c)
        #         print(l)

        return l
    

def small_choose(s,k):
    l = []
    if k == 0:
        return [[]]
    elif k == 1:
        return [[x] for x in s]
    elif k > len(s):
        return None
    elif k == len(s):
        return [s]
    else:
        #first element is in the list
        x = s[0]
        i = 0
        prevl = choose(s[i+1:],k-1) 
        for sub in prevl:
            subset = [x] + sub
            l.append(subset)
        #first element not in the list
        prevl = choose(s[1:],k)
        for sub in prevl:
            l.append(sub)
                
    return l
        
        
        
# def small_choose(s,k):
#     l = []
#     if k == 0:
#         return [[]]
#     elif k == 1:
#         return [[x] for x in s]
#     elif k > len(s):
#         return None
#     elif k == len(s):
#         return [s]
#     else:
#         for x in s:
#             i = s.index(x)
#             prevl = choose(s[:i]+s[i+1:],k-1) #removed s[:i]+, added -i 
#             for sub in prevl:
#                 if x < sub[0]:
#                     subset = [x] + sub
#                     l.append(subset)
#     return l


def permutations(s): 
    l = []
    if len(s) == 1 or len(s) == 0:
        return [s]
    else:
        ns = s[1:]
        prevl = permutations(ns)
        for sub in prevl:
            for k in range(len(sub) +1):
                l.append(sub[:k] + [s[0]] + sub[k:])
    return l
                
                
                    
                
# def permutations(s): 
#     l = []
#     if len(s) == 1 or len(s) == 0:
#         return [s]
#     else:   
#         for x in s:
#             i = s.index(x)
#             prevl = permutations(s[:i] + s[i+1:])
#             if prevl != []:
#                 for sub in prevl:
#                     subset = [x] + sub
#                     if subset not in l: 
#                         l.append(subset)
#             elif [x] not in l:
#                 l.append([x])
#     return l
            


def not_angry(n):
    if n == 0:
        return 1
    if n == 1:
        return 2
    return  not_angry(n-2) + not_angry(n-1)










# =============================================================================
# 
# 
# 
# 
# 
# def choose(s, k):
#     l = []
#     if k == 0:
#         return [[]]
#     elif k == 1:
#         return [[x] for x in s]
#     elif k > len(s):
#         return None
#     elif k == len(s):
#         return [s]
#     else:
#         for x in s:
#             i = s.index(x)
#             prevl = choose(s[:i]+s[i+1:],k-1) #removed s[:i]+, added -i 
#             # print(prevl)
#             # if prevl != []:
#             for sub in prevl:
#                 subset = [x] + sub
#                     # subset.sort()
#                     # if subset not in l: 
#                 l.append(subset)
#             # elif [x] not in l:
#             #     l.append([x])
#     return l
# 
# 
# 
# 
# 
# =============================================================================

















            