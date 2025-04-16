import pygame as pg

from sub_classes import *
from algorithms import *

from typing import List


class App:
    """Главный класс приложения для генерации и визуализации лабиринтов.
    
    Attributes:
        width (int): Ширина лабиринта в клетках.
        height (int): Высота лабиринта в клетках.
        arr (List[int]): Массив для отслеживания групп клеток.
        prev_arr (List[int]): Предыдущее состояние групп клеток.
        cell_size (int): Размер клетки в пикселях.
        algorithm (str): Экземпляр выбранного алгоритма генерации.
        maze (Maze): Объект лабиринта.
        player (Player): Объект игрока.
        screen: Поверхность отображения Pygame.
        clock (pg.time.Clock): Объект часов Pygame.
    """
    
    def __init__(self, width: int, height: int, cell_size: int, algorithm: str = 'Sidewinder') -> None:
        """Инициализирует приложение для генерации лабиринта.
        
        Args:
            width (int): Ширина лабиринта в клетках.
            height (int): Высота лабиринта в клетках.
            cell_size (int): Размер клетки в пикселях.
            algorithm (str): Название алгоритма генерации. Варианты:
                'AldousBroder', 'Eller', 'BinaryTree', 'Sidewinder' (по умолчанию).
        """
        self.width = width
        self.height = height
        self.arr = [i + 1 for i in range(width)]  # Инициализация групп клеток
        self.prev_arr = []  # Для отслеживания предыдущей строки в алгоритме Эллера
        self.cell_size = cell_size
        
        # Соответствие названий алгоритмов их классам
        name_to_algorithm = {
            'AldousBroder': AldousBroder, 
            'Eller': Eller, 
            'BinaryTree': BinaryTree, 
            'Sidewinder': Sidewinder
        }
        self.algorithm = name_to_algorithm[algorithm](self)  # Создаем экземпляр выбранного алгоритма

        # Инициализируем лабиринт и игрока
        self.maze = Maze(self, width, height, self.algorithm.is_blank)
        self.player = Player(self)

        # Генерируем лабиринт
        self.algorithm.create_maze()

    def print_maze_ascii(self) -> None:
        """Выводит ASCII-представление лабиринта в консоль."""
        self.maze.print_ascii()
        
    def print_maze_pygame(self) -> None:
        """Запускает визуализацию лабиринта с использованием Pygame."""
        self.clock = pg.time.Clock()
        self.screen_size = self.screen_width, self.screen_height = (
            self.cell_size * self.width, 
            self.cell_size * self.height
        )
        self.screen = pg.display.set_mode(self.screen_size)
        
        # Главный игровой цикл
        while True:
            # Обработка событий
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            # Управление игроком
            self.player.control(pg.key.get_pressed())
                    
            # Отрисовка
            self.maze.draw_pygame()
            self.player.draw()
            pg.display.flip()  # Обновление экрана
        
            # Ограничение до 10 кадров в секунду
            self.clock.tick(10)


if __name__ == "__main__":
    app = App(width=20, height=20, cell_size=10)
    app.print_maze_ascii()
    app.print_maze_pygame()
