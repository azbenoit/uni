#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:26:46 2022

@author: alixb1908
"""

def slice_dice(n, s, dice):
    return [dice[i * s:i * s + s] for i in range(n)]


def win_probability(die1, die2):
    prob = 0
    n = len(die1)
    for v1 in die1:
        for v2 in die2:
            if v1 > v2:
                prob += 1/(n*n)
    return prob 
            
def beats(die1,die2):
    return win_probability(die1, die2) > 0.5


def get_dice(n, s, dice, left = None): #Numbers left
    # print(dice)
    if len(dice) == n*s and beats(dice[-s:] , dice[0:s]):
        yield dice
    left = set(range(n*s))-set(dice) if left is None else left
    if len(dice) % s != s-1:
        for i in left:
            # print(i)
            if i > dice[-1] or len(dice) % s == 0:
                dice.append(i)
                yield from get_dice(n, s, dice, left- {i})
                dice.remove(i)
    else:
        for i in left:
            # print(i)
            if i > dice[-1]:
                dice.append(i)
                if beats(dice[-2*s:-s] , dice[-s:]) or len(dice) == s:# beats(dice[-s:] , dice[0:s+1])):
                    yield from get_dice(n, s, dice, left - {i})
                    dice.remove(i)
                else:
                    dice.remove(i) 
            

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # slidie = slice_dice(n, len(dice)/n, dice)
    # for d in slidie
    #if get_dice(n,s,dice+newnumb,left -newnumb)!= False
    #yield the thing
    
    # if get_dice(n, s, dice)
    # incorporate + getdice(n, s-1, dice)
    # if n == 1 or n == 2 or s == 1 or s==2:
    #     return None
    
    