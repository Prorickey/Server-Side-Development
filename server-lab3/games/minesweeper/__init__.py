from .minesweeper import MineSweeper

def name():
    return "MineSweeper"

def factory(rows, cols):
    return MineSweeper(rows, cols)