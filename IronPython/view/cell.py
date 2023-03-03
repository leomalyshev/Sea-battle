# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Button, FlatStyle, MouseButtons, MouseEventArgs
clr.AddReference('System.Drawing')
from System.Drawing import Color, Pen, Brushes


class Cell(Button):
    def __init__(self, x, y):
        self._y = y
        self._x = x
        self.BackColor = Color.White
        self.paint_handlers = []
        self.Enabled = True
        self.is_checked = False

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    def set_value(self, value):
        self.Text = value

    def OnGotFocus(self, *args):
        self.NotifyDefault(False)

    @staticmethod
    def paint_cross(sender, args):
        """Рисует красный крест на ячейке"""
        g = args.Graphics
        my_pen = Pen(Color.Black)
        my_pen.Width = 3
        g.DrawLine(my_pen, 0, 0, 30, 30)
        g.DrawLine(my_pen, 0, 30, 30, 0)
        sender.BackColor = Color.Red

    @staticmethod
    def paint_miss(sender, args):
        """Рисует синий круг на ячейке,
        интересно, можно ли реализовать без PaintEventArgs"""
        g = args.Graphics
        g.FillEllipse(Brushes.Blue, 9, 9, 10, 10)

    def paint(self, hit):
        """Создает событие перекраски ячейки,
        без обновления работает не сразу"""
        if hit:
            self.Paint += self.paint_cross
        else:
            self.Paint += self.paint_miss
        self.Refresh()
        self.Enabled = False
        self.is_checked = True

    @staticmethod
    def paint_fleets(fleet_ships, cells):
        """Отрисовка кораблей на поле боя,
        предназначен для технических целей"""
        for obj in fleet_ships:
            for point in obj.coord_map:
                x = int(point.split("_")[1])
                y = int(point.split("_")[2])
                cells[x][y].BackColor = Color.Red

