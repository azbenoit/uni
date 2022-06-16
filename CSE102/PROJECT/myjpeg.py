#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:54:36 2022

@author: alixb1908
"""
import math
import random
import time

def zeros(m,n): #create a matrix full of zeros of size mxn
    M = []
    for _ in range(m):
        r = []
        for __ in range(n):
            r.append(0)
        M.append(r)
    return M


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
    submat = zeros(math.ceil(h/b), math.ceil(w/a))

            
    
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
    mat = zeros(h,w)
        
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
            # print(v[j])
            # print(v)
            v_hat[i]+= v[j]*math.cos((math.pi/n)*(j+.5)*i)
        v_hat[i] = v_hat[i]*delta*math.sqrt(2/n)
        v_hat[i] = round(v_hat[i],2)
    
    return v_hat

def gen_C(n):
    C = []
    for i in range(n):
        r = []
        delta = 1/ math.sqrt(2)
        if i != 0:
            delta = 1
        for j in range(n):
            c = delta*math.cos((math.pi/n)*(j+.5)*i)*math.sqrt(2/n)
            r.append(c)
        C.append(r)
    return C


def IDCT(v_hat):
    n = len(v_hat)
    # Creating the C matrix:
    C = gen_C(n)
    # print(C)
    return dot_product(v_hat, C)[0]
    
 
def dot_product(V,C,cache = None, precision = 1):
    try: #If V is a 1D vector
        print(V[0][0])
    except:
        V = [V]
    if cache is None:
        cache = {}
    n = len(V[0]) #columns of V (V is mxn)
    m = len(V) #rows
    h = len(C[0])
    #C is a nXh matrix
    # initialize V_hat
    V_hat = zeros(m,h)
            
    
    #Matrix multiplication
    for i in range(m):#iterate thru the rows of the matrix
        for j in range(h):
            psum = 0
            for k in range(n):
                v = V[i][k]
                c = C[k][j]
                if (v,c) not in cache:
                    cache[(v,c)] = v*c
                psum += cache[(v,c)]
                
            V_hat[i][j] = round(psum,precision)
    return (V_hat,cache)


    # C = [[0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373], [0.4903926402016152, 0.4157348061512726, 0.27778511650980114, 0.09754516100806417, -0.0975451610080641, -0.277785116509801, -0.4157348061512727, -0.4903926402016152], [0.46193976625564337, 0.19134171618254492, -0.19134171618254486, -0.46193976625564337, -0.4619397662556434, -0.19134171618254517, 0.191341716182545, 0.46193976625564326], [0.4157348061512726, -0.0975451610080641, -0.4903926402016152, -0.2777851165098011, 0.2777851165098009, 0.4903926402016153, 0.09754516100806396, -0.4157348061512721], [0.3535533905932738, -0.35355339059327373, -0.35355339059327384, 0.3535533905932737, 0.35355339059327384, -0.35355339059327334, -0.35355339059327356, 0.3535533905932733], [0.27778511650980114, -0.4903926402016152, 0.09754516100806415, 0.41573480615127273, -0.41573480615127256, -0.09754516100806489, 0.49039264020161516, -0.27778511650980076], [0.19134171618254492, -0.4619397662556434, 0.46193976625564326, -0.19134171618254495, -0.19134171618254528, 0.4619397662556437, -0.46193976625564354, 0.19134171618254314], [0.09754516100806417, -0.2777851165098011, 0.41573480615127273, -0.4903926402016153, 0.4903926402016152, -0.415734806151272, 0.2777851165098022, -0.09754516100806254]]
    # test_v_hat = [101.82, -51.54, 0.00, -5.39, 0.00, -1.61, 0.00, -0.41]
        
def test_IDCT():
    # import random
    
    v = [
        float(random.randrange(-10**5, 10**5))
        for _ in range(random.randrange(1, 128))
        ]
    v2 = IDCT(DCT(v))
    try:
        assert (all(math.isclose(v[i], v2[i]) for i in range(len(v))))
        # print(v)
        # print(v2)
    except:
        for i in range(len(v)):
            if v[i] != v2[i]:
                print(f'{v[i]} != {v2[i]}')
            
            
def DCT2(m,n,V):
    # n = len(V[0]) #cols
    # m = len(V) #rows
    temp,cache = dot_product(V, transpose(gen_C(n)))
    return dot_product(gen_C(m), temp,cache)[0]

def transpose(C):
    n = len(C[0]) #col of C row of T
    m = len(C) #row
    T = zeros(n,m)
    for row in range(n):
        for col in range(m):
            T[row][col] = C[col][row]
    return T
          

def IDCT2(m,n,V):
    # n = len(V[0]) #cols
    # m = len(V) #rows
    temp, cache = dot_product(V, gen_C(n))
    return dot_product(transpose(gen_C(m)), temp, cache, 0)[0]


def test_IDCT2():
    
    m = random.randrange(1, 128)
    n = random.randrange(1, 128)
    A = [
        [
            float(random.randrange(-10**5, 10**5))
            for _ in range(n)
        ]
        for _ in range(m)
    ]
    # print( DCT2(m, n, A))
    A2 = IDCT2(m, n, DCT2(m, n, A))
    try:
        assert (all(
            math.isclose(A[i][j], A2[i][j])
            for i in range(m) for j in range(n)
        ))
    except:
        for i in range(m):
            for j in range(n):
                if A[i][j] != A2[i][j]:
                    print(f'{A[i][j]} != {A2[i][j]}')
        print(len(A2) == len(A))





# testmat  = [[1,2,3],[2,3,4]] #2,3
# tmat2 = [1,2] 

# print(dot_product(testmat, testmat))



def redalpha(i):
    j = (i //8)%4
    if j == 0: #first quadrant
        return (1,i%8)
    if j == 1: #2nd quadrant
        return (-1, (8-i%8))
    if j == 2:
        return (-1, i%8)
    if j == 3:
        return (1, 8-i%8)
    
def ncoeff8(i,j):
    if i == 0:
        return (1,4)
    return redalpha(i*(2*j+1))

M8 = [
    [ncoeff8(i, j) for j in range(8)]
    for i in range(8)
]


def M8_to_str(M8):
    def for1(s, i):
        return f"{'+' if s >= 0 else '-'}{i:d}"

    return "\n".join(
        " ".join(for1(s, i) for (s, i) in row)
        for row in M8
    )

# print(M8_to_str(M8))

def gen_C_bar():#pre-divided by two
    alphas = []
    for j in range(8): #pre-divided by two
        alphas.append(math.cos(j*math.pi/16)/2)
    C = []
    for i in range(8):
        row = []
        for j in range(8):
            s,ind = ncoeff8(i,j)
            row.append(s*alphas[ind]) 
        C.append(row)
    return C


def DCT_Chen_1D(v, C = None):
    v_hat = [0]
    #initialize cache
    if C is None:
        C = gen_C_bar()
        
    #computing v_0
    for j in range(8):
        v_hat[0] += v[j]
    v_hat[0] *= C[0][0]
    v_hat[0] = round(v_hat[0],2)
    
    #computing the other v_is
    for i in range(1,8):
        w = -1
        if i%2 == 0:
            w = 1
        s = 0
        for j in range(4):
            s += (v[j] + w*v[7-j])*C[i][j]
        v_hat.append(round(s,3))
    
    return v_hat


def DCT_Chen(A):
    C = gen_C_bar()
    temp = []
    for row in A:
        temp.append(DCT_Chen_1D(row,C))
    temp = transpose(temp) #Can probably improve efficiency by finding a way not to transpose
    res = []
    for row in temp:
        res.append(DCT_Chen_1D(row,C))
    return transpose(res)
    
def gen_C_inv(): #maybe need to generate transpose directly so it's easier to compute
    alphas = []
    for j in range(8): #pre-divided by two
        alphas.append(math.cos(j*math.pi/16)/2)
        
    C = gen_C_bar()
    C_inv = []
    for i in range(4):
        C_inv.append(C[2*i])
    for i in range(4):
        C_inv.append(C[2*i+1])
    for i in range(8):
        for j in range(4,8):
            if i == 1 or i == 3:
                C_inv[i][j] = -1*C_inv[i][j]
            if i>=4:
                C_inv[i][j] = -1*C_inv[i][j-4]
    
    return C_inv
    

def IDCT_Chen_1D(v, C_inv = None, cache = None):
    #initialize cache
    if C_inv is None:
        C_inv = gen_C_inv()
    if cache is None:
        cache = {}
    #reorder v_hat
    v_hat = []
    for i in range(4):
        v_hat.append(v[2*i])
    for i in range(4):
        v_hat.append(v[1+2*i])        
    v = dot_product(v_hat, C_inv, cache)[0][0]
    new_v = v[:4]
    for i in range(4,8):
        new_v.append(v[11-i])
    return (new_v,cache)

def IDCT_Chen(A):#need to add Cache input, Make dot-product return cache
    C = gen_C_inv()
    temp = []
    cache = {}
    for row in A:
        chen,cache = IDCT_Chen_1D(row,C,cache)
        temp.append(chen)
    temp = transpose(temp) #Can probably improve efficiency by finding a way not to transpose
    res = []
    for row in temp:
        chen,cache = IDCT_Chen_1D(row,C,cache)
        res.append(chen)
    return transpose(res) 

test_A = [
  [ 140,  144,  147,  140,  140,  155,  179,  175],
  [ 144,  152,  140,  147,  140,  148,  167,  179],
  [ 152,  155,  136,  167,  163,  162,  152,  172],
  [ 168,  145,  156,  160,  152,  155,  136,  160],
  [ 162,  148,  156,  148,  140,  136,  147,  162],
  [ 147,  167,  140,  155,  155,  140,  136,  162],
  [ 136,  156,  123,  167,  162,  144,  140,  147],
  [ 148,  155,  136,  155,  152,  147,  147,  136],
]


#function timer
def time_it(f,rep, *args, **kwargs):
    tot = []
    for _ in range(rep): 
        t = time.time()
        f(*args,**kwargs)
        tot.append((time.time()-t)*1000)
    # return f'[f] took {(time.time()-t)*1000} milliseconds'  
    return sum(tot)/rep

def quantization(A,Q):
    for i in range(8):
        for j in range(8):
            A[i][j] = round(A[i][j]/Q[i][j])
    return A

def quantizationI(A,Q):
    for i in range(8):
        for j in range(8):
            A[i][j] = A[i][j]*Q[i][j]
    return A




def Qmatrix(isY, phi):
    S = round(5000/phi)
    if phi >= 50:
        S = 200 - 2*phi
    
    
    LQM = [
      [16, 11, 10, 16,  24,  40,  51,  61],
      [12, 12, 14, 19,  26,  58,  60,  55],
      [14, 13, 16, 24,  40,  57,  69,  56],
      [14, 17, 22, 29,  51,  87,  80,  62],
      [18, 22, 37, 56,  68, 109, 103,  77],
      [24, 35, 55, 64,  81, 104, 113,  92],
      [49, 64, 78, 87, 103, 121, 120, 101],
      [72, 92, 95, 98, 112, 100, 103,  99],
    ]
    
    CQM = [
      [17, 18, 24, 47, 99, 99, 99, 99],
      [18, 21, 26, 66, 99, 99, 99, 99],
      [24, 26, 56, 99, 99, 99, 99, 99],
      [47, 66, 99, 99, 99, 99, 99, 99],
      [99, 99, 99, 99, 99, 99, 99, 99],
      [99, 99, 99, 99, 99, 99, 99, 99],
      [99, 99, 99, 99, 99, 99, 99, 99],
      [99, 99, 99, 99, 99, 99, 99, 99],
    ]
    
    if isY:
        for i in range(8):
            for j in range(8):
                LQM[i][j] = math.ceil((50+S*LQM[i][j])/100)
        return LQM
    else:
        for i in range(8):
            for j in range(8):
                CQM[i][j] = math.ceil((50+S*CQM[i][j])/100)
        return CQM
    
def zigzag(A):
    row = 0
    col = 0
    forwards = True
    down = True 
    h = len(A)
    w = len(A[0])
    while True:
        yield A[row][col]
        if row == h-1 and col == w-1:
            break
        if row == 0:
            if forwards:
                col+=1
                forwards = False
                down = True
            else:
                row+=1
                col-=1
                forwards = True
        elif col == 0 and row != h-1:
            if down:
                row += 1
                down = False
            else:
                row -= 1
                col += 1
        elif row == h - 1:
            if forwards:
                col+=1
                forwards = False
            else:
                row-=1
                col+=1
                forwards = True
        elif col == w - 1:
            if not down:
                down = True
                row += 1
            else:
                row+=1
                col-=1
        else:
            if down:
                row +=1
                col -=1
            else:
                row -=1
                col +=1
                
   

def test_zigzag():
     TA = [[(j,i) for i in range(8)] for j in range(8)] 
     repr(TA)
     g = zigzag(TA)
     for _ in range(8*8):
         print(next(g))

def rle0(g):
    while True:
        count = 0
        num = next(g)
        while num == 0:
            count+=1
            num = next(g)
        yield (count, num)
    
                   
                
                
        
            
         
        
    





























