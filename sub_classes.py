import pygame as pg

from typing import List


class Maze:
    """Класс для представления и отображения лабиринта.
    
    Отвечает за хранение структуры лабиринта и его визуализацию в разных форматах.
    
    Attributes:
        app (App): Ссылка на родительское приложение.
        width (int): Ширина лабиринта в клетках.
        height (int): Высота лабиринта в клетках.
        horisontal_walls (List[List[int]]): Матрица горизонтальных стен.
        vertical_walls (List[List[int]]): Матрица вертикальных стен.
    """
    
    def __init__(self, app, width: int, height: int, is_blank: bool) -> None:
        """Инициализирует лабиринт с заданными параметрами.
        
        Args:
            app: Главное приложение.
            width: Ширина лабиринта в клетках.
            height: Высота лабиринта в клетках.
            is_blank: Если True, создает лабиринт со всеми стенами, иначе - без стен.
        """
        self.app = app
        self.width = width
        self.height = height
        
        # Инициализация стен
        if is_blank:
            # Создаем лабиринт со всеми стенами
            self.horisontal_walls = [[1 for _ in range(width)] for _ in range(height)]
            self.vertical_walls = [[1 for _ in range(width - 1)] for _ in range(height)]
        else:
            # Создаем лабиринт без стен
            self.horisontal_walls = [[0 for _ in range(width)] for _ in range(height)]
            self.vertical_walls = [[0 for _ in range(width - 1)] for _ in range(height)]
    
    def create_maze_ascii(self) -> List[str]:
        """Генерирует ASCII-представление лабиринта.
        
        Returns:
            maze_lines (List[str]): Список строк, где каждая строка представляет ряд лабиринта.
        """
        maze = [" _" * self.width + " "]  # Верхняя граница
        
        for i in range(self.height - 1):
            row = "|"  # Левая граница
            for j in range(self.width - 1):
                # Добавляем пол или стену в зависимости от состояния
                row += "_" if self.horisontal_walls[i][j] else " "
                row += "|" if self.vertical_walls[i][j] else " "
            
            # Правая граница и последняя клетка в ряду
            row += "_" if self.horisontal_walls[i][-1] else " "
            row += "|"
            maze.append(row)
        
        # Нижняя граница
        row = "|"
        for j in range(self.width - 1):
            row += "_"
            row += "|" if self.vertical_walls[-1][j] else " "
        row += "_|"
        maze.append(row)
        
        return maze
    
    def print_ascii(self) -> None:
        """Выводит ASCII-представление лабиринта в консоль."""
        maze_ascii = self.create_maze_ascii()
        for row in maze_ascii:
            print(row)
    
    def draw_pygame(self) -> None:
        """Отрисовывает лабиринт с использованием Pygame."""
        self.app.screen.fill(pg.Color('black'))
        
        # Отрисовка горизонтальных стен
        for i in range(self.height - 1):
            for j in range(self.width):
                if self.horisontal_walls[i][j]:
                    start_pos = (j * self.app.cell_size, (i + 1) * self.app.cell_size)
                    end_pos = ((j + 1) * self.app.cell_size, (i + 1) * self.app.cell_size)
                    pg.draw.line(self.app.screen, 'white', start_pos, end_pos)
        
        # Отрисовка вертикальных стен
        for i in range(self.height):
            for j in range(self.width - 1):
                if self.vertical_walls[i][j]:
                    start_pos = ((j + 1) * self.app.cell_size, i * self.app.cell_size)
                    end_pos = ((j + 1) * self.app.cell_size, (i + 1) * self.app.cell_size)
                    pg.draw.line(self.app.screen, 'white', start_pos, end_pos)


class Player:
    """Класс для представления игрока в лабиринте.
    
    Attributes:
        pos_x (int): Текущая x-координата игрока.
        pos_y (int): Текущая y-координата игрока.
        app (App): Ссылка на родительское приложение.
    """
    
    def __init__(self, app) -> None:
        """Инициализирует игрока в стартовой позиции (0, 0).
        
        Args:
            app (App): Главное приложение.
        """
        self.pos_x = 0
        self.pos_y = 0
        self.app = app
    
    def draw(self) -> None:
        """Отрисовывает игрока в виде красного круга."""
        center = (
            (self.pos_x + 0.5) * self.app.cell_size,
            (self.pos_y + 0.5) * self.app.cell_size
        )
        radius = self.app.cell_size / 3
        pg.draw.circle(self.app.screen, "red", center, radius)
    
    def control(self, keys: List[bool]) -> None:
        """Обрабатывает управление игроком с клавиатуры.
        
        Args:
            keys (List[bool]): Список состояний клавиш из pg.key.get_pressed().
        """
        # Движение вверх (W или стрелка вверх)
        if keys[pg.K_w] or keys[pg.K_UP]:
            if (self.pos_y > 0) and not self.app.maze.horisontal_walls[self.pos_y - 1][self.pos_x]:
                self.pos_y -= 1
        
        # Движение вниз (S или стрелка вниз)
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            if (self.pos_y < (self.app.height - 1)) and not self.app.maze.horisontal_walls[self.pos_y][self.pos_x]:
                self.pos_y += 1
        
        # Движение влево (A или стрелка влево)
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if (self.pos_x > 0) and not self.app.maze.vertical_walls[self.pos_y][self.pos_x - 1]:
                self.pos_x -= 1
        
        # Движение вправо (D или стрелка вправо)
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            if (self.pos_x < self.app.width - 1) and not self.app.maze.vertical_walls[self.pos_y][self.pos_x]:
                self.pos_x += 1
