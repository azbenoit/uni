#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 16:43:03 2022

@author: alixb1908
"""
#ugly part to create the lists
# =============================================================================
# to_remove = [[x] for x in range(4)]
# sublist = list(range(4))
# l=[]
# for _ in range(len(to_remove)):
#     l.append([])
# for i in range(len(to_remove)):
#     for s in sublist:
#         l[i].append(s)
# print(f'Initial list: {l}')
# =============================================================================





#old way
to_remove = [[x] for x in range(4)]
sublist = list(range(4))
l = [sublist]*len(to_remove)


# Part that actually does the removing
for i in range(len(l)):
    l[i].remove(i)
    print(f'removed {i} from l[{i}]: {l}')
    
    
    
    
    
    
    
    