#!/usr/bin/env python3
# -*- coding: utf-8 -*-

                   
#  ⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⣈⠬⠄⠀⠠⢠⣮⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⢀⠄⠂⠁⠀⠀⠀⢠⣶⡌⠻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⢰⡁⠀⡠⠂⠀⠀⠀⠀⠉⡁⠀⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠘⠀⡄⠀⠀⠀⠀⢢⡀⠀⠐⠀⠢⡈⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠣⠰⢀⠀⠠⠐⠁⠁⠀⠑⠀⠀⠠⠀⠈⢐⠠⣀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠙⠀⡄⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⢈⠀⡑⡄⠀⠀
# ⠀⠀⠀⠀⠀⡇⠀⠀⠀⠴⠀⠀⢠⠔⠂⠀⠢⡀⢁⠈⠊⠄⠀
# ⠀⠀⠀⠀⠀⢁⢠⠀⠀⢀⠀⢠⠁⠀⠀⠀⡀⠈⠀⠡⠠⠘⡀
# ⠀⠀⠀⠀⠀⠘⡀⠀⡆⠸⠀⢘⡀⠈⠀⠀⠒⠀⢱⠀⠀⡀⡇
# ⠀⠀⠀⠀⠀⠀⢸⣄⣵⠀⠀⡄⠑⡀⠀⠀⠀⠀⠀⠀⠃⢡⠁
# ⠀⠀⠀⠀⠀⠘⠛⠧⢋⣷⢴⠃⠲⢨⣕⣠⠤⠄⢀⠀⠤⠁⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠘⠺⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               
             

"""
Created on Thu May 19 12:54:36 2022

@author: alixb1908
"""
import math
import random
import time

def zeros(m,n): #create a matrix full of zeros of size mxn
    """Creates an m by n matrix full of zeros"""
    M = []
    for _ in range(m):
        r = []
        for __ in range(n):
            r.append(0)
        M.append(r)
    return M


def ppm_tokenize(stream):
    """takes an input stream 
    returns an iterator for all the tokens of stream, ignoring the comments"""
    is_word = False #Flag checking whether the current character is part of a word
    word = '' #current word
    for line in stream:
        for char in line:
            if char == '#': #ignore comments
                break
            elif char != ' ': #start of word
                is_word = True
                word+=char
            elif char == ' ' and is_word: #end of word
                is_word = False
                yield word
                word = ''
                
      
        
def ppm_load(stream):
    """Takes an input stream and that loads the PPM image,
    returning the resulting image as a 3-element tuple (w, h, img)
    where w is the image’s width, 
    h is the image’s height 
    img is a 2D-array that contains the image’s pixels’ color information"""
    
    g = ppm_tokenize(stream) #Tokenize input stream
    img_type = next(g) #get first four initialization values (even if two aren't used)
    w = int(next(g))
    h = int(next(g))
    max_val = int(next(g))
    i = 0 # counter variable that tracks number of values in current pixel list
    r = 0 # counter that tracks number of pixels in current row
    img = [] #full image
    img_row = [] #current image row
    pixel = [] #current pixel
    for token in g:
        token = int(token)
        if i == 3:#if pixel full
            i = 0
            if r == w: #if row full
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
    return (w,h,img)

        

    
def ppm_save(w, h, img, output):
    """takes an output stream output 
    and saves the PPM image img whose size is w x h."""
    output.write(f'P3\n{w} {h}\n255\n')
    for row in img:
        for pixel in row:
            output.write(f'{pixel[0]} {pixel[1]} {pixel[2]}\n')

#test
# with open('file2.ppm', 'w') as stream:
#     ppm_save(3,2,[[(255, 0, 0), (0, 255, 0), (0, 0, 255)], [(255, 255, 0), (255, 255, 255), [0, 0, 0]]], stream)



