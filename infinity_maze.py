import pygame as pg
from random import random
from copy import deepcopy


class Maze:
    def __init__(self, app_, width_, height_, is_blank):
        self.app = app_
        self.width = width_
        self.height = height_
        if is_blank:
            self.horisontal_walls = [[1 for _1 in range(self.width)] for _2 in range(self.height)]
            self.vertical_walls = [[1 for _1 in range(self.width - 1)] for _2 in range(self.height)]
        else:
            self.horisontal_walls = [[0 for _1 in range(self.width)] for _2 in range(self.height)]
            self.vertical_walls = [[0 for _1 in range(self.width - 1)] for _2 in range(self.height)]
        
    def create_maze_ascii(self):
        maze = [" _" * self.width + " "]
        for i in range(self.height - 1):
            row = "|"
            for j in range(self.width - 1):
                if self.horisontal_walls[i][j]:
                    row += "_"
                else:
                    row += " "
                if self.vertical_walls[i][j]:
                    row += "|"
                else:
                    row += " "
            if self.horisontal_walls[i][-1]:
                row += "_"
            else:
                row += " "
            row += "|"
            maze.append(row)
        row = "|"
        for j in range(self.width - 1):
            row += "_"
            if self.vertical_walls[-1][j]:
                row += "|"
            else:
                row += " "
        row += "_|"
        maze.append(row)
        
        return maze
    
    def print_ascii(self):
        maze_ascii = self.create_maze_ascii()
        for i in range(self.height + 1):
            print(maze_ascii[i])
            
    def draw_pygame(self):
        self.app.screen.fill(pg.Color('black'))
        
        for i in range(self.height - 1):
            for j in range(self.width):
                if self.horisontal_walls[i][j]:
                    pg.draw.line(self.app.screen, 'white', 
                                 (j * self.app.cell_size, (i + 1) * self.app.cell_size), 
                                 ((j + 1) * self.app.cell_size, (i + 1) * self.app.cell_size))
                    
        for i in range(self.height):
            for j in range(self.width - 1):
                if self.vertical_walls[i][j]:
                    pg.draw.line(self.app.screen, 'white', 
                                 ((j + 1) * self.app.cell_size, i * self.app.cell_size), 
                                 ((j + 1) * self.app.cell_size, (i + 1) * self.app.cell_size))


class Player:
    def __init__(self, app):
        self.pos_x = self.pos_y = 0
        self.app = app
        
    def draw(self):
        pg.draw.circle(self.app.screen, "red", 
                       ((self.pos_x + 0.5) * self.app.cell_size, (self.pos_y + 0.5) * self.app.cell_size), 
                       self.app.cell_size / 3)
        
    def control(self, keys):
        if keys[pg.K_w] or keys[pg.K_UP]:
            if (self.pos_y > 0) and not self.app.maze.horisontal_walls[self.pos_y - 1][self.pos_x]:
                self.pos_y -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            if (self.pos_y < (self.app.height - 1)) and not self.app.maze.horisontal_walls[self.pos_y][self.pos_x]:
                self.pos_y += 1
                if self.pos_y == 2:
                    self.pos_y -= 1
                    self.app.maze.horisontal_walls.pop(0)
                    self.app.maze.vertical_walls.pop(0)
                    self.app.maze.horisontal_walls.append([0 for _1 in range(self.app.width)])
                    self.app.maze.vertical_walls.append([0 for _1 in range(self.app.width - 1)])
                    self.app.algorithm.create_row(2)
                    
        if keys[pg.K_a]  or keys[pg.K_LEFT]:
            if (self.pos_x > 0) and not self.app.maze.vertical_walls[self.pos_y][self.pos_x - 1]:
                self.pos_x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if (self.pos_x < self.app.width - 1) and not self.app.maze.vertical_walls[self.pos_y][self.pos_x]:
                self.pos_x += 1



class Eller:
    def __init__(self, app):
        self.app = app
        self.is_blank = False
        
    def create_maze(self):
        for _ in range(self.app.height):
            self.create_row(_)


    def create_row(self, depth):
        for i in range(1, self.app.width):
            if (random() <= 0.5) or (self.app.arr[i] == self.app.arr[i - 1]):
                self.app.maze.vertical_walls[depth][i - 1] = 1
            else:
                new_group = self.app.arr[i]
                old_group = self.app.arr[i - 1]
                for _ in range(self.app.width):
                    if self.app.arr[_] == old_group:
                        self.app.arr[_] = new_group

        for i in range(self.app.width):
            if random() <= 0.5:
                self.app.maze.horisontal_walls[depth][i] = 1

        check_arr = [[0, 0, []] for _ in range(self.app.width)]

        for i in range(self.app.width):
            check_arr[self.app.arr[i] - 1][0] += 1
            if self.app.maze.horisontal_walls[depth][i]:
                check_arr[self.app.arr[i] - 1][1] += 1
                check_arr[self.app.arr[i] - 1][2].append(i)

        for count_cell, count_floor, indxes in check_arr:
            if (count_cell == count_floor) and (count_cell != 0):
                tmp = indxes[-1]
                self.app.maze.horisontal_walls[depth][tmp] = 0

        self.prev_arr = deepcopy(self.app.arr)

        for i in range(self.app.width):
            if self.app.maze.horisontal_walls[depth][i]:
                self.app.arr[i] = -1

        nums = [i + 1 for i in range(self.app.width)]

        for i in range(self.app.width):
            if self.app.arr.count(i + 1):
                nums.pop(nums.index(i + 1))

        for i in range(self.app.width):
            if self.app.arr[i] == -1:
                self.app.arr[i] = nums[0]
                nums.pop(0)


class App:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.arr = [i + 1 for i in range(width)]
        self.prev_arr = []
        self.cell_size = cell_size
        
        self.algorithm = Eller(self)
        self.maze = Maze(self, width, height, self.algorithm.is_blank)
        self.player = Player(self)
        
        self.algorithm.create_maze()
        
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


app = App(width=10, height=3, cell_size=50)
app.print_maze_pygame()
