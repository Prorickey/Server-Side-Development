from typing import Any
from .minesweeper import MineSweeper

"""
    Wrapper which handles all server-side events for the Minesweeper Game
"""
class ServerMineSweeper:
    def __init__(self, startupOptions: dict[str, int]):
        """
            Creates a Minesweeper Game

            Required startupOptions:
                rows - (int) number of rows in the game
                cols - {int} number of columns in the game

            Raises:
                Exception if a required startupOption is missing
        """

        if 'rows' not in startupOptions:
            raise Exception('Missing rows required option')
        if 'cols' not in startupOptions:
            raise Exception('Missing cols required option')
        
        try:
            rows = int(startupOptions['rows'])
            cols = int(startupOptions['cols'])
        except:
            raise Exception('Required options rows and cols must be integers')

        self.gameLogic = MineSweeper(rows, cols)


    def action(self, actionOptions: dict[str, Any]) -> dict[str, Any]:
        """
            Handles all server actions for the game

            Args:
                actionOptions - a dictionary with the following keys:
                    action - (str) name of the action to take
                    data - {dict} options for the action
            Returns:
                dictionary with the data to return to the client
            
            Actions Allowed:
                board - Get the board status of the game
                pick - pick a space within the board
                space - the status of a space on the board
                name - the name of the player playing the game
                time - the current time counter of the game

            Action Options:
                board - None
                pick - row {int; required}, col {int; required}, flag {bool; optional(False)}
                space - row {int; required}, col {int; required}
                name - None
                time - None

            Action Returns:
                board - board {dict[tuple,int]}, size {str; [row,col]}, 
                        gameOver{int; -1 = Loss, 1 = win, 0 = keep playing},
                        score {int}, time {float}
                pick - score {int}, gameOver {int}, space {int; result value}
                space - space {int; result value}
                time - time {float}
                name - name {str}

            Raises:
                Exception if a required action option is missing
        """

        if 'action' not in actionOptions:
            raise Exception('Required action not provided')
        if 'data' not in actionOptions:
            raise Exception('Required action data not provided')

        action = actionOptions['action']
        data = actionOptions['data']

        rtnData = dict()
        if action == 'board':
            board = dict()
            for row in range(self.gameLogic.rows):
                for col in range(self.gameLogic.cols):
                    board[ f'({row},{col})'] = self.gameLogic.getSpace(row,col)
            
            rtnData = {
                'board' : board,
                'size' : f'[{self.gameLogic.rows},{self.gameLogic.cols}]',
                'gameOver' : self.gameLogic.gameOver,
                'score' : self.gameLogic.score,
                'time' : self.gameLogic.time
            }
        elif action == 'name':
            rtnData = {
                'name' : self.gameLogic.name
            }
        elif action == 'pick':
            if 'row' not in data or 'col' not in data:
                raise Exception(f'Action {action}: Missing options \'row\' or \'col\'')
            
            flag = False
            if 'flag' in data:
                try:
                    flag = bool(data['flag'])
                except:
                    raise Exception(f'Action {action}: Option \'flag\' must be a boolean')

            try:
                row = int(data['row'])
                col = int(data['col'])
            except:
                raise Exception(f'Action {action}: \'row\' and \'col\' must be integers')

            rtn = self.gameLogic.pickSpace(row, col, flag)
            rtnData:dict[str, Any] = {
                'score' : self.gameLogic.score,
                'gameOver' : self.gameLogic.gameOver,
                'space' : self.gameLogic.getSpace(row, col)
            }

            if rtn:
                rtnData['_announce_'] = {
                    'row': row,
                    'col': col,
                    'flag': flag
                }
        elif action == 'space':
            if 'row' not in actionOptions or 'col' not in actionOptions:
                raise Exception(f'Action {action}: Missing options \'row\' or \'col\'')
            try:
                row = int(actionOptions['row'])
                col = int(actionOptions['col'])
            except:
                raise Exception(f'Action {action}: \'row\' and \'col\' must be integers')

            rtnData = {
                'space': self.gameLogic.getSpace(row, col)
            }
        elif action == 'time':
            rtnData = {
                'time' : self.gameLogic.time
            }
        else:
            raise Exception(f'{action} is not a valid action')

        return rtnData

    @property
    def actions(self) -> set[str]:
        """
            Valid actions for this Game

            Returns:
                set of valid actions
        """
        rtn = set(['board', 'pick', 'time', 'space', 'score', 'name'])
        return rtn