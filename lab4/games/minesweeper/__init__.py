'''
This files sets up and loads the MineSweeper game

'''
from .minesweeper import MineSweeper
from .serverwrapper import ServerMineSweeper
from .blueprint import MineSweeperBlueprint
from typing import Any

def name():
    """
        Provides the name of this Game Module
            
        Returns:
            the name of the Game Module
    """
    return "minesweeper"

def blueprint():
    """
        Provides the Flask Blueprint for the Minesweeper Game Module

        Returns:
            the flask blueprint
    """
    return MineSweeperBlueprint

def factory():
    """
        Provides Creation Factory for this Game Module
        All Game Factory constructors take a dictionary of creation options
        
        If a required creation option is missing, then the constructor raises
        an Exception

        Returns:
            the Factory for this Game Module
    """
    return ServerMineSweeper