#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:47:05 2022

@author: alixb1908
"""
import math

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        
def size(root):
    s = 0
    if not root is None:
        s+= 1
        if not root.right is None:
            s+= size(root.right) 
            # print(root.right)
        if not root.left is None:
            s+= size(root.left) 
            # pass
    return s

T1 = Node(0, Node(1, Node(2), Node(3)), Node(4, Node(5)))
T2 = Node(0, Node(1), Node(2, Node(3), Node(4, Node(5))))
T3 = Node(11, Node(10, Node(9, None, Node(8)), Node(7)), Node(6))

def sum_values(root):
    s = 0
    if not root is None:
        s+= root.value
        if not root.right is None:
            s+= sum_values(root.right) 
            # print(root.right)
        if not root.left is None:
            s+= sum_values(root.left) 
            # pass
    return s
    
def height(root):
    if root is None:
        return -1
    return max(height(root.left),height(root.right)) + 1


def mirrored(lr, rr):
    if lr is None and rr is None:
        return True
    if not (lr is None or rr is None):
        return lr.value == rr.value and mirrored(lr.left,rr.right) and mirrored(lr.right,rr.left)
    return False

def check_symmetry(root):
    if root is None:
        return True
    if root.left is None and root.right is None:
        return True
    if not (root.left is None or root.right is None):
        return mirrored(root.left, root.right)
    return False

def check_BST(root, minv = None, maxv = None):
    if root is None:
        return True
    if maxv is None and minv is None:
        maxv,minv = math.inf, -math.inf
    if not root.left is None:
        if not ( minv <= root.left.value <= root.value and check_BST(root.left, minv, root.value)):
            return False
    if not root.right is None:
        if not( root.value <= root.right.value <= maxv and check_BST(root.right, root.value, maxv)):
            print(root.right.value)
            print(f'min:{minv} max:{maxv}')
            return False
    return True
    
def min_BST(root):
    if root is None:
        return math.inf
    if root.left is None:
        return root.value
    else:
        return min_BST(root.left)































