from random import choice, randint, random
from copy import deepcopy

from typing import List, Tuple


def check_cell(app, x: int, y: int) -> List[Tuple[int, int]]:
    """Проверяет соседние клетки и возвращает список валидных координат.
    
    Args:
        app (App): Экземпляр главного приложения
        x (int): x координата текущей клетки
        y (int): y координата текущей клетки
        
    Returns:
        valid_cells (List[Tuple[int, int]]): Список кортежей с координатами (x, y) доступных соседей
    """
    sub_list = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]  # Верх, низ, лево, право
    res = []
    for i, j in sub_list:
        if (i >= 0) and (j >= 0) and (i < app.width) and (j < app.height):
            res.append((i, j))
    return res


class AldousBroder:
    """Реализация алгоритма генерации лабиринта Aldous-Broder."""
    
    def __init__(self, app) -> None:
        """Инициализирует алгоритм с привязкой к приложению.
        
        Args:
            app (App): Главное приложение с параметрами лабиринта
        """
        self.app = app
        self.is_blank = True  # Флаг для инициализации пустого лабиринта
    
    def create_maze(self) -> None:
        """Генерирует лабиринт используя алгоритм случайного блуждания."""
        map = [[0 for _ in range(self.app.width)] for _ in range(self.app.height)]
        count = self.app.width * self.app.height - 1
        x, y = randint(0, self.app.width - 1), randint(0, self.app.height - 1)
        map[y][x] = 1
        
        while count:
            sub_list = check_cell(self.app, x, y)
            i, j = choice(sub_list)
            if not map[j][i]:
                count -= 1
                map[j][i] = 1
                self.del_wall(x, y, i, j)
            x, y = i, j
            
    def del_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Удаляет стену между двумя соседними клетками.
        
        Args:
            (x1, y1): Координаты первой клетки
            (x2, y2): Координаты второй клетки
        """
        if x1 == x2:  # Вертикальные соседи
            self.app.maze.horisontal_walls[min(y1, y2)][x1] = 0
        else:  # Горизонтальные соседи
            self.app.maze.vertical_walls[y1][min(x1, x2)] = 0


class Eller:
    """Реализация алгоритма генерации лабиринта Эллера."""
    
    def __init__(self, app) -> None:
        """Инициализирует алгоритм с привязкой к приложению.
        
        Args:
            app (App): Главное приложение с параметрами лабиринта
        """
        self.app = app
        self.is_blank = False  # Флаг для инициализации заполненного лабиринта
        
    def create_maze(self) -> None:
        """Генерирует лабиринт построчно, используя алгоритм Эллера."""
        for depth in range(self.app.height):
            self.create_row(depth)
        self.finish_maze()

    def finish_maze(self) -> None:
        """Завершающий этап генерации - соединение последнего ряда."""
        for i in range(1, self.app.width):
            if self.prev_arr[i-1] != self.prev_arr[i]:
                self.app.maze.vertical_walls[-1][i - 1] = 0

    def create_row(self, depth: int) -> None:
        """Генерирует один ряд лабиринта.
        
        Args:
            depth (int): Номер текущего ряда
        """
        # Обработка вертикальных стен
        for i in range(1, self.app.width):
            if (random() <= 0.5) or (self.app.arr[i] == self.app.arr[i - 1]):
                self.app.maze.vertical_walls[depth][i - 1] = 1
            else:
                new_group = self.app.arr[i]
                old_group = self.app.arr[i - 1]
                for j in range(self.app.width):
                    if self.app.arr[j] == old_group:
                        self.app.arr[j] = new_group

        # Обработка горизонтальных стен
        for i in range(self.app.width):
            if random() <= 0.5:
                self.app.maze.horisontal_walls[depth][i] = 1

        # Проверка изолированных групп
        check_arr = [[0, 0, []] for _ in range(self.app.width)]
        for i in range(self.app.width):
            check_arr[self.app.arr[i] - 1][0] += 1
            if self.app.maze.horisontal_walls[depth][i]:
                check_arr[self.app.arr[i] - 1][1] += 1
                check_arr[self.app.arr[i] - 1][2].append(i)

        # Удаление изолированных групп
        for count_cell, count_floor, indexes in check_arr:
            if (count_cell == count_floor) and (count_cell != 0):
                tmp = indexes[-1]
                self.app.maze.horisontal_walls[depth][tmp] = 0

        # Подготовка к следующему ряду
        self.prev_arr = deepcopy(self.app.arr)
        for i in range(self.app.width):
            if self.app.maze.horisontal_walls[depth][i]:
                self.app.arr[i] = -1

        # Перенумерация групп
        nums = [i + 1 for i in range(self.app.width)]
        for i in range(self.app.width):
            if self.app.arr.count(i + 1):
                nums.pop(nums.index(i + 1))

        for i in range(self.app.width):
            if self.app.arr[i] == -1:
                self.app.arr[i] = nums[0]
                nums.pop(0)


class BinaryTree:
    """Реализация алгоритма генерации лабиринта Binary Tree."""
    
    def __init__(self, app) -> None:
        """Инициализирует алгоритм с привязкой к приложению.
        
        Args:
            app (App): Главное приложение с параметрами лабиринта
        """
        self.app = app
        self.is_blank = True
    
    def create_maze(self) -> None:
        """Генерирует лабиринт, где каждая клетка соединяется либо с верхней, либо с левой."""
        for depth in range(1, self.app.height):
            for i in range(self.app.width - 1):
                if random() <= 0.5:  # 50% вероятность
                    self.app.maze.vertical_walls[depth][i] = 0  # Соединяем с левой
                else:
                    self.app.maze.horisontal_walls[depth - 1][i] = 0  # Соединяем с верхней

        # Обработка границ
        for i in range(self.app.width - 1):
            self.app.maze.vertical_walls[0][i] = 0  # Первый ряд соединяем с левой
        
        for j in range(self.app.height - 1):
            self.app.maze.horisontal_walls[j][-1] = 0  # Последний столбец соединяем с верхней


class Sidewinder:
    """Реализация алгоритма генерации лабиринта Sidewinder."""
    
    def __init__(self, app) -> None:
        """Инициализирует алгоритм с привязкой к приложению.
        
        Args:
            app (App): Главное приложение с параметрами лабиринта
        """
        self.app = app
        self.is_blank = True
    
    def create_maze(self) -> None:
        """Генерирует лабиринт, используя алгоритм Sidewinder."""
        for depth in range(1, self.app.height):
            sub_set = [0]  # Начальный набор клеток
            curr = 0  # Текущая позиция
            
            while curr < self.app.width:
                if (random() <= 0.5) or (curr == self.app.width - 1):
                    # Соединяем случайную клетку из набора с верхним рядом
                    self.app.maze.horisontal_walls[depth - 1][choice(sub_set)] = 0
                    curr += 1
                    sub_set = [curr]  # Начинаем новый набор
                else:
                    # Соединяем с левой клеткой
                    self.app.maze.vertical_walls[depth][curr] = 0
                    curr += 1
                    sub_set.append(curr)  # Расширяем текущий набор

        # Первый ряд полностью соединяем по горизонтали
        for i in range(self.app.width - 1):
            self.app.maze.vertical_walls[0][i] = 0
