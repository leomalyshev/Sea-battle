# -*- coding: utf-8 -*-
from random import randrange

ship_point = "enemy" + "_" + str(randrange(1, 11)) + "_" + str(randrange(1, 11))
shootpoint = "enemy_7_3"


class Ship(object):
    """
    Реализация поведения корабля

    length - длина корабля
    orientation - ориентация корабля, 1 - вертикальное расположение,
    0 - горизонтальное расположение
    keypoint - тэг в формате "столбец_строка"
    """

    def __init__(self, length, orientation, keypoint):
        # массив со статусами точек корабля
        self.status_map = []
        # массив с точками вокруг корабля
        self.around_map = []
        # массив с координатами точек корабля
        self.coord_map = []
        # статус гибели корабля
        self.death = 0
        # длина корабля
        self.length = length
        self.orientation = orientation
        self.prefix = keypoint.split("_")[0]
        self.row = int(keypoint.split("_")[1])
        self.column = int(keypoint.split("_")[2])
        self._initialize_components()

    def _initialize_components(self):
        self._generation_ship()
        self._find_point_around()

    def _generation_ship(self):
        """Генерирует точки для корабля"""
        row = self.row
        column = self.column
        orientation = self.orientation
        prefix = self.prefix + "_"
        for i in range(self.length):
            self.status_map.append(0)
            if orientation:
                if column + self.length <= 10:
                    self.coord_map.append(prefix + str(row) + "_" + str(column + i))
                else:
                    self.coord_map.append(prefix + str(row) + "_" + str(column - i))
            else:
                if row + self.length <= 10:
                    self.coord_map.append(prefix + str(row + i) + "_" + str(column))
                else:
                    self.coord_map.append(prefix + str(row - i) + "_" + str(column))
        return self.coord_map

    def _find_point_around(self):
        """Определяет точки, которые находятся вокруг корабля"""
        for point in self.coord_map:
            tx = int(point.split("_")[1])
            ty = int(point.split("_")[2])
            for rx in range(tx - 1, tx + 2):
                for ry in range(ty - 1, ty + 2):
                    if 1 <= rx <= 10 and 1 <= ry <= 10:
                        tag = self.prefix + "_" + str(rx) + "_" + str(ry)
                        if all([not (tag in self.around_map),
                                not (tag in self.coord_map)]):
                            self.around_map.append(tag)

    def shoot(self, shootpoint):
        """Определить номер точки и изменить ее статус
        Пока не понятно как реализована проверка, стрельбы по
        определенной точке"""
        for point in range(len(self.coord_map)):
            if self.coord_map[point] == shootpoint:
                self.status_map[point] = 1
            # если нет нулей в status_map, значит корабль убит
            if not (0 in self.status_map):
                self.death = 1
                # print(self.death)


if __name__ == '__main__':
    a = Ship(4, 1, ship_point)
    # a._generation_ship()
    # a._find_point_around()
    print(a.status_map)
    print(a.coord_map)
    print(a.around_map)
    print(a.shoot(shootpoint))
