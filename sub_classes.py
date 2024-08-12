import pygame as pg


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
        if keys[pg.K_a]  or keys[pg.K_LEFT]:
            if (self.pos_x > 0) and not self.app.maze.vertical_walls[self.pos_y][self.pos_x - 1]:
                self.pos_x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if (self.pos_x < self.app.width - 1) and not self.app.maze.vertical_walls[self.pos_y][self.pos_x]:
                self.pos_x += 1
