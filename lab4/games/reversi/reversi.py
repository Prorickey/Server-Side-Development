'''
    Defines the rules for Reversi

    Note: Passing has not been implemented
'''

class Reversi:
    
    @staticmethod
    def PLAYER_1():
        return -1
    
    @staticmethod
    def PLAYER_2():
        return 1
    
    @staticmethod
    def OPEN():
        return 0

    def __init__(self, rows = 8, cols = 8):
        '''
            Creates a Reversi Game

            Args:
                {int} rows - number of rows in the game (default: 8)
                {int} cols - number of columns in the game (default: 8)
        '''
        self.__board: dict[tuple[int,int], int] = dict()
        self.__rows:int = rows
        self.__cols:int = cols

        self.__scores: dict[int,int] = {
            Reversi.PLAYER_1() : 2,
            Reversi.PLAYER_2() : 2
        }

        self.__turn:int = Reversi.PLAYER_1()
        self.__gameOver:int = 0

        self.__names: dict[int,str] = dict()

        self.__board[ (3,3) ] = Reversi.PLAYER_1()
        self.__board[ (4,4) ] = Reversi.PLAYER_1()
        self.__board[ (3,4) ] = Reversi.PLAYER_2()
        self.__board[ (4,3) ] = Reversi.PLAYER_2()
        

    def getSpace(self, row:int, col:int) -> int:
        '''
            Gets who owns a space (PLAYER_1, PLAYER_2, or OPEN)

            Args:
                {int} row - the row of the selected space
                {int} col - the column of the selected space

            Returns:
                the player who owns the space (PLAYER_1, PLAYER_2, or OPEN)
        '''
        if (row,col) in self.__board:
            return self.__board[ (row, col) ]
        return Reversi.OPEN()
    
    def changePlayer(self, spot:int, name:str|None) -> bool:
        '''
            Changes the status of a player

            Args:
                spot - the spot to change
                name - the name of the player, None causes the player to be removed

            Returns:
                True on success, False otherwise (generally the spot is already taken)
        '''
        player = Reversi.PLAYER_1()
        if( spot != player):
            player = Reversi.PLAYER_2()

        status = True
        if name == None:
            if player in self.__names:
                del self.__names[player]
        elif player not in self.__names:
            self.__names[player] = name
        else:
            status = False
    
        return status


    def pickSpace(self, row:int, col:int) -> dict[tuple[int,int], int]:
        '''
            Picks a spot in the game. On success, the game board changes per the rules
            of Reversi and the turn changes.

            Args:
                {int} row - the row to of the selected space
                {int} col - the colimn of the selected space
            
            Returns:
                A dictionary contains all the spot that change as a result of the move and
                the resulting value. If the move is invalid, the dictionary is empty
        '''
        spacesChanged = dict()

        try:
            row = int(row)
            col = int(col)
        except:
            return spacesChanged
        
        if (row,col) in self.__board:
            return spacesChanged
        self.__board[ (row,col) ] = self.__turn
        spacesChanged[(row,col)] = self.__turn

        directions = [
            (-1, 1), (-1,0), (-1,-1), (0, 1), (0, -1), (1,1), (1, 0), (1,-1)
        ]
        for dir in directions:
            endRow = row + dir[0]
            endCol = col + dir[1]

            capped = False
            placed = self.__turn
            
            while endRow < self.rows and endCol < self.cols and endRow >= 0 and endCol >= 0:
                
                # Open space ends line
                if (endRow, endCol) not in self.__board:
                    break

                # Found end element
                rowDiff = abs(row-endRow)
                colDiff = abs(col-endCol)
                if placed == self.__board[ (endRow, endCol) ]:
                    if rowDiff > 1 or colDiff > 1:
                        capped = True
                    break
                endRow += dir[0]
                endCol += dir[1]

            changeRow = row
            changeCol = col
            if capped:
                while changeRow != endRow-dir[0] or changeCol != endCol-dir[1]:
                    
                    changeRow += dir[0]
                    changeCol += dir[1]

                    self.__scores[ placed ] += 1
                    self.__scores[ placed * -1 ] -= 1
                    spacesChanged[ (changeRow,changeCol) ] = placed

        # No valid lines, so the move isn't valid
        if len(spacesChanged) == 1:
            del self.__board[ (row,col) ]
            spacesChanged.clear()
        else:
            self.__scores[ self.__turn ] += 1 # Count the piece just played
            self.__turn *= -1

        for [space, value] in spacesChanged.items():
            self.__board[space] = value

        # The game is over
        if len(self.__board) == self.rows*self.cols:
            self.__gameOver = True

        return spacesChanged

    @property
    def names(self) -> dict[int,str]:
        '''
            Returns:
                the player spots related to their names
        '''
        return self.__names

    @property
    def rows(self) -> int:
        '''
            Returns:
                {int} the number of rows in the game
        '''
        return self.__rows
    @property
    def cols(self) -> int:
        '''
            Returns:
                {int} the number of columns in the game
        '''
        return self.__cols
    @property
    def turn(self) -> int:
        '''
            Returns:
                {int} Whose turn it is (-1=Player 1, 1=Player 2)
        '''
        return self.__turn
    @property
    def gameOver(self) -> int:
        '''
            Returns:
                the status of the game (-1=Player 1 wins, 1=Player 2 wins, 0=Keep going)
        '''
        return self.__gameOver
    
    @property
    def score(self) -> dict[int,int]:
        '''
            Returns:
                {dict[int,int]} Player ID -> score
        '''
        return {
            Reversi.PLAYER_1() : self.__scores[Reversi.PLAYER_1()],
            Reversi.PLAYER_2() : self.__scores[Reversi.PLAYER_2()]
        }
    
    def printBoard(self):
        print(self.__board)

if __name__ == '__main__':
    game = Reversi()
    game.pickSpace(1,1)
    game.printBoard()
    game.changePlayer(Reversi.PLAYER_1(), "Bob")