def RGB2YCbCr(r, g, b):
    """Takes a pixel’s color in the RGB color space 
    and converts it in the YCbCr color space.
    Returns the 3-element tuple (Y, Cb, Cr)"""
    
    #Applying the given formulas
    Y = round(.299*r + .587*g + .114*b)
    Cb = round(128 - 0.168736*r -0.331264*g + .5*b)
    Cr = round(128 + .5*r -0.418688*g -0.081312*b)
    #Normalizing the values if rounding errors make them overflow
    if Y > 255: Y = 255
    if Cb > 255: Cb = 255
    if Cr > 255: Cr = 255
    if Y < 0: Y = 0
    if Cb < 0: Cb = 0
    if Cr < 0: Cr = 0
    return (Y,Cb,Cr)
    
def YCbCr2RGB(Y, Cb, Cr):
    """
    Takes a point in the YCbCr 
    converts it in the RGB color space
    returns the 3-element tuple (R, G, B)"""
    #Applying given formulas
    R = round(Y + 1.402*(Cr-128))
    G = round(Y - 0.344136*(Cb-128) - 0.714136 * (Cr-128))
    B = round(Y + 1.772 * (Cb - 128))
    #Normalizing values
    if R > 255: R = 255
    if G > 255: G = 255
    if B > 255: B = 255
    if R < 0: R = 0
    if G < 0: G = 0
    if B < 0: B = 0
    return (R,G,B)

def img_RGB2YCbCr(img):
    """
    Takes an image in the RGB-color space 
    returns a 3-element tuple (Y, Cb, Cr) 
    where Y (resp. Cb, Cr) is a matrix s.t. 
    Y[i][j] (resp. Cb[i][j], Cr[i][j]) denotes the Y (resp. Cb, Cr) component of img[i][j].
    """
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
    """
    Performs the inverse transformation to img_RGB2YCbCr(img)
    using RGB2YCbCr function.
    """
    img = []
    for row in range(len(Y)):
        img_row = []
        for col in range(len(Y[row])):
            img_row.append(YCbCr2RGB(Y[row][col], Cb[row][col], Cr[row][col]))
        img.append(img_row)
    return img

def subsampling(w,h,C,b,a):
    """
    Performs & returns the subsampling of the channel C (of size w x h)
    in the a:b subsampling mode.
    
    NOTE: In this implementation b is height, a is width. 
    parameter order has been switched for grader to work
    """
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
    """
    Does the inverse operation of subsampling, 
    where w & h denotes the size of the channel 
    before the subsampling has been applied.
    """
    #initialize new matrix
    mat = zeros(h,w)
        
    #filling new matrix
    for i in range(len(C)):#Iterate through rows of shrunken matrix C (corresponds to each block row-wise)
        for j in range(len(C[i])):#Iterate through columns of C
            for row in range(b*i, min(b*(i+1), h)):#corresponds to row location of new matrix, of height h
            #For edge case takes min to avoid index out of bound errors
                for col in range(a*j, min(a*(j+1), w)):
                    mat[row][col] = C[i][j]
    
    return mat
                    

#modified to take in arbitray block sizes
def block_splitting(w, h, C, a = 8, b =8):
    """
    Takes a channel C 
    and yields all the 8 x 8 subblocks of the channel,
    line by line, from left to right.
    """
    for i in range(math.ceil(h/(b))): #num of vertical blocks
        for j in range(math.ceil(w/(a))): #num of horizontal blocks
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
                    elif col >=w and row < h: #partially empty rows
                        mat[row-b*i][col-a*j] = mat[row-b*i][col-a*j-1]
                    else: #fully empty rows
                        mat[row-b*i][col-a*j] = mat[row-b*i-1][col-a*j]
                        
            yield mat
                

def DCT(v):
    """
    Computes and returns the DCT-II of the vector v. 
    The input vector v is given as a non-empty Python list of numbers 
    (integers and/or floating point numbers)
    This function returns 
    a list of floating point numbers that contains the DCT-II coefficients.
    """
    n = len(v)
    v_hat = [0]*n
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
    """Generates the C, n by n matrix for DCT"""
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
    """
    Computes the inverse DCT-II of the vector v. 
    The input vector v is given as a non-empty Python list of numbers 
    the function returns
    a list of floating point numbers that contains the inverse DCT-II coefficients.
    """
    n = len(v_hat)
    # Creating the C matrix:
    C = gen_C(n)
    # print(C)
    return dot_product(v_hat, C)[0]
    
 
