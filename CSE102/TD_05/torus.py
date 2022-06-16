#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:24:45 2022

@author: alixb1908
"""
import random
import math

def torus_volume_cuboid(R, r, N=100_000):
    S = sum(tl(R,r) for _ in range(N)) # Number of successes
    cube_volume = (2*(R+r))*(2*(R+r))*(2*r)
    return (S / N) * cube_volume
    
    
def tl(R,r):
    (x,y,z) = (random.random()*2*(R+r)-R-r,random.random()*2*(R+r)-R-r, random.random()*2*r-r)
    return (math.sqrt(x**2+y**2) - R)**2 + z**2 <= r**2