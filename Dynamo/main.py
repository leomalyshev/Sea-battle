import clr
import sys
sys.path.append(r'c:\Program Files (x86)\IronPython 2.7\Lib')
import os
sys.path.append(
    os.path.join(os.path.dirname(IN[0].DirectoryName), 'IronPython')
)
from presenter.game import Game

game = Game()
game.start()