def dot_product(V,C):
    """Computes the dot product 
    between two compatible vectors or matrices"""
    try: #If V is a 1D vector
        print(V[0][0])
    except:
        V = [V]
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
                psum += v*c
                
            V_hat[i][j] = psum
    return V_hat


  
def test_IDCT():
    """Tests IDCT function"""
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
    """
    Computes the 2D DCT-II of the matrix A. 
    The input matrix A contains numbers only 
    and is made of m rows and n columns.
    This function returns
    a matrix of floating point numbers that contain the 2D DCT-II coefficients.
    """
    # n = len(V[0]) #cols
    # m = len(V) #rows
    temp = dot_product(V, transpose(gen_C(n)))
    return dot_product(gen_C(m), temp)

def transpose(C):
    """Computes the transpose of a given matrix C"""
    n = len(C[0]) #col of C row of T
    m = len(C) #row
    T = zeros(n,m)
    for row in range(n):
        for col in range(m):
            T[row][col] = C[col][row]
    return T
          

def IDCT2(m,n,V):
    """
    Computes the 2D inverse DCT-II of the matrix A. 
    The input matrix A contains numbers only 
    and is made of m rows and n columns. 
    This function returns 
    a matrix of floating point numbers that contain the 2D inverse DCT-II coefficients."""
    # n = len(V[0]) #cols
    # m = len(V) #rows
    temp = dot_product(V, gen_C(n))
    return dot_product(transpose(gen_C(m)), temp)


def test_IDCT2():
    """Tests IDCT2 function"""
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


