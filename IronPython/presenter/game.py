# -*- coding: utf-8 -*-
import clr

clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import MouseButtons, MessageBox


clr.AddReference('System.Drawing')
from System.Drawing import Size, Color, SolidBrush, Pen, Pens, Brushes

from view.window import GameWindow
# from model.field import Field
from model.bot import Bot

from view.cell import Cell
from random import randrange
from model.ship import Ship
from time import time
from threading import Thread


import sys
sys.path += [
    r'c:\sea_battle\IronPython\view'
]


class Game(object):
    def __init__(self):
        # класс бота
        self.bot = None
        # время генерации флота
        self._fleet_time = 0
        # окно с кораблями
        self._view = None
        # флот игрока
        self.fleet_user = []
        # флот бота
        self.fleet_bot = []

    def start(self):
        self._view_initialize()
        thread = Thread(target=self._create_ship("enemy"))
        thread.start()
        self._create_ship("my")
        # при старте создаем бота, передаем в него корабля игрока, и ячейки
        self.bot = Bot(self.fleet_user, self._view.first)
        self._view.ShowDialog()

    def _view_initialize(self):
        self._view = GameWindow()
        self._view.add_handler_new_game_buttons(self._new_game)
        self._view.set_cell_click_handler_second(self.change_cell_state_second)

    def _create_ship(self, prefix):
        """Функция генерации кораблей на поле,
        количество сгенерированных кораблей"""
        count_ships = 0
        fleet_array = []
        fleet_ships = []
        while count_ships < 10:
            # палубность корабля (length - палубность корабля)
            for length in reversed(range(1, 5)):
                # генерация необходимого количества кораблей необходимой длины
                for i in range(5 - length):
                    while True:
                        ship_point = prefix + "_" + str(randrange(1, 11)) + "_" + str(randrange(1, 11))
                        orientation = randrange(2)
                        new_ship = Ship(length, orientation, ship_point)
                        intersect_array = list(set(fleet_array) & set(new_ship.coord_map))
                        if len(intersect_array) == 0:
                            fleet_array += new_ship.coord_map + new_ship.around_map
                            fleet_ships.append(new_ship)
                            count_ships += 1
                            break
        # print(prefix,time() - self._fleet_time,"секунд")
        if prefix == "enemy":
            self.fleet_bot = fleet_ships
            # отрисовка кораблей
            # Cell.paint_fleets(fleet_ships, self._view.second)
        else:
            # отрисовка кораблей
            self.fleet_user = fleet_ships
            # Cell.paint_fleets(fleet_ships, self._view.first)

    def check_finish(self):
        count = 0
        for ship in self.fleet_bot:
            count += ship.death
        return count

    def change_cell_state_second(self, cell, args):
        """Стрельба по клеткам противника"""
        hit_status = None
        if cell.x == 0 or cell.y == 0:
            return
        point = "enemy_" + str(cell.x) + "_" + str(cell.y)
        for obj in self.fleet_bot:
            if point in obj.coord_map:
                hit_status = True
                obj.shoot(point)
                if obj.death == 1:
                    for point in obj.around_map:
                        x = int(point.split("_")[1])
                        y = int(point.split("_")[2])
                        neighbro_cell = self._view.second[x][y]
                        neighbro_cell.paint(False)
        if hit_status:
            cell.paint(True)
            self._finish()
        else:
            cell.paint(False)
            self.bot.hit()
            self._finish()

    def _mouse_button_field_second(self, cell, args):
        self.change_cell_state_second(cell)

    def _disabled_cells(self):
        for i in zip(self._view.first, self._view.second):
            for row in i:
                for cell in row:
                    if cell.Enabled:
                        cell.Enabled = False

    def _finish(self):
        print(self.bot.check_finish())
        print(self.check_finish())
        if self.bot.check_finish() >= 10:
            self._view.set_final_message('You Lose!')
            self._disabled_cells()
        if self.check_finish() >= 10:
            self._view.set_final_message('You Win!')
            self._disabled_cells()

    def _new_game(self, sender, event_args):
        """self указывает на то, что функция принадлежит классу Game,
        sender - это GameWindow, event_args - ToolStripMenuItem('Новая игра')"""
        self._hide_previus_game(sender)
        self.start()

    def dispose(self):
        """Для освобождения памяти дескриптора созданных ячеек,
        если их не освободить, то при нажатии "Новая игра" много раз в подряд,
        вылетит ошибка дескриптора окна"""
        for i in zip(self._view.first, self._view.second):
            for row in i:
                for cell in row:
                    cell.Dispose()

    def _hide_previus_game(self, game_window):
        game_window.Hide()
        self.dispose()
        game_window.Close()








