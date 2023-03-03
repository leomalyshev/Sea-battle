# -*- coding: utf-8 -*-
import sys
import os
try:
    main_dir_path = os.path.dirname(os.path.dirname(__file__))
except Exception as e:
    main_dir_path = r'c:\sea_battle'
sys.path.append(os.path.join(main_dir_path, 'IronPython'))
from presenter.game import Game

__window__.Close()
game = Game()
game.start()
