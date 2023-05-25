#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:22:36 2022

@author: alixb1908
"""
import random

def is_prime(n, k = 32):
    if n <= 3:
        return n > 1
    d = n-1
    r = 0
    while d % 2 == 0:
        print(d)
        d //= 2
        r += 1
    for _ in range(k):
        a = int(random.random()*(n-3) +2)
        # print(f'a = {a}')
        x = pow(a, d,n)
        # print(x)
        if not (x==1 or x==n-1):
            if r <= 1:
                return False
            for j in range(r):
                # print('test')
                x = pow(x,2,n)
                # print(x)
                if x == 1:
                    return False
                if x == n-1:
                    break
                if j == r-1:
                    return False
    return True
            
def genprime(l):
    n = 1
    for i in range (1,l-1):
        n += pow(2,i) * random.choice([0,1])
    n += pow(2,l-1)
    i = 0
    while True:
        if is_prime(n + 2*i):
            return n+2*i
        i+=1
        
def egcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0

def genmod(p,q):
    r = 0
    M = p*q
    while r !=1:
        phi = (p-1)*(q-1)
        e = random.randint(2, phi - 1)
        r,u,v = egcd(e, phi)
    if u<0:
        k = 1
        while True:
            if 2 < u + k*phi < phi:
                break
            else:
                k+=1
        u += k*phi    
    return ((M,e), u)

def keygen(l):
    l //= 2
    p = genprime(l)
    q = genprime(l)
    return genmod(p,q)

def enc(m,pkey):
    M,e = pkey
    c = pow(m,e,M)
    return c

def dec(c,pkey,skey):
    M,e = pkey
    return pow(c,skey,M)

def encmsg(s,pkey):
    a = []
    for m in s:
       a.append(enc(m,pkey))
    return a 


def decmsg(a,pkey,skey):
    s = b''
    for c in a:
        b = dec(c,pkey,skey).to_bytes(1, 'big')
        s+=b
    return s

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        
        
        
        