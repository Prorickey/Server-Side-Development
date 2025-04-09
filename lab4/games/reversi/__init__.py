from .reversi import Reversi
from .serverwrapper import ServerReversi
from .blueprint import ReversiBlueprint
from typing import Any

def name():
    """
        Provides the name of this Game Module
            
        Returns:
            the name of the Game Module
    """
    return "reversi"

def blueprint():
    """
        Provides the Flask Blueprint for the Minesweeper Game Module

        Returns:
            the flask blueprint
    """
    return ReversiBlueprint

def factory():
    """
        Provides Creation Factory for this Game Module
        All Game Factory constructors take a dictionary of creation options
        
        If a required creation option is missing, then the constructor raises
        an Exception

        Returns:
            the Factory for this Game Module
    """
    return ServerReversi