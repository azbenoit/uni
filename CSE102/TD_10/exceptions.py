#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 14:48:02 2022

@author: alixb1908
"""

class InvalidInput(Exception):
    pass

class Found(Exception):
    solution = None

def sum_of_input():
    # 
    nums = []
    while True:
        try:
            i = input("Enter number: ")
            try:
                nums.append(int(i))
            except:
                raise InvalidInput('Invalid input')
                
        except EOFError:
            break
    return sum(nums)



def subset_sum(nm, S, M):
    # "nm" is the set of available numbers
    # "M" is the target sum
    # "S" is the current partial solution

    nS = sum(S) # The sum of the partial solution
    
    if nS > M:
        # "S" is a non-feasible solution.
        # We reject it.
        return None
    
    if nS == M:
        # S is a valid solution.
        # We accept it.
        Found.solution = S
        raise Found(S)

    for i in nm:
        # Otherwise, we try to extend S with the integers
        # from "nm" - 1 by 1 and continue recursively.
        rS = subset_sum(
            nm.difference([i]), # We remove "i" from "nm"
            S.union([i])      , # We add "i" to "S"
            M                   # The targeted sum is unchanged
        )
        
        if rS is not None:
            # We found a solution (recursively)
            # We return it
            Found.solution = rS
            raise Found(rS)
    
    # We tried all the numbers in "nm" without finding
    # a solution. We report the failure with "None"
    return None