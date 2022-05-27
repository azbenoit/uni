#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 14:10:29 2022

@author: alixb1908
"""
import math

class Fraction:
    def __init__(self, numerator = 1, denominator = 1):
        self.__numerator = numerator
        if denominator == 0:
            denominator = 1
        self.__denominator = denominator
        
    def reduce2(self):
        n = self.__numerator
        d = self.__denominator
        if d < 0:
            n *= -1
            d *= -1
        gcd = math.gcd(n, d)
        d //= gcd
        n //= gcd
        return (n,d)
        
    def reduce(self):
        (n,d) = self.reduce2()
        self.__denominator = n
        self.__numerator = d
    
    @property
    def denominator(self):
        return self.__denominator
    
    @property 
    def numerator(self):
        return self.__numerator
    
    def __repr__(self):
        return 'Fraction(%d,%d)'%(self.__numerator, self.__denominator)

    def __str__(self):
        (n,d) = self.reduce2()
        return '%r/%d'%(n,d)        
    
    def __eq__(self, o):
        (n,d) = self.reduce2()
        (n2,d2) = o.reduce2()
        return n == n2 and d2 == d
    
    def __add__(self,o):
        (n1,d1) = self.reduce2()
        (n2,d2) = o.reduce2()
        d = d1 * d2
        n = n1*d2 + n2*d1
        return Fraction(n,d)
    
    def __neg__(self):
        return Fraction(self.__numerator * -1,self.__denominator)
    
    def __sub__(self,o):
        return self + (-o)
    
    def __mul__(self,o):
        (n1,d1) = self.reduce2()
        (n2,d2) = o.reduce2()
        d = d1 * d2
        n = n1*n2
        return Fraction(n,d)
    
    def __truediv__(self,o):
        (n1,d1) = self.reduce2()
        (n2,d2) = o.reduce2()
        d = d1 * n2
        n = n1*d2
        return Fraction(n,d)
        
        
        