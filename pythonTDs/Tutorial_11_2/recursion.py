#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 10:16:42 2021

@author: alixb1908
"""
import sys
sys.setrecursionlimit(120)


def is_palindrome(word_test):
    """Check if input is a palindrome."""
    if word_test == '':
        return True
    shortened = word_test[1:-1]
    if(word_test[0] == word_test[-1]):
        if(len(shortened) <= 1):
            return True
        else:
            return is_palindrome(shortened)
    else:
        return False
    
def rec_pow(a, b):
    """Compute a**b recursively"""
    if b == 0:
        return 1
    if b == 1:
        return a
    if b % 2 == 0:
        return rec_pow(a,b/2)**2
    else:
        return rec_pow(a, (b-1)/2) ** 2 *a
    
    
def binary_search(sorted_list, l, u, e):
    """Return the position of the element in the sublist of sorted_list
    starting at position lower up to (but excluding) position upper 
    if it appears there. Otherwise return -1.
    """
    print(sorted_list[l:u])
    
    if len(sorted_list[l:u]) <= 1:
        if e == sorted_list[u-1]:
            return l
        return -1
    m = sorted_list[(l+u)//2]
    print(m)
    mi = (l+u)//2
    if e == m: return mi
    if e > m:
        return binary_search(sorted_list,mi+1 , u, e)
    return binary_search(sorted_list, l, mi, e)
    
    
    
    
def read_positive_integer(text, p):
    """Read a number starting from the given position, return it and the first
    position after it in a tuple. If there is no number at the given position
    then return None.
    """
    dig = list(range(10))
    for i in range(10):
        dig[i] = str(dig[i])
    if text[p] not in dig:
        return
    for k in range(p+1,len(text)):
        if(text[k] not in dig):
            return (int(text[p:k]), k)
    return (int(text[p:]),len(text) - p)

def evaluate(x, p):
    """Evaluate the expression starting from the given position.
    Return the value and the first position after the read
    sub-expression. If the string starting at the given expression
    is not an arithmetic expression, return None.
    """
    operators = ('+','-','*')
    if not read_positive_integer(x, p) is None:
        return read_positive_integer(x, p)
    initp = -1
    lastp = -1
    for i in range(len(x) - p):
        i = i+p
        if x[i] == '(' and initp == -1:
            initp = i
        if x[i] == ')':
            lastp = i
    cxp = x[initp+1:lastp]
    print(cxp)
    #evaluate result of evaluate(cxp, 0) * or + or - evaluate(cxp, location of (*,+,-) +1)
    in_exp = 0 #if >1 we're in exp
    o = ''
    oi = 0
    for i in range(len(cxp)):
        if cxp[i] == '(': 
            in_exp += 1
        elif cxp[i] == ')':
            in_exp -= 1
        if in_exp == 0 and cxp[i] in operators:
            o = cxp[i]
            oi = i
    if o == '+':
        return (evaluate(cxp[:oi], 0)[0] + evaluate(cxp, oi + 1)[0], len(cxp) +2 +p)
    elif o == '-':
        return (evaluate(cxp[:oi], 0)[0] - evaluate(cxp, oi + 1)[0], len(cxp) +2+p)
    elif o == '*':
        return (evaluate(cxp[:oi], 0)[0] * evaluate(cxp, oi + 1)[0], len(cxp) +2+p)
            
            
        
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    