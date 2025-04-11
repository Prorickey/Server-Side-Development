from typing import Any
from .reversi import Reversi

import logging
"""
    Wrapper which handles all server-side events for the Minesweeper Game
"""
class ServerReversi:
    def __init__(self, startupOptions):
        """
            Creates a Reversi Game

            Required startupOptions:
                None
            Raises:
                Exception if a required startupOption is missing
        """
        self.__gameLogic = Reversi()


    def action(self, actionOptions):
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
                player - change the status of a player

            Action Options:
                board - None
                pick - row {int; required}, col {int; required}
                space - row {int; required}, col {int; required}
                player -  change {str (join,leave); required}, spot (int; required), name {str; required;}

            Action Returns:
                board - board {dict[tuple,int]}, size {str; [row,col]}, 
                        gameOver{int; -1 = Player 1 Wins, 1 = Player 2 Wins, 0 = keep playing},
                        score {list[int]; (Player 1, Player 2)}
                pick - score {int}, gameOver {int}, space {dict[tuples, value]; spaces that change}, turn {int; whose turn it is}
                space - space {int; result value}
                player - change {str (join,leave)}, spot {int}, name {str}

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
            for row in range(self.__gameLogic.rows):
                for col in range(self.__gameLogic.cols):
                    board[ f'({row},{col})'] = self.__gameLogic.getSpace(row,col)
            
            rtnData = {
                'board' : board,
                'turn' : self.__gameLogic.turn,
                'gameOver' : self.__gameLogic.gameOver,
                'score' : self.__gameLogic.score, 
                'names' : self.__gameLogic.names
            }
        elif action == 'pick':
            if 'row' not in data or 'col' not in data:
                raise Exception(f'Action {action}: Missing options \'row\' or \'col\'')
            
            try:
                row = int(data['row'])
                col = int(data['col'])
            except:
                raise Exception(f'Action {action}: \'row\' and \'col\' must be integers')

            rtn = self.__gameLogic.pickSpace(row, col)

            # Convert tuples to strings so that they can be sent over network
            convert = dict()
            for [key,value] in rtn.items():
                k = f'({key[0]},{key[1]})'
                convert[k] = value

            rtnData:dict[str, Any] = {
                'score' : self.__gameLogic.score,
                'gameOver' : self.__gameLogic.gameOver,
                'spaces' : convert,
                'turn': self.__gameLogic.turn,
                'scores': self.__gameLogic.score
            }

            if len(rtn) > 0:
                # We annouce picks
                rtnData['_announce_'] = {
                    'row': row,
                    'col': col
                }
        elif action == 'player':
            requiredFields = ['change', 'spot', 'name']
            for field in requiredFields:
                if field not in data:
                    raise Exception(f'Action {action}: Missing required option - {field}')
                
            name = data['name']
            if data['change'] == 'leave':
                name = None

            spot = data['spot']
            
            if spot == 'player1':
                spot = Reversi.PLAYER_1()
            elif spot == 'player2':
                spot = Reversi.PLAYER_2()
            else:
                raise Exception(f'Action {action}: Invalid player - {spot}')
            
            rtn = self.__gameLogic.changePlayer(spot, name)
            if rtn == False:
                raise Exception(f'Action{action}: Player spot is filled')
            
            rtnData = {
                'change': data['change'],
                'spot' : spot,
                'name' : name
            }
            rtnData['_announce_'] = rtnData

        elif action == 'space':
            if 'row' not in actionOptions or 'col' not in actionOptions:
                raise Exception(f'Action {action}: Missing options \'row\' or \'col\'')
            try:
                row = int(actionOptions['row'])
                col = int(actionOptions['col'])
            except:
                raise Exception(f'Action {action}: \'row\' and \'col\' must be integers')

            rtnData = {
                'space': self.__gameLogic.getSpace(row, col)
            }
        else:
            raise Exception(f'{action} is not a valid action')

        return rtnData

    @property
    def actions(self):
        """
            Valid actions for this Game

            Returns:
                set of valid actions
        """
        rtn = set(['board', 'pick', 'space', 'score'])
        return rtn
    
if __name__ == '__main__':
    wrapper = ServerReversi({})
    rtn = wrapper.action({
        'action': 'pick',
        'data': {
            'row': 3,
            'col': 5
        }
    })

