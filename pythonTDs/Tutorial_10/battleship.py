import random
# List of tuples: (name, length) where length is the number of positions of your ship
ship_types = [('Battleship',4),('Carrier',5),('Cruiser',3),('Destroyer',2),('Submarine',3)]

class Ship:
    """A ship that can be placed on the grid."""

    def __repr__(self):
        return f"Ship('{self.name}', {self.positions})"

    def __str__(self):
        return f'{repr(self)} with hits {self.hits}'

    def __init__(self, name, positions):
        self.name = name
        self.positions = positions
        self.hits = set()
    
    def __eq__(self, o):
        return self.name == o.name and self.positions == o.positions and self.hits == o.hits
    
    def is_afloat(self):
        return not self.positions == self.hits
    
    def take_shot(self, shot):
        """Check if the shot hits the ship. If so, remember the hit.
        Returns one of 'MISS', 'HIT', or 'DESTROYED'.
        """
        if shot not in self.hits and shot in self.positions:
            self.hits.add(shot)
            if self.hits == self.positions:
                return 'DESTROYED'
            else:
                return 'HIT'
        else:
            return 'MISS'
        
        
                


class Grid:
    """Encodes the grid on which the Ships are placed.
    Also remembers the shots fired that missed all of the Ships.
    """
    
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.ships = []
        self.misses = set()
    
    def add_ship(self, ship):
        """Add a Ship to the grid at the end of the ships list."""
        f = True
        for p in ship.positions:
            for s in self.ships:
                if p in s.positions:
                    f = False
        if f:   
           self.ships.append(ship)
           
    def shoot(self, position):
        for s in self.ships:    
            results = s.take_shot(position)
            if results == 'HIT':
                return (results, None)
            elif results == 'DESTROYED':
                return (results, s)
        self.misses.add(position)
        return ('MISS', None)
    
    def random_ship(self):
        i = random.randint(0, 4)
        (name, pnum) = ship_types[i]
        up = random.randint(0, 1)
        x = 0
        y = 0
        if up == 0:
            x = random.randint(0, self.x_size - pnum)
            y = random.randint(0 , self.y_size)
        else:
            x = random.randint(0, self.x_size)
            y = random.randint(0 , self.y_size - pnum)
        positions = []
        side = (up +1)%2 
        for k in range(pnum):
            positions.append((x + k * side,y + k * up))
        return Ship(name, positions)
        
    def create_random(self,n):
        snum = len(self.ships)
        while len(self.ships) != snum + n:
            self.add_ship(self.random_ship())
        
           
           
def create_ship_from_line(line):
    l = line.split()
    name = l[0]
    positions = set()
    #print(l)
    for p in l[1:]:
        print(p)
        n = p.split(':')
        positions.add((int(n[0]),int(n[1])))
    return Ship(name, positions)

def load_grid_from_file(filename):
    with open(filename, 'r')as file:
        lines = file.readlines()        
        #print(lines[0])
        dim = lines[0].split(':')
        gx = int(dim[0])
        gy = int(dim[1])
        g = Grid(gx,gy)
        for l in lines[1:]:
            g.add_ship(create_ship_from_line(l))
    return g

class BlindGrid:
    """Encodes the opponent's view of the grid."""

    def __init__(self, grid):
        self.x_size = grid.x_size
        self.y_size = grid.y_size
        self.misses = grid.misses
        self.hits = set()
        self.sunken_ships = []
        #if s in grid.ships is a subset of hits, add s to sunken ships
        for s in grid.ships:
            self.hits = self.hits.union(s.hits)
            if s.positions == s.hits:
                self.sunken_ships.append(s)





















