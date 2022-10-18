from time import sleep
import os
import numpy as np

class Board:
    def __init__(self, size, random=False):
        self.size_t = (size, size)
        self.stagnant = False
        self.current_position = [0, 0]
        self.current_neighbours = 0

        if random: 
            self.arr_a = np.random.randint(2, size=self.size_t)
        else:
            self.arr_a = np.zeros(self.size_t, dtype=int)

        self.arr_b = np.zeros(self.size_t, dtype=int)
    
    def progress_board(self):
        if np.array_equal(self.arr_a, self.arr_b): self.stagnant = True
        self.arr_a = self.arr_b
        self.arr_b = np.zeros(self.size_t, dtype=int)

    def determine_fate(self):
        row, col = self.current_position
        n = self.current_neighbours
        if (self.arr_a[row][col] == 1 and n == 2 or 
            self.arr_a[row][col] == 1 and n == 3 or 
            self.arr_a[row][col] == 0 and n == 3): return 1
        else: return 0

    def count_neighbours(self):
        row_len, col_len = self.arr_a.shape
        row, col = self.current_position

        self.current_neighbours = 0
        for row_n in range(row-1, row+2):
            for col_n in range(col-1, col+2):
                if(0 <= row_n < row_len and 
                    0 <= col_n < col_len and
                    [row_n, col_n] != [row, col]):
                        self.current_neighbours += self.arr_a[row_n][col_n]

        return self.determine_fate()

    def iterate_board(self):
        row_len, col_len = self.arr_a.shape
        for row in range(row_len):
            for col in range(col_len):
                    self.current_position = [row, col]
                    self.arr_b[row][col] = self.count_neighbours()

    def play_board(self):
        self.iterate_board()
        self.progress_board()
        self.print_board()

    def print_board(self):
        os.system('cls')
        fmt = {'int': lambda i: '\x1b[{}m{}\x1b[0m'.format(1 if i else 8, b'\xfe'.decode('cp437'))} 
        np.set_printoptions(formatter=fmt, linewidth=1000)
        print(self.arr_a)

    def empty_board(self):
        return np.all(self.arr_a == 0)

    def stagnant_board(self):
        return self.stagnant

board = Board(30, random=True)

while(not board.empty_board() and not board.stagnant_board()):
    board.play_board()
    sleep(0.2)
    