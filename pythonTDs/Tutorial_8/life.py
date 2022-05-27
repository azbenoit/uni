#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 10:26:33 2021

@author: alixb1908
"""

class Point:
    """Encodes a live point in the Game of Life.
    Data attributes:
    x -- x-coordinate
    y -- y-coordinate
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
    
    def __eq__(self, p):
        return (self.x == p.x) and (self.y == p.y)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def get_neighbors(self):
        """Return the neighbors of the Point as a set."""
        neighbors = set({})
        for i in range(3):
            for j in range(3):
                neighbors.add(Point(self.x-1+i, self.y-1+j))
        neighbors.remove(self)
        return neighbors
    
class Board:
    """A board to play the Game of Life on.
    Data attributes:
    points -- a set of Points
    x_size  -- size in x-direction
    y_size  -- size in y-direction
    """

    def __init__(self, x_size, y_size, points):
        self.points = points
        self.x_size = x_size
        self.y_size = y_size
        
    def is_legal(self, point):
        """Check if a given Point is on the board."""
        if(point.x < 0 or point.y < 0):
            return False
        elif(point.x >= self.x_size or point.y >= self.y_size):
            return False
        else: return True
        
    def number_live_neighbors(self, p):
        """Compute the number of live neighbors of p on the Board."""
        nei = p.get_neighbors()
        return len(nei.intersection(self.points))
    
    def next_step(self):
        """Compute the points alive in the next round and update the
        points of the Board.
        """
        np = set()
        neighbors = set()
        for p in self.points:
            if(1 < self.number_live_neighbors(p) < 4):
                np.add(p)
            neighbors.update(p.get_neighbors())
        neighbors -= neighbors.intersection(self.points)#only dead neighboors
        print(np)
        for d in neighbors:
            if(self.is_legal(d) and self.number_live_neighbors(d) == 3):
                np.add(d)
        print(np)
        self.points = np
        
    def load_from_file(self, filename):
        """Load a board configuration from file in the following format:
        - The first two lines contain a number representing the size in
            x- and y-coordinates, respectively.
        - Each of the following lines gives the coordinates of a single
            point, with the two coordinate values separated by a comma.
            Those are the points that are alive on the board.
        """
        sx = 0
        sy = 0
        points = set()
        with open(filename, 'r') as file:
            f = []
            for line in file:
                f.append(line)
            sx = int(f[0].strip('\n'))
            sy = int(f[1].strip('\n'))
            print(f)
            for line in f[2:]:
                points.add(Point(int(line[0]),int(line[2])))
        #Board(sx,sy,points)
        self.points = points
        self.x_size = sx
        self.y_size = sy
        
    def toggle_point(self, x, y):
        """Add Point(x,y) if it is not in points, otherwise delete it
        from points.
        """
        p = Point(x,y)
        if p in self.points:
            self.points.remove(p)
        else:
            self.points.add(p)
    
def is_periodic(board):
    """
    Return (True, 0) if the input board is periodic, otherwise (False, i),
    where i is the smallest index of the state to which it loops
    """
    init_p = board.points
    ps = []
    i = -1
    while(board.points not in ps):
        ps.append(board.points)
        board.next_step()
        if(board.points == init_p):
            return (True,0)
        else:
            i+=1
    return (False, i)
            
        
                
                
            
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        