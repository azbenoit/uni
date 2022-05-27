#!/usr/bin/env python3

# In grids/boards: (0,0) is the top-left corner.

import random
import time
import tkinter as tk
try:
    import tkinter.font
    import tkinter.messagebox
except ModuleNotFoundError:
    pass

# Square Class ################################################################

class Square():
    """ A square of the game.
    Data attributes:
        - revealed: True/False
        - flagged: True/False
        - mined: True/False
        - mines_nearby: count of known neighboring mines
    """
    # DO NOT MODIFY THIS CLASS!

    def __init__(self):
        self.revealed = False
        self.flagged = False
        self.mined = False
        self.mines_nearby = 0

    def reset(self):
        """Reset this Square back to a blank state."""
        self.revealed = False
        self.flagged = False
        self.mined = False
        self.mines_nearby = 0

    def __str__(self):
        if self.mined:
            return '*'
        elif self.mines_nearby == 0:
            return '.'
        return str(self.mines_nearby)

    def str_for_player(self):
        if not self.revealed:
            if self.flagged:
                return 'F'
            return '#'
        if self.mined:
            return '*'
        if self.mines_nearby == 0:
            return '.'
        return str(self.mines_nearby)

# GameGrid Class ##############################################################

class GameGrid:
    """ A game grid, containing Squares.
    Models the state of a Minesweeper game.
    Data attributes:
        - nrows: the number of rows
        - ncols: the number of columns
        - nmines: the number of mines
        - nflags: the number of flags currently placed
        - tab: a list of nrows lists, each of ncols Square objects
        - squares_revealed: the number of Squares that have been revealed
    Note that (0,0) is the top left position.
    """

    def __init__(self, nrows, ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.nmines = 0
        self.nflags = 0
        self.tab = [[Square() for j in range(self.ncols)]
                    for i in range(self.nrows)]
        self.squares_revealed = 0

    def __str__(self):
        """Useful for debugging: describes the board with all the squares revealed"""
        lines = [''.join([str(sq) for sq in line]) for line in self.tab]
        return '\n'.join(lines)

    def str_for_player(self):
        """Useful for debugging: describes the board for the player's point of view"""
        lines = [''.join([sq.str_for_player() for sq in line]) for line in self.tab]
        return '\n'.join(lines)

    # Methods for accessing a specific square and its propreties

    # EXERCISE 1
    def neighbors(self, i, j):
        """Returns a list of tuples (x, y) of valid
        neighboring positions; the order does not matter
        """
        n = []
        for k in range(3):
            for l in range(3):
                if 0 <= i+k-1 < self.nrows and 0 <= j+l-1 < self.ncols: 
                    n.append((i+k-1,j+l-1))
        n.remove((i,j))
        return n


    def square_at(self, i, j):
        """The square at position (i, j)."""
        return self.tab[i][j]

    def revealed(self, i, j):
        """True iff the Square at (i, j) has been revealed."""
        return self.square_at(i, j).revealed

    def flagged(self, i, j):
        """True iff there is a flag at position (i,j)."""
        return self.square_at(i, j).flagged

    def mined(self, i, j):
        """True iff there is a mine in the Square at (x,y)."""
        return self.square_at(i, j).mined

    def mines_nearby(self, i, j):
        """The number of mines near (i, j)."""
        return self.square_at(i, j).mines_nearby

    # EXERCISE 3
    def flags_nearby(self, i, j):
        """The number of flages near (i, j)."""
        f = 0
        for l,k in self.neighbors(i, j):
            if self.square_at(l, k).flagged: f+=1
        return f

    #--------------------------------------------------------------------------
    # Function for changing the state of a square

    def place_flag(self, i, j):
        """If there is no flag at (i,j) then add a flag there,
        and increase the flag count.
        """
        if not self.flagged(i, j):
            self.square_at(i, j).flagged = True
            self.nflags += 1

    # EXERCISE 2
    def place_mine(self, i, j):
        """If there is a mine at (i, j), does nothing;
        Otherwise, places a mine at (i, j) and increments
        mines_nearby for all the neighbors
        """
        if self.square_at(i, j).mined:
            return
        else:
            self.square_at(i, j).mined = True
            for l,k in self.neighbors(i, j):
                self.square_at(l, k).mines_nearby += 1
            self.nmines += 1

    # EXERCISE 5
    def reveal(self, i, j):
        """Reveal the square at (x,y);
        if there are no mines nearby, reveals all the neighbors
        """
        if self.square_at(i, j).revealed or self.square_at(i, j).flagged:
            return
        else:
            self.squares_revealed +=1
            self.square_at(i, j).revealed = True
            if not self.square_at(i, j).mined and self.mines_nearby(i, j) == 0:
                for l,k in self.neighbors(i, j):
                    self.reveal(l, k)
            

    # EXERCISE 6
    def chording(self, i, j):
        """If the number of flags nearby does not coincide
        with the number mines nearby, does nothing.
        Otherwise, reveals all the non-flagged neighbors
        """
        if self.flags_nearby(i, j) == self.mines_nearby(i, j):
            for l,k in self.neighbors(i, j):
                if not self.square_at(l, k).flagged:
                    self.reveal(l, k)
                    
    def remove_flag(self, i, j):
        """If there is flag at (i,j) then remove it,
        and decrease the flag count.
        """
        if self.flagged(i, j):
            self.square_at(i, j).flagged = False
            self.nflags -= 1

    #--------------------------------------------------------------------------
    # Methods acting on the whole board

    # EXERCISE 4
    def random_game(self, n_mines):
        """Reset the game grid and place n_mines random mines."""
        if n_mines <= 0 or n_mines >= self.nrows*self.ncols:
            raise Exception(f'Invalid number of mines ({n_mines}).')
        self.reset()
        while(self.nmines < n_mines):
            (i,j) = (random.randint(0, self.nrows-1), random.randint(0, self.ncols-1))
            self.place_mine(i, j)
        

    def game_won(self):
        """True iff the game has been won:
        1. all non-mined Squares have been revealed, and
        2. no mined Squares have been revealed.
        """
        return (not self.game_lost()) and (self.nrows * self.ncols - self.squares_revealed) == self.nmines

    def game_lost(self):
        """True iff at least one mine is revealed"""
        for i in range(self.nrows):
            for j in range(self.ncols):
                if self.mined(i, j) and self.revealed(i, j):
                    return True
        return False

    def reset(self):
        """Reset every Square in the GameGrid back to blank."""
        for row in self.tab:
            for square in row:
                square.reset()
        self.nmines = 0
        self.nflags = 0
        self.squares_revealed = 0

# Minesweeper App #############################################################

class MinesweeperApp:
    """Minesweeper graphical game.
    Data attributes:
        - game: a GameGrid object with the layout of mines
        - t_0: the time that the current game started
        - started: True if the game has already started (that is, 
                   the first click has been made)
        - root: a Tk display
        - board: the array of buttons to be clicked on
        - flag_image: a picture of a flag
        - mine_image: a picture of a mine
        - game_frame: the tkinter frame with the buttons
        - top_frame: the tkinter frame with the counters
        - mine_counter: the tkinter label with the mine counter
        - mine_counter_str: the corresponding tkinter string
        - time_counter, time_counter_str - the same for time
    """

    def __init__(self, game):
        self.game = game
        self.started = False

        # Set up base window...
        self.root = tk.Tk()
        self.root['bg'] = 'white'
        self.root.resizable(width=False, height=False)
        self.flag_image = tk.PhotoImage(file='flag.gif')
        self.mine_image = tk.PhotoImage(file='mine.gif')

        # Create and set up game frame
        self.game_frame = tk.Frame(self.root, borderwidth=2, relief=tk.SUNKEN)

        self.board = [[self.make_cell(i, j) for j in range(self.game.ncols)]
                      for i in range(self.game.nrows)]
        self.game_frame.pack(padx=10, pady=10, side=tk.BOTTOM)
        self.draw_board()

        # Create top frame (with mine counter, new game button, timer)
        self.top_frame = tk.Frame(self.root,
                             borderwidth=2,
                             height=40,
                             relief=tk.GROOVE)
        self.top_frame.pack(padx=0, pady=0, side=tk.TOP, fill="x")
        self.top_frame.columnconfigure(0, weight=1)  # For mine counter
        self.top_frame.columnconfigure(1, weight=1)  # For 'New game' button
        self.top_frame.columnconfigure(2, weight=1)  # For timer

        # Mine counter (top left, top frame):
        self.mine_counter_str = tk.StringVar()
        self.mine_counter_str.set('MINES')
        self.mine_counter = tk.Label(self.top_frame,
                                height=1,
                                width=4,
                                bg='white',
                                textvariable=self.mine_counter_str,
                                font=tk.font.Font(weight='bold', size=10))
        self.mine_counter.grid(row=0, column=0, padx=5, sticky=tk.W)
        try:
            self.update_mine_counter()
        except AttributeError:
            pass

        # New game button (top centre, top frame):
        # When clicked, this button generates a call to new_game.
        self.newgame_button = tk.Button(self.top_frame,
                                   bd=1,
                                   width=15,
                                   text="New game",
                                   command=self.new_game)
        self.newgame_button.grid(row=0, column=1, padx=0, sticky=tk.E)

        # Timer (top right, top frmae):.
        self.t_0 = time.time()
        self.time_counter_str = tk.StringVar()
        self.time_counter_str.set('TIME')
        self.time_counter = tk.Label(self.top_frame,
                                height=1,
                                width=4,
                                bg='white',
                                textvariable=self.time_counter_str,
                                font=tk.font.Font(slant='italic', size=10))
        self.time_counter.grid(row=0, column=2, padx=5, sticky=tk.E)
        try:
            self.update_time_counter()
        except AttributeError:
            pass

    def run(self):
        self.root.mainloop()

    def make_cell(self, i, j):
        """Make a 30x30 Frame holding a Button corresponding to a Square
        at (i,j) in the GameGrid.
        """
        # First, create a 30x30 frame within to hold a button object.
        # This provides a rigid piece of screen real estate for the button,
        # and prevents awkward resizing when we change the text or image.
        # image in the button.
        cell_frame = tk.Frame(self.game_frame, height=30, width=30)
        cell_frame.pack_propagate(False)
        cell_frame.grid(row=i, column=j)

        # Now set up the new button within the new frame:
        cell_button = tk.Button(cell_frame,
                                borderwidth=1,
                                state='normal',
                                disabledforeground='#000000')
        cell_button.pack(fill=tk.BOTH, expand=True)

        # Tkinter allows us to "bind" a function f (say) to an event such
        # as a mouse being clicked on this Button.  But that function
        # must take the event object as an argument (and some other keyword
        # arguments that we're not very interested in...)  So we are forced
        # to define a no-argument function to "wrap" the functionality we
        # want, supplying any missing arguments from the current context.
        # For example: we want to call the method left_click_handler(i, j)
        # when the mouse is left-clicked over (i, j).  So we need a wrapper
        # function _on_left_click(event) to call left_click_handler(i, j).
        # (It's traditional to use the lambda construction for the wrapper,
        # but since we haven't covered that in class yet, we'll just define
        # the functions using def...  See Lecture E.)
        def _on_left_click(event):
            print(f'left click in cell {(i, j)}')
            self.left_click_handler(i, j)

        def _on_right_click(event):
            print(f'right click in cell {(i, j)}')
            self.right_click_handler(i, j)

        # Register the callbacks for mouse click events:
        cell_button.bind('<Button-1>', _on_left_click)
        cell_button.bind('<Button-3>', _on_right_click)
        return cell_button

    # EXERCISE 7
    def update_mine_counter(self):
        """Updates mine counter and schedules the next update in 100 ms"""
        self.mine_counter_str.set(self.game.nmines - self.game.nflags)
        self.top_frame.after(100,self.update_mine_counter)
        

    # EXERCISE 8
    def update_time_counter(self):
        """Updated the time counter and schedules the next update in 100ms"""
        if not self.started:
            self.time_counter_str.set(0)
        else:
            self.time_counter_str.set(self.game_time())
        self.top_frame.after(100, self.update_time_counter)

    def draw_cell(self, i, j):
        """Draws the cell with coordinates (i, j)"""
        cell = self.board[i][j]
        cell['image'] = ''
        cell['text'] = ''
        if self.game.revealed(i, j):
            cell['relief'] = tk.SUNKEN
            if self.game.mined(i, j):
                cell['image'] = self.mine_image
                cell['state'] = 'normal'
            else:
                mines_nearby = self.game.mines_nearby(i, j)
                cell['text'] = '' if mines_nearby == 0 else mines_nearby
                cell['state'] = 'disabled'
        else:
            cell['relief'] = tk.RAISED
            if self.game.flagged(i, j):
                cell['image'] = self.flag_image
                cell['state'] = 'normal'
            else:
                cell['state'] = 'disabled'

    def draw_board(self):
        """Draws the board"""
        for i in range(self.game.nrows):
            for j in range(self.game.ncols):
                self.draw_cell(i, j)

    def new_game(self):
        """Reset the game grid, board, re-distribute random mines, and
        reinitialise the timer.
        """
        nmines = self.game.nmines
        self.game.reset()
        self.draw_board()
        self.game.random_game(nmines)
        self.t_0 = time.time()
        self.started = False

    def game_time(self):
        """The current elapsed time since the game started, rounded down to a
        whole second.
        """
        if not self.started:
            return 0
        delta = time.time() - self.t_0
        return int(delta//1)  # Round down and convert to int

    def game_over(self, win):
        """End-game sequence: display an appropriate message, win or lose,
        and propose a new game.
        """
        title = 'Game over!'
        if win:
            message = f'Well done! You won in {self.game_time()} seconds.\nPlay again?'
        else:
            message = f'Too bad, you lost after {self.game_time()} seconds.\nTry again?'
        if tk.messagebox.askyesno(title, message):
            self.new_game()
        else:
            # Good bye!
            self.root.destroy()

    # EXERCISE 9
    def left_click_handler(self, i, j):
        """To be called when there is a left-click on the cell at (i, j).
        The left mouse button reveals cells, so this method
        - If (i, j) is revealed, then chording is performed
        - If (i, j) is flagged, then nothing happens
        - If (i,j) is not revealed and not flagged, and reveals (i,j).
        Note that the board should be redrawn
        """
        if not self.started:
            self.t_0 = time.time()
            self.started = True
        if not self.game.square_at(i,j).flagged:
            if self.game.square_at(i,j).revealed:
                self.game.chording(i,j)
            else:
                self.game.reveal(i,j)

    # EXERCISE 10
    def right_click_handler(self, i, j):
        """To be called when there is a right-click on the cell at (i, j).
        The right mouse button controls marker flags, so this method
        - Does nothing if (i, j) has already been revealed
        - Sets a flag at non-revealed (i, j) if it has no flag
        - Removes the flag at non-revealed (i, j) if it already has a flag
        """
        if not self.game.square_at(i,j).revealed:
            if not self.game.square_at(i,j).flagged:
                self.game.place_flag(i,j)
            else:
                self.game.remove_flag(i,j)
            self.draw_cell(i, j)
