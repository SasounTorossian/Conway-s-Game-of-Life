from time import sleep
import os
import numpy as np

ASCII_BOCK_CODE = bytes([254]).decode('cp437')
SLEEP_TIME = 0.2

class World:
    def __init__(self, size, random=False):
        self.size_t = (size, size)
        self.stagnant = False
        self.old_world = np.random.randint(2, size=self.size_t) if random else np.zeros(self.size_t, dtype=int)
        self.new_world = np.zeros(self.size_t, dtype=int)
        self.configure_printing()

    def play_board(self):
        self.create_new_generation()
        self.is_new_same_as_old()
        self.new_gen_to_world()
        self.print_board()

    def create_new_generation(self):
        row_len, col_len = self.old_world.shape
        for row in range(row_len):
            for col in range(col_len):
                    position = [row, col]
                    neighbours = self.count_neighbours(position)
                    self.determine_fate(position, neighbours)

    def count_neighbours(self, position):
        row_len, col_len = self.old_world.shape
        row, col = position
        current_neighbours = 0
        for row_n in range(row-1, row+2):
            for col_n in range(col-1, col+2):
                if(0 <= row_n < row_len and 
                    0 <= col_n < col_len and
                    [row_n, col_n] != [row, col]):
                        current_neighbours += self.old_world[row_n][col_n]

        return current_neighbours
    
    def determine_fate(self,position, neighbours):
        row, col = position
        n = neighbours
        if (self.old_world[row][col] == 1 and n == 2 or 
            self.old_world[row][col] == 1 and n == 3 or 
            self.old_world[row][col] == 0 and n == 3): 
            self.new_world[row][col] = 1
        else: 
            self.new_world[row][col] = 0

    def new_gen_to_world(self):
        self.old_world = self.new_world
        self.new_world = np.zeros(self.size_t, dtype=int)

    def configure_printing(self):
        fmt = {'int': lambda i: '\033[{}m{}\033[0m'.format(1 if i else 8, ASCII_BOCK_CODE)}
        np.set_printoptions(formatter=fmt, linewidth=1000)

    def print_board(self):
        os.system('clear')
        print(self.old_world)

    def is_new_same_as_old(self):
        if np.array_equal(self.old_world, self.new_world): self.stagnant = True

    def is_empty(self):
        return np.all(self.old_world == 0)

    def is_stagnant(self):
        return self.stagnant

world = World(30, random=True)

while(not world.is_empty() and not world.is_stagnant()):
    world.play_board()
    sleep(SLEEP_TIME)
    