from . import minesweeper
from . import reversi

"""
    Initialize the all Valid Games
"""

games = {
    minesweeper.name() : minesweeper, 
    reversi.name() : reversi
}