import pygame as pg
from sub_classes import *
from algorithms import *


class App:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.arr = [i + 1 for i in range(width)]
        self.prev_arr = []
        self.cell_size = cell_size
        
        # Алгоритм генерации пихать сюда. Список всех алгоримов в "algorithms.py".
        self.algorithm = Sidewinder(self)
        self.maze = Maze(self, width, height, self.algorithm.is_blank)
        self.player = Player(self)
        
    def print_maze_pygame(self):
        self.clock = pg.time.Clock()
        self.screen_size = self.screen_width, self.screen_height = self.cell_size * self.width, self.cell_size * self.height
        self.screen = pg.display.set_mode(self.screen_size)
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            self.player.control(pg.key.get_pressed())
                    
            self.maze.draw_pygame()
            self.player.draw()
            pg.display.flip()
        
            self.clock.tick(10)


app = App(width=130, height=70, cell_size=10)
app.algorithm.create_maze()
app.maze.print_ascii()
app.print_maze_pygame()
