# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import MessageBox

from random import randrange
from view.cell import Cell

class Bot(object):
    """Осуществляет стрельбу по кораблям игрока"""

    def __init__(self, fleet_user, cells):
        # ячейки игрового поля игрока
        self.cells = cells
        # массив точек, в которые стрелял бот
        self.bot_shoot = set()
        # массив точек, куда попал бот в корабль
        self.bot_hits = []
        # точки, в которые попал бот
        self.last_fleet = None
        # попал в корабль, значит статус True
        self.hit_status = True
        # корабли игрока
        self.fleet_user = fleet_user

    def hit(self):
        """Определяет порядок стрельбы по кораблям"""
        if self.last_fleet is None:
            self.first_shoot()
        else:
            self.next_shoot()

    def first_shoot(self):
        """Делает первый рандомный выстрел по карте игрока,
        а также выстрел после убийства корабля"""
        # чтобы не уйти в бесконечный цикл, когда все клетки заполнены
        if len(self.bot_shoot) >= 100:
            return
        a = 1
        while a:
            y = randrange(1, 11)
            x = randrange(1, 11)
            point = "my_" + str(x) + "_" + str(y)
            if not (point in self.bot_shoot):
                a = 0
                self.bot_shoot.add(point)
                # изменить статус корабля
                print("Передаю ход")
                self.change_status(point)

    def next_shoot(self):
        """Если есть попадание, данная функция продолжает стрельбу"""
        point = self.points_around()
        if not point:
            self.first_shoot()
        else:
            self.change_status(point)

    def change_status(self, point):
        """Изменить статус кораблей"""
        for obj in self.fleet_user:
            if point in obj.coord_map:
                obj.shoot(point)
                self.hit_status = True
                self.bot_shoot.add(point)
                # если попал в однопалубный корабль, а также проверка на смерть
                if self.check_death(obj):
                    self.last_fleet = None
                    self.bot_hits = []
                    # чтобы он остановился на точке, в которую попал
                    break
                else:
                    # если попал в корабль, который больше 1 палубы
                    self.bot_hits.append(point)
                    self.last_fleet = obj
                    # self.points_around()
                    self.change_color(point)
                    break
            # если промахнулся и никуда и не попадал, в том числе после убийства корабля
            self.hit_status = False
            self.bot_shoot.add(point)
        self.change_color(point)
        # print(f"точка - {point} "
        #       f"статус попаданий {self.hit_status} "
        #       f"последний корабль {self.last_fleet} ")
        if self.hit_status:
            self.hit()

    def check_death(self, obj):
        # проверить не уничтожен ли корабль,
        # покрасить соседние клетки вокруг
        if obj.death:
            for point in obj.around_map:
                x = int(point.split("_")[1])
                y = int(point.split("_")[2])
                neighbro_cell = self.cells[x][y]
                neighbro_cell.paint(False)
                self.bot_shoot.add(point)
            return True
        else:
            return False

    def points_around(self):
        points_around = []
        bot_hits = self.bot_hits
        # ищет куда можно стрелять, исключает диагональные клетки
        for hit in bot_hits:
            current_x = int(hit.split("_")[1])
            current_y = int(hit.split("_")[2])
            for dy in (-1, 0, 1):
                y = current_y + dy
                if not (1 <= y <= 10):
                    continue
                for dx in (-1, 0, 1):
                    x = current_x + dx
                    if not (1 <= x <= 10):
                        continue
                    if not ("my_" + str(x) + "_" + str(y) in self.bot_shoot) and len(self.bot_hits) < 2:
                        if any([x == current_x and y == current_y + 1,
                                x == current_x and y == current_y - 1,
                                x == current_x - 1 and y == current_y,
                                x == current_x + 1 and y == current_y]):
                            points_around.append([x, y])
                    # если длина корабля больше 1, то исключает клетки в которые нельзя
                    # стрелять логически, а также ищет куда можно стрелять,
                    # красит ячейки
                    if len(self.bot_hits) > 1:
                        self.hit_status = False
                        orientation = self.get_orientation(self.bot_hits)
                        if orientation:
                            if any([not x == current_x - 1 and not y == current_y,
                                    not x == current_x + 1 and not y == current_y]):
                                self.change_color("my_" + str(x) + "_" + str(y))
                                self.bot_shoot.add("my_" + str(x) + "_" + str(y))
                            else:
                                if not ("my_" + str(x) + "_" + str(y) in self.bot_shoot):
                                    points_around.append([x, y])
                        if not orientation:
                            if any([not x == current_x and not y == current_y + 1,
                                    not x == current_x and not y == current_y - 1]):
                                self.change_color("my_" + str(x) + "_" + str(y))
                                self.bot_shoot.add("my_" + str(x) + "_" + str(y))
                            else:
                                if not ("my_" + str(x) + "_" + str(y) in self.bot_shoot):
                                    points_around.append([x, y])
                        self.hit_status = True
            # если корабль больше 2 ячеек, и стрелять боту некуда
            if len(points_around) == 0:
                return list(set(self.last_fleet.coord_map) - set(self.bot_hits)).pop()
            select = randrange(len(points_around))
            x = points_around[select][0]
            y = points_around[select][1]
            point = "my_" + str(x) + "_" + str(y)
            return point

    def check_finish(self):
        """Проверка закончена ли игра"""
        count = 0
        for ship in self.fleet_user:
            count += ship.death
        return count

    def change_color(self, point):
        """Изменить цвет ячеек"""
        x = int(point.split("_")[1])
        y = int(point.split("_")[2])
        cell = self.cells[x][y]
        if self.hit_status:
            cell.paint(True)
        else:
            cell.paint(False)

    def get_orientation(self, hits):
        """Если корабль горизонтальный, вернет True,
        если корабль вертикальный, вернет False"""
        horizontal = set()
        vertical = set()
        for hit in hits:
            x = int(hit.split("_")[1])
            y = int(hit.split("_")[2])
            horizontal.add(x)
            vertical.add(y)
        if len(horizontal) > len(vertical):
            return True
        if len(horizontal) < len(vertical):
            return False

    def __str__(self):
        return "Бот активирован"
