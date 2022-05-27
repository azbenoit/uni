#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 10:29:03 2022

@author: alix.benoit
"""

class Node:
    def __init__(self, key, value, left = None, right = None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.key == other.key \
           and self.value == other.value \
           and self.left == other.left \
           and self.right == other.right

    def __repr__(self):
        return f'Node({repr(self.key)}, {repr(self.value)}, {repr(self.left)}, {repr(self.right)})'

    def __str__(self):
        lines, _ = self._str_aux()
        return '\n'.join(lines)

    def _str_aux(self):
        # Recursive helper for __str__.
        # Returns lines (to be joined) and the horizontal position where
        # a branch from an eventual parent should be attached.
        label = f'{self.key}: {self.value}'

        # Leaf case
        if self.right is None and self.left is None:
            return [label], len(label) // 2
    
        if self.left is None:
            llines, lpos, lwidth, ltop0, ltop1, lfill = [], 0, 0, '', '', ''
        else:  # Recurse left
            llines, lpos = self.left._str_aux()
            lwidth = len(llines[0])
            ltop0 = lpos*' ' + ' ' + (lwidth - lpos - 1)*'_'
            ltop1 = lpos*' ' + '/' + (lwidth - lpos - 1)*' '
            lfill = lwidth*' '
            
        if self.right is None:
            rlines, rpos, rwidth, rtop0, rtop1, rfill = [], 0, 0, '', '', ''
        else:  # Recurse right
            rlines, rpos = self.right._str_aux()
            rwidth = len(rlines[0])
            rtop0 = rpos*'_' + ' ' + (rwidth - rpos - 1)*' '
            rtop1 = rpos*' ' + '\\' + (rwidth - rpos - 1)*' '
            rfill = rwidth*' '

        cfill = len(label)*' '
        
        # Extend llines or rlines to same length, filling with spaces (or '')
        maxlen = max(len(llines), len(rlines))
        llines.extend(lfill for _ in range(maxlen - len(llines)))
        rlines.extend(rfill for _ in range(maxlen - len(rlines)))
          
        res = []
        res.append(ltop0 + label + rtop0)
        res.append(ltop1 + cfill + rtop1)
        res.extend(lline + cfill + rline for (lline, rline) in zip(llines, rlines))
        
        return res, lwidth + len(label) // 2
    
    def add(self, k, v):
        if k < self.key:
            if self.left is None:
                self.left = Node(k,[v])
            else:
                self.left.add(k,v)
        elif k > self.key:
            if self.right is None:
                self.right = Node(k,[v])
            else:
                self.right.add(k,v)
        elif v != self.value[-1]:
            self.value.append(v)
            
    def add2(self, k, v):
        if k < self.key:
            if self.left is None:
                self.left = Node(k,v)
            else:
                self.left.add2(k,v)
        elif k > self.key:
            if self.right is None:
                self.right = Node(k,v)
            else:
                self.right.add2(k,v)
        elif v != self.value[-1]:
            self.value.append(v)
            
    def search(self, k):
        if k==self.key:
            print('==')
            print(f'value: {self.value}')
            return self.value
        elif k < self.key:
            print('<--')
            if self.left is None:
                return None
            else:
                return self.left.search(k)
        elif k > self.key:
            print('-->')
            if self.right is None:
                return None
            else:
                return self.right.search(k)
            
    def print_in_order(self):
        if not self.left is None:
            self.left.print_in_order()
        print(f'{self.key}: {self.value}')
        if not self.right is None:
            self.right.print_in_order()
            
    def write_in_order(self, filename):
        """Write all key: value pairs in the index tree
        to the named file, one entry per line.
        """
        with open(filename, 'w') as file:
            self.write_in_order_rec(file)

    def write_in_order_rec(self, file):
        """Recursive helper method for write_in_order."""
        if self.left is None:
            file.write(f'{self.key}: {self.value}\n')
            if not self.right is None:
                self.right.write_in_order_rec(file)
        else:
            self.left.write_in_order_rec(file)
            file.write(f'{self.key}: {self.value}\n')
            if not self.right is None:
                self.right.write_in_order_rec(file)
                
    def height(self, h = 0):
        if self.left is None and self.right is None:
            return h
        elif self.left is None:
            return self.right.height(h+1)
        elif self.right is None:
            return self.left.height(h+1)
        elif self.left.height(h) > self.right.height(h):
            return self.left.height(h+1)
        else:
            return self.right.height(h+1)
        
    def list_in_order(self, l = None):
        if l is None:
            l = []
        if self.left is None and self.right is None:
            l.append((self.key,self.value))
        elif self.left is None:
            l.append((self.key,self.value))
            l = self.right.list_in_order(l)
        else:
            l = self.left.list_in_order(l)
            l.append((self.key,self.value))
            if not self.right is None:
                l = self.right.list_in_order(l)
        return l
    
    
            
        

            
    
    
    
def example_bst():
    root = Node(8,'Eight')
    root.add2(4,'Four')
    root.add2(3,'Three')
    root.add2(6,'Six')
    root.add2(10,'Ten')
    root.add2(14,'Fourteen')
    root.add2(13,'Thirteen')
    root.add2(7,'Seven')
    return root
    

#ex = example_bst()

#test = Node('quick', [1], None, None)

def split_in_words_and_lowercase(line):
    """Split a line of text into a list of lower-case words."""
    parts = line.strip('\n').replace('-', ' ').replace("'", " ").replace('"', ' ').split()
    parts = [p.strip('",._;?!:()[]').lower() for p in parts]
    return [p for p in parts if p != '']

def construct_bst_for_indexing(filename):
    with open(filename, 'r') as f:
        lines = []
        for l in f:
            lines.append(split_in_words_and_lowercase(l))
        bst = Node(lines[0][0],[1])
        for l in range(len(lines)):
            for w in lines[l]:
                bst.add(w, l+1)
    return bst
                
#root = construct_bst_for_indexing('foxdog.txt')

    
def generate_index(textfile, indexfile):
    bst = construct_bst_for_indexing(textfile)
    bst.write_in_order(indexfile)
    
def balanced_bst(sorted_list):
    """Return balanced BST constructed from sorted list."""
    return balanced_bst_rec(sorted_list, 0, len(sorted_list))

def balanced_bst_rec(sorted_list, lower, upper):
    """Recursive helper function for balanced_bst."""
    if lower == upper:
        return None
    i = (upper - lower) // 2 + lower
    root = Node(sorted_list[i][0],sorted_list[i][1])
    root.left = balanced_bst_rec(sorted_list, lower, i)
    root.right = balanced_bst_rec(sorted_list, i+1, upper)
    return root
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    