def redalpha(i):
    """
    Takes a non-negative integer i 
    returns a pair (s, k) s.t.
    s is an integer in the set {−1,1},
    k is an integer in the range {0,..,8}, and
    alphai = s x alphak.
    """
    j = (i //8)%4
    if j == 0: #first quadrant
        return (1,i%8)
    if j == 1: #2nd quadrant
        return (-1, (8-i%8))
    if j == 2: #3rd quadrant
        return (-1, i%8)
    if j == 3:
        return (1, 8-i%8)
    
def ncoeff8(i,j):
    """
    Returns C matrix alpha sign s and subscript k from [1,8]
    """
    if i == 0:
        return (1,4)
    return redalpha(i*(2*j+1))

M8 = [
    [ncoeff8(i, j) for j in range(8)]
    for i in range(8)
]


def M8_to_str(M8):
    """Turns ncoeff C matrix into string """
    def for1(s, i):
        return f"{'+' if s >= 0 else '-'}{i:d}"

    return "\n".join(
        " ".join(for1(s, i) for (s, i) in row)
        for row in M8
    )

# print(M8_to_str(M8))

def gen_C_bar():#pre-divided by two
    """
    Generates the C^bar matrix M8 described 
    
    """
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

C_bar = gen_C_bar()
# print(C_bar)




#Must have 22 multiplications max
def DCT_Chen_1D(v):
    """
    1D DCT of vector v optimized with Chen Algorithm 
    """
    v_hat = [0 for _ in range(8)]
    
    #computing v_0 (1 multiplication)
    for j in range(8):
        v_hat[0] += v[j]
    v_hat[0] *= C_bar[0][0]
    # v_hat[0] = round(v_hat[0],2)
    
    # print(v_hat)
    #computing v_2 (2 multiplications)
    v_hat[2] = (v[0] + v[7] - v[3] - v[4])*C_bar[2][0] + (v[1]-v[2]-v[5]+v[6])*C_bar[2][1]
    
    #computing v_4 (1 multiplication)
    v_hat[4] = (v[0] - v[1] - v[2] + v[3] + v[4] - v[5] - v[6] + v[7])*C_bar[4][0] 
    
    #computing v_6 (2 multiplication)
    v_hat[6] = (v[0] + v[7] - v[3] - v[4])*C_bar[6][0] + (v[1]-v[2]-v[5]+v[6])*C_bar[6][1]

    
    #computing the other v_is (4*4 = 16 multiplications)
    for i in range(1,8,2): 
        w = -1
        if i%2 == 0:
            w = 1
        s = 0
        for j in range(4):
            s += (v[j] + w*v[7-j])*C_bar[i][j]
        v_hat[i] = s
    
    #(1+1+2+2+16) = 22 total multiplications
    return v_hat

#Must have a max of 352 multiplications
def DCT_Chen(A):
    """
    Takes an 8 x 8 matrix A of numbers
    returns the 2D DCT-II transform of A, 
    using Chen Algorithm
    """
    temp = []
    for row in A: #(8*22 = 176 multiplications)
        temp.append(DCT_Chen_1D(row))
    temp = transpose(temp) #Can probably improve efficiency by finding a way not to transpose
    res = []
    for row in temp: #(8*22 = 176 multiplications)
        res.append(DCT_Chen_1D(row))
    #352 multiplications
    return transpose(res)
    



a = [(math.cos(j*math.pi/16)/2) for j in range(9)] #alpha vector
# a = alphas #shorten name to make typing easier
Theta = [[a[1],a[3],a[5],a[7]],
         [a[3],-a[7],-a[1],-a[5]],
         [a[5],-a[1],a[7],a[3]],
         [a[7],-a[5],a[3],-a[1]]]
Omega = [[a[4]]*4,
         [a[2],a[6],-a[6],-a[2]],
         [a[4], -a[4], -a[4], a[4]],
         [a[6],-a[2],a[2],-a[6]]
         ]

def IDCT_Chen_1D(v_hat): #from v_hat --> v_0
    """
    1D inverse DCT using Chen algorithm
    """
    #Create v
    v = [0 for _ in range(8)]
    
    #reorder v_hat
    v_hat = [v_hat[0],v_hat[2],v_hat[4],v_hat[6],v_hat[1],v_hat[3],v_hat[5],v_hat[7]]
    
    #Creating a cache
    c = {(0,4):v_hat[0]*a[4], (1,2): v_hat[0]*a[2]}
    for tup in [(0,4),(1,2),(1,6),(2,4),(3,6),(3,2)]:
        c[tup] = v_hat[tup[0]] * a[tup[1]] #6 multiplications
    
    #multiplying first half of v_hat by Omega (hard-coded for optimization)
    vOmega = [c[(0,4)]+c[(1,2)]+c[(2,4)]+c[(3,6)],
              c[(0,4)]+c[(1,6)]-c[(2,4)]-c[(3,2)],
              c[(0,4)]-c[(1,6)]-c[(2,4)]+c[(3,2)],
              c[(0,4)]-c[(1,2)]+c[(2,4)]-c[(3,6)],              
                ]
    
    
    #multiplying the second half of v_hat by Theta
    vTheta = dot_product(v_hat[4:], Theta)[0]
    
    
    #adding everything together
    for i in range(4):
        v[i] = vTheta[i] + vOmega[i]
        v[i+4] = -vTheta[i] + vOmega[i]
    
    #final reorder of v
    new_v = v[:4] + [v[7],v[6],v[5],v[4]]
    
    return new_v
    
    


def IDCT_Chen(A): # if had 
    """
    Takes an 8x8 matrix A of numbers 
    returns the 2D DCT-II inverse transform of A,
    using Chen Algorithm"""
    temp = []
    for row in A:
        chen = IDCT_Chen_1D(row)
        temp.append(chen)
    temp = transpose(temp) #Can probably improve efficiency by finding a way not to transpose
    res = []
    for row in temp:
        chen = IDCT_Chen_1D(row)
        res.append(chen)
    return transpose(res) 


def test_Chen(A):
    """Function to test DCT and IDCT Chen"""
    B = DCT_Chen(A)
    B2 = [
  [1210.000,  -17.997,   14.779,   -8.980,   23.250,   -9.233,  -13.969,  -18.937],
  [  20.538,  -34.093,   26.330,   -9.039,  -10.933,   10.731,   13.772,    6.955],
  [ -10.384,  -23.514,   -1.854,    6.040,  -18.075,    3.197,  -20.417,   -0.826],
  [  -8.105,   -5.041,   14.332,  -14.613,   -8.218,   -2.732,   -3.085,    8.429],
  [  -3.250,    9.501,    7.885,    1.317,  -11.000,   17.904,   18.382,   15.241],
  [   3.856,   -2.215,  -18.167,    8.500,    8.269,   -3.608,    0.869,   -6.863],
  [   8.901,    0.633,   -2.917,    3.641,   -1.172,   -7.422,   -1.146,   -1.925],
  [   0.049,   -7.813,   -2.425,    1.590,    1.199,    4.247,   -6.417,    0.315],
] #Actual DCT of A
    C = IDCT_Chen(B)
    count = 0
    #Test only DCT
    for i in range(8):
        for j in range(8):
            if abs(B[i][j] -B2[i][j]) > .01:
                # print(B[i][j]," ", B2[i][j])
                print("Difference is: ", abs(B[i][j] -B2[i][j]))
    
    #Test both IDCT and DCT
    for i in range(8):
        for j in range(8):
            if abs(C[i][j] -A[i][j]) > .01:
                # print(C[i][j]," ", A[i][j])
                print("Difference is: ", abs(C[i][j] -A[i][j]))
                count+=1
    
    
    #Test IDCT only
    # C2 = IDCT_Chen(B2) #actual inverse, should equal A
    # for i in range(8):
    #     for j in range(8):
    #         if abs(A[i][j] -C2[i][j]) > .01:
    #             # print(A[i][j]," ", C2[i][j], "Difference is: ", abs(A[i][j] -C2[i][j]))
    #             print("Difference is: ", abs(A[i][j] -C2[i][j]))
    return "Done: " + str(count)
    
    
    

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
    """Times a given function averaged over {rep} times"""
    tot = []
    for _ in range(rep): 
        t = time.time()
        f(*args,**kwargs)
        tot.append((time.time()-t)*1000)
    # return f'[f] took {(time.time()-t)*1000} milliseconds'  
    return sum(tot)/rep

def quantization(A,Q):
    """
    Takes two 8 x 8 matrices of numbers 
    returns the quantization of A by Q.
    The returned matrix is an 8x8 matrix of integers.
    """
    for i in range(8):
        for j in range(8):
            A[i][j] = round(A[i][j]/Q[i][j])
    return A

def quantizationI(A,Q):
    """
    Takes two 8 x 8 matrices of numbers 
    returns the inverse quantization of A by Q.
    The returned matrix is an 8 x 8 matrix of numbers.
    """
    for i in range(8):
        for j in range(8):
            A[i][j] = A[i][j]*Q[i][j]
    return A




def Qmatrix(isY, phi):
    """
    Takes a boolean isY and a quality factor phi.
      If isY is True, it returns the standard JPEG quantization matrix for the luminance channel,
      lifted by the quality factor phi.
      If isY is False, it returns the standard JPEG quantization matrix for the chrominance channel,
      lifted by the quality factor phi.
    """
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
    """
    Takes a 8 x 8 row-major matrix 
    returns a generator that yields all the
    values of A, following the zig-zag ordering.
    """
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
                down = False
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
    """helper to test zigzag"""
    TA = [[(j,i) for i in range(8)] for j in range(8)] 
    repr(TA)
    g = zigzag(TA)
    for _ in range(8*8):
        print(next(g))

def test_zigzag2(A):
    """Helper to test zigzag"""
    g = zigzag(A)
    l = []
    for _ in range(8*8):
         l.append(next(g))
    return l 

def rle0(g):
    """
    Takes a generator (a list) that yields integers 
    returns a generator that yields the pairs obtained from the RLE0 encoding of g.
    """
    i = 0
    while i < len(g):
        count = 0
        num = g[i]
        while num == 0 and i < len(g) - 1:
            count+=1
            i+=1
            num = g[i]
        if num != 0:
            yield (count,num)
        i+=1
       
    # while True:
    #     count = 0
    #     num = next(g)
    #     while num == 0:
    #         count+=1
    #         num = next(g)
    #     yield (count, num)
      

        
        
        
def list_from_gen(g):
    """Returns a list from a generator"""
    l = []
    for i in g:
         l.append(i)
    return l 

# Thank you for this semester!!!
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣶⣶⣆⠀⢸⣏⠓⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⢳⣿⡏⣼⣀⣸⣿⣧⣸⣇⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣼⣿⡅⠻⠿⢄⣠⠠⣄⡀⠉⠛⠿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠟⠻⣿⣿⠂⢸⡧⠤⣼⣇⠀⠀⠀⠀⠉⣿⣿⣿⣷⣶⣄⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠃⠀⠀⠉⠀⠀⠈⠙⠛⢿⡿⠀⠀⠀⠀⢠⣿⠿⠿⣿⡿⠿⡆⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⠤⠤⠶⠒⠒⠶⠶⠤⠤⠤⠖⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣼⣷⣾⣷⣿⡇⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⣀⡤⠖⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢤⣤⣄⡈⠉⢹⡏⠁⣽⠶⢴⠆
# ⠀⠀⠀⢀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠴⠶⢿⠇⢸⡇⠰⡾⠶⠶⠀
# ⠀⠀⣠⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡴⠚⠛⠀⢨⣧⣀⠟⢦⠀⠀
# ⠀⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⣠⣄⣴⣶⣶⣾⣿⠟⠉⠀⠀⠀⠀
# ⣸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⡿⢿⣿⣾⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀
# ⣿⣿⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠸⠟⠛⡽⠛⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⣿⣿⡇⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⢻⣿⣿⣿⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠀⠀⠀⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠈⣿⣿⣿⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠀⠀⠀⠀⠀⠀⠀⠀⣀⣾⠇⠀⢀⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⢹⣿⣿⣿⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⣼⣿⣇⠀⠀⠀⠀⠀⠀⣠⣴⣿⢹⣀⣾⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⢻⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣧⣾⣿⣿⡏⣸⣇⣸⣀⣶⣴⣿⡇⣹⣾⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠈⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣠⣾⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⠛⢻⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⢿⡟⠀⠀⠀⠀⣀⠀⢀⣤⣇⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⣿⠃⢀⣼⣷⣾⣷⣾⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⢿⣿⣻⡿⠋⣿⣿⣿⣿⢧⣀⠻⠿⣿⣍⣺⣿⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⢠⡧⠼⠿⣟⣻⣿⢿⣿⣿⣿⣿⣿⣻⣻⠿⢭⣿⣳⣦⣍⠀⠀⠀⠀⠛⠿⢿⣮⣛⢮⣿⡆⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠉⠙⠉⠉⠉⠉⠙⠙⠛⠓⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⢀⡀⣄⣀⣀⣀⣀⣀⣀⣀⣠⣀⣀⣀⣤⡀⠀⣀⣀⣀⣀⡀⢀⠀⣤⣠⣤⣤⢀⡤⢤⣀⣄⡤⣄⣄⢤⣄⣄⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠐⠛⠛⡛⠛⠛⢛⠛⠛⠛⡛⠛⢛⠛⠛⠓⠘⠚⠛⠛⠋⠃⠀⠀⠚⠒⠃⠚⠋⠛⠓⠛⠛⠛⠛⠚⠋⠛⡋
# (art source: https://emojicombos.com/capybara-ascii-art)⠀⠀⠀⠀⠀⠀⠀   
   
            
         
        
    





























