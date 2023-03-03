# -*- coding: utf-8 -*-
import clr

clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import (Form, Button, FlatStyle, Label, TextRenderer,
                                  FormBorderStyle, MenuStrip, ToolStripMenuItem, ToolStripControlHost)

clr.AddReference('System.Drawing')
from System.Drawing import Size, Point, Color, Pens, Pen, Brushes


import sys
sys.path += [
    r'c:\sea_battle\IronPython\view'
]


from cell import Cell
# from field import Field


class GameWindow(Form):
    def __init__(self):
        self.Text = "Морской бой"
        self.CenterToScreen()
        self.FormBorderStyle = FormBorderStyle.Fixed3D
        self._cell_side = 30
        self._cell_size = Size(self._cell_side, self._cell_side)
        self._map_size = 11
        self.first = []
        self.second = []
        self._indent_top = 50
        self._indent_lr = 10
        self._indent_bottom = 10
        self._indent_middle = 10
        self._symbols = "АBCDEFGHIJ"
        self.ClientSize = self._generate_window_size(self._map_size, self._map_size)
        self._initialize_components()


    def _initialize_components(self):
        self._generate_menu_strip()
        self._create_first_buttons()
        self._create_second_buttons()

        self.map1 = Label()
        self.map1.Parent = self
        self.map1.Text = 'Карта игрока'
        self.map1.Location = Point(10, 30)

        self.map2 = Label()
        self.map2.Parent = self
        self.map2.Text = 'Карта противника'
        self.map2.Location = Point(self._indent_lr + self._map_size * self._cell_side + self._indent_middle, 30)

        self._result = Label()
        self._result.Parent = self
        self._result.Text = ''
        self._result.Size = TextRenderer.MeasureText(self._result.Text, self._result.DefaultFont)
        self._result.Location = Point(round(self.Size.Width/2) - self._cell_side * 4, 30)

    def _generate_menu_strip(self):
        menu_strip = MenuStrip()
        menu_strip.Parent = self

        file_item = ToolStripMenuItem('Файл')
        menu_strip.Items.Add(file_item)

        self._new_game = ToolStripMenuItem('Новая игра')
        self._new_game.Click += self._on_new_game_click
        file_item.DropDownItems.Add(self._new_game)

        self._exit = ToolStripMenuItem('Выход')
        self._exit.Click += self._exit_game
        file_item.DropDownItems.Add(self._exit)

        self._new_game_handlers = []

    def _generate_window_size(self, rows, columns):
        width = 2 * columns * self._cell_side + 2 * self._indent_lr + self._indent_middle
        height = self._indent_top + rows * self._cell_side + self._indent_bottom
        return Size(width, height)

    def set_final_message(self, message):
        self._result.Text = message
        self._result.Size = TextRenderer.MeasureText(self._result.Text, self._result.DefaultFont)
        self._result.Location = Point(round(self.Size.Width/2) - self._cell_side * 4, 30)
        self._result.Refresh()

    def _create_first_buttons(self):
        for x in range(self._map_size):
            row = []
            for y in range(self._map_size):
                cell = Cell(x, y)
                cell.Parent = self
                cell.Size = self._cell_size
                cell.Location = Point(self._indent_lr + x * self._cell_side,
                                      self._indent_top + y * self._cell_side)
                if x == 0 or y == 0:
                    cell.BackColor = Color.Gray
                    if x == 0 and y > 0:
                        cell.Text = self._symbols[y - 1]
                    if y == 0 and x > 0:
                        cell.Text = str(x)
                row.append(cell)
            self.first.append(row)

    def _create_second_buttons(self):
        for x in range(self._map_size):
            row = []
            for y in range(self._map_size):
                cell = Cell(x, y)
                if x == 0 or y == 0:
                    cell.BackColor = Color.Gray
                    if x == 0 and y > 0:
                        cell.Text = self._symbols[y - 1]
                    if y == 0 and x > 0:
                        cell.Text = str(x)
                cell.Parent = self
                cell.Size = self._cell_size
                cell.Location = Point(self._indent_lr + (x + self._map_size) * self._cell_side + self._indent_middle,
                                      self._indent_top + y * self._cell_side)
                row.append(cell)
            self.second.append(row)

    def set_cell_start_handler(self, handler):
        self._button_start.Click += handler

    def _exit_game(self, sender, args):
        self.Close()

    def set_cell_click_handler_second(self, handler):
        for row in self.second:
            for cell in row:
                cell.Click += handler

    def add_handler_new_game_buttons(self, handler):
        self._new_game_handlers.append(handler)

    def _on_new_game_click(self, sender, args):
        for handler in self._new_game_handlers:
            handler(self, sender)

    # Чтобы вызвать, например print f[3]
    def __getitem__(self, index):
        return self.first[index]


if __name__ == '__main__':
    f = GameWindow()
    f.ShowDialog()
