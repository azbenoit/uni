#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:36:14 2022

@author: alixb1908
"""
import numpy as np

def display_image(m, n, data):
    import tkinter as tk
    from PIL import Image, ImageTk

    imraw  = Image.new('1', (m, n))
    imraw.putdata([
        255 if data[i][j] else 0
        for j in range(n) for i in range(m)])

    root   = tk.Tk()
    image  = ImageTk.PhotoImage(image = imraw)
    canvas = tk.Canvas(root,width=300,height=300)

    canvas.pack()
    canvas.create_image(m, n, anchor="nw", image=image)

    root.mainloop()

n,img = (2, [[0, 0, 1, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])

#Expected qtree: ('c', 
#                   (('u', 0), ('c', (('u', 1), ('u', 0), ('u', 0), ('u', 0))), ('c', (('u', 1), ('u', 0), ('u', 0), ('u', 0))), ('u', 0)))


def image_to_qtree(n, img):
    #Check whether uniform
    #create four split matrices nw,ne,sw,se
    #Recursively call function
    #Return representation of quarter
    if n == 0:
        return ('u', img[0][0])
    init = img[0][0]
    flag = True
    for row in img:
        for pix in row:
            if pix != init:
                flag = False
                break
        if not flag:
            break
    #if uniform
    if flag:
        return ('u',init)
    #check pointers
    #Create sub-matrices
    nw,ne,sw,se = [],[],[],[]
    for _ in range(2**(n-1)):
        nw.append([])
        ne.append([])
        sw.append([])
        se.append([])
    
    
    
    for row in range(2**n):
        for col in range(2**n):
            if row < 2**(n-1): #North
                if col < 2 **(n-1): #West
                    nw[row].append(img[row][col])
                else: #East
                    ne[row].append(img[row][col])
            else: #South
                if col < 2 **(n-1): #West
                    sw[row-2**(n-1)].append(img[row][col])
                else: #East
                    se[row-2**(n-1)].append(img[row][col])
    
    
    return ('c',( image_to_qtree(n-1, nw), image_to_qtree(n-1, ne), image_to_qtree(n-1, sw), image_to_qtree(n-1, se)))


def qtree_to_image(n, node):
    if node[0] == 'u':
        return np.full((2**n,2**n), node[1]).tolist()
    #Composite node
    nw = qtree_to_image(n-1, node[1][0])
    ne = qtree_to_image(n-1, node[1][1])
    sw = qtree_to_image(n-1, node[1][2])
    se = qtree_to_image(n-1, node[1][3])
    
    img = np.zeros((2**n,2**n)).tolist()
    for row in range(2**n):
        for col in range(2**n):
            if row < 2**(n-1): #North
                if col < 2 **(n-1): #West
                    img[row][col] = nw[row][col]
                else: #East
                    img[row][col] = ne[row][col-2**(n-1)]
            else: #South
                if col < 2 **(n-1): #West
                    img[row][col] = sw[row-2**(n-1)][col]
                else: #East
                    img[row][col] = se[row-2**(n-1)][col-2**(n-1)]
    return img 
    
def qtree_to_bits(node):
    if node[0] == 'u':
        return '0'+ str(node[1])
    return '1' + qtree_to_bits(node[1][0]) + qtree_to_bits(node[1][1]) + qtree_to_bits(node[1][2]) + qtree_to_bits(node[1][3])

def bits_to_qtree(node):
    if node[0] == '0' and len(node) == 2:
        return ('u', int(node[1]))
    if (node[0] == '1'):
        res = cards(node[1:])
        if res is None:
            return
        if res[1] + 1 == len(node):
            return ('c', cards(node[1:])[0])
    return
                
            
def cards(sub):#helper recursive method for combined trees
    #return: (subtree, last_bit)
    count = 0
    i = 0
    tree = [0,0,0,0]
    while count < 4:
        if i >= len(sub):
            return
        if sub[i] == '0':
            tree[count] = ('u', int(sub[i+1]))
            i+=2
            count += 1
        else:
            res = cards(sub[(i+1):])
            if res is None:
                return
            tree[count] = ('c', res[0])
            count += 1
            i += res[1] +1
    return (tuple(tree), i)
            
        
def inverse(img):
    if img[0] == 'u':
        return ('u', (img[1]-1) * -1)
    else:
        res = []
        for i in range(4):
            res.append(inverse(img[1][i]))
        return ('c', tuple(res))
    
def rotate(img):
    if img[0] == 'u':
        return img
    else:
        res = [0,0,0,0]
        repr(img)
        res[0] = rotate(img[1][2])
        res[1] = rotate(img[1][0])
        res[2] = rotate(img[1][3])
        res[3] = rotate(img[1][1])
        return ('c', tuple(res))
        
def zoom(img):
    return img
    

def fractal(n):
    # if n == 0:
    #     return ('u', 0)
    frac = ('u', 0)
    for _ in range(n):
        frac = next_fractal(frac)
    return frac


node = ('u', 1)
def next_fractal(node):
    nw = ('c', (node,node,node,('u', 1)))
    ne = ('c', (node,node,('u', 1),node))
    sw = ('c', (node,('u', 1),node,node))
    se = ('c', (('u', 1), node,node,node))
    return ('c',( nw,ne,sw,se))
    
    
    
    
    
    # z = [0,0,0,0]
    # for i in range(4):
    #     if img[1][i][0] == 'u':
    #         z[i] = ('u', img[1][i])
    #     else:
    #         f = (i%2)*((i+1)%4) + ((i+1)%4)*((i+3)%4)
    #         z[i] = ('u', img[1][i][1][f])
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    