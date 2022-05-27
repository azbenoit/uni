#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:54:36 2022

@author: alixb1908
"""
import math

def ppm_tokenize(stream):
    is_word = False
    word = ''
    for line in stream:
        for char in line:
            if char == '#':
                break
            elif char != ' ':
                is_word = True
                word+=char
            elif char == ' ' and is_word:
                is_word = False
                yield word
                word = ''
                

# with open('file.ppm') as stream:
# 	for token in ppm_tokenize(stream):
# 		print(token)


# with open('file.ppm') as stream:
#     g = ppm_tokenize(stream)
#     print(next(g))
#     for token in g:
#         print(token)
        
        
def ppm_load(stream):
    # tokens = []
    # for token in ppm_tokenize(stream):
    #     tokens.append(token)
    g = ppm_tokenize(stream)
    img_type = next(g)
    w = int(next(g))
    h = int(next(g))
    max_val = int(next(g))
    i = 0
    r = 0
    img = []
    img_row = []
    pixel = []
    for token in g:
        # print(pixel)
        # print(i)
        token = int(token)
        if i == 3:#pixel full
            i = 0
            if r == w: #row full
                r = 0
                img.append(img_row)
                img_row = []
            r+=1
            img_row.append(tuple(pixel))
            pixel = []
                
        pixel.append(token)
        i+=1
    img_row.append(pixel)
    img.append(img_row)
    # print(pixel)
    return (w,h,img)

        
        
# with open('file.ppm') as stream:
#     w, h, img = ppm_load(stream)
#     print(w)
#     print(h)
#     print(img)
    
def ppm_save(w, h, img, output):
    output.write(f'P3\n{w} {h}\n255\n')
    for row in img:
        for pixel in row:
            output.write(f'{pixel[0]} {pixel[1]} {pixel[2]}\n')
    


# with open('file2.ppm', 'w') as stream:
#     ppm_save(3,2,[[(255, 0, 0), (0, 255, 0), (0, 0, 255)], [(255, 255, 0), (255, 255, 255), [0, 0, 0]]], stream)

def RGB2YCbCr(r, g, b):
    Y = round(.299*r + .587*g + .114*b)
    Cb = round(128 - 0.168736*r -0.331264*g + .5*b)
    Cr = round(128 + .5*r -0.418688*g -0.081312*b)
    if Y > 255: Y = 255
    if Cb > 255: Cb = 255
    if Cr > 255: Cr = 255
    if Y < 0: Y = 0
    if Cb < 0: Cb = 0
    if Cr < 0: Cr = 0
    return (Y,Cb,Cr)
    
def YCbCr2RGB(Y, Cb, Cr):
    R = round(Y + 1.402*(Cr-128))
    G = round(Y - 0.344136*(Cb-128) - 0.714136 * (Cr-128))
    B = round(Y + 1.772 * (Cb - 128))
    if R > 255: R = 255
    if G > 255: G = 255
    if B > 255: B = 255
    if R < 0: R = 0
    if G < 0: G = 0
    if B < 0: B = 0
    return (R,G,B)

def img_RGB2YCbCr(img):
    Y = []
    Cb = []
    Cr = []
    for row in img:
        Y_row, Cb_row, Cr_row = [], [], []
        for pixel in row:
            R,G,B = pixel
            y,b,r = RGB2YCbCr(R,G,B)
            Y_row.append(y)
            Cb_row.append(b)
            Cr_row.append(r)
        Y.append(Y_row)
        Cb.append(Cb_row)
        Cr.append(Cr_row)
    return (Y,Cb,Cr)
        
def img_YCbCr2RGB(Y, Cb, Cr):
    img = []
    for row in range(len(Y)):
        img_row = []
        for col in range(len(Y[row])):
            img_row.append(YCbCr2RGB(Y[row][col], Cb[row][col], Cr[row][col]))
        img.append(img_row)
    return img

def subsampling(w,h,C,a,b):
    #initialize submatrix
    submat = []
    for i in range(math.ceil(h/b)):
        r = []
        for j in range(math.ceil(w/a)):
            r.append(0)
        submat.append(r)
            
    
    #iteratively go through C channel
    for i in range(math.ceil(h/b)):
        for j in range(math.ceil(w/a)):
            avg = 0
            n = 0
            for row in range(b*i, min(b*(i+1), h)):
                for col in range(a*j, min(a*(j+1), w)):
                    avg += C[row][col]
                    n +=1
            # print(n)
            avg //= n
            submat[i][j] = avg
    return submat
            


def extrapolate(w, h, C, a, b):
    #initialize new matrix
    mat = []
    for i in range(h):
        r = []
        for j in range(w):
            r.append(0)
        mat.append(r)
        
    #filling new matrix
    for i in range(len(C)):
        for j in range(len(C[i])):
            for row in range(b*i, min(b*(i+1), h)):
                for col in range(a*j, min(a*(j+1), w)):
                    mat[row][col] = C[i][j]
    
    return mat
                    

#modified to take in arbitray block sizes
def block_splitting(w, h, C, a = 8, b =8):
    for i in range(h//(b)+1): #num of vertical blocks
        for j in range(w//(a)+1): #num of horizontal blocks
            #init matrix to be returned
            mat = []
            for _ in range(a):
                r = []
                for __ in range(b):
                    r.append(None)
                mat.append(r)
            
            #fill new matrix
            for row in range(b*i, b*(i+1)):
                for col in range(a*j, a*(j+1)):
                    if row < h and col < w:
                        mat[row-b*i][col-a*j] = C[row][col]
                    elif col >=h and row < h: #partially empty rows
                        mat[row-b*i][col-a*j] = mat[row-b*i][col-a*j-1]
                    else: #fully empty rows
                        mat[row-b*i][col-a*j] = mat[row-b*i-1][col-a*j]
                        
            yield mat
                

def DCT(v):
    n = len(v)
    v_hat = [0]*n
    #Init:
    # M = []
    # for i in range(n):
    #     r = []
    #     for j in range(n):
    #         r.append(None)
    #     M.append(r)
    for i in range(n):
        delta = 1/ math.sqrt(2)
        if i != 0:
            delta = 1
        for j in range(n):
            v_hat[i]+= v[j]*math.cos((math.pi/n)*(j+.5)*i)
        v_hat[i]*=delta*math.sqrt(2/n)
        v_hat[i] = round(v_hat[i],2)
    
    return v_hat


def IDCT(v_hat):
    n = len(v_hat)
    v = [0]*n
    # Init:
    M = []
    for i in range(n):
        r = []
        delta = 1/ math.sqrt(2)
        if i != 0:
            delta = 1
        for j in range(n):
            c = delta*math.cos((math.pi/n)*(j+.5)*i)*math.sqrt(2/n)
            r.append(c)
        M.append(r)
    
    
    
    
    #for i in range(n):
        



        




























