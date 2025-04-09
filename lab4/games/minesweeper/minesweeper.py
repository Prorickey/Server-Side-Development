import random
import time

'''
    * 
    * The Public Interface is not allowed to change!
    * Make sure you add a JSDoc comment to every non-private method or attribute
    *
'''
class MineSweeper:
    
    __COVERED_ZERO = -10
    __FLAG_MOD = 10
    __OPEN = -1
    
    @property
    def OPEN(self) -> int:
        '''
            Returns:
                {int} value representing a selectable space   
        '''
        return MineSweeper.__OPEN;

    __FLAG = -2
    @property
    def FLAG(self) -> int:
        '''
            Returns:
                {int} value representing a flag placemnt
        '''
        return MineSweeper.__FLAG

    __MINE = 9
    @property
    def MINE(self) -> int:
        '''
            Returns:
                {int} value representing a mine
        '''
        return MineSweeper.__MINE
    

    def __init__(self, rows:int, cols:int):
        '''
            Create a populating MineSweeper board
            
            Args:
                rows number of rows in the game
                cols number of columns in the game
        '''

        '''
        * 2D list
        * 0-8: uncovered number of mines around space
        * 9: uncovered mine
        * negative: covered equivalent
        * -10: covered zero
        * < -10: flagged equivalent of negative
        '''
        self.__board: list[list[int]] = []            

        self.__startTime:float = time.time()         # ms
        self.__gameOver:int = 0                    # 1 = win, -1 = lose, 0 = keep going
        self.__numMines:int = 0
        
        self.__score:int = 0
        self.__name:str = '' 

        self.__PERCENT_CHANCE_MINE:int = 20
        
        for row in range(rows):    
            r:list[int] = []
            for col in range(cols):
                r.append(0)
            self.__board.append(r)
        self.__resetBoard()

    def __resetBoard(self) -> None:
        self.__score = self.rows*self.cols;
        
        # Reset the board to zeros
        for row in range(self.rows):
            for col in range(self.cols):
                self.__board[row][col] = 0

        # Place mines and calculate board spaces
        for row in range(self.rows):
            for col in range(self.cols):
                isMine = random.random()*100 < self.__PERCENT_CHANCE_MINE
                if( isMine ):
                    self.__board[row][col] = -self.MINE
                    self.__numMines += 1

                    # Deduct one from adjacent spaces
                    for r in range(row-1, row+2):
                        for c in range(col-1, col+2):
                            if( r >= 0 and r < self.rows and c >= 0 and c < self.cols):
                                if( self.__board[r][c] != -self.MINE):
                                    self.__board[r][c] -= 1
                                
        # Set zeros to their covered values
        for row in range(self.rows):
            for col in range(self.cols):
                if( self.__board[row][col] == 0):
                    self.__board[row][col] = MineSweeper.__COVERED_ZERO


    def pickSpace(self, row:int, col:int, toggleFlag:bool = False) -> bool:
        '''
            Picks a space and enforces rules of MineSweeper

            Args:
                {int} row row to select (start at zero)
                {int} col column to select (start at zero)
                {bool} toogleFlag true to toggle a flag placement
            
            Returns:
                {boolean} true if the move was valid, false otherwise
        '''      
        if( self.__gameOver ):
            return False
        
        if(row < 0 or row >= self.rows or col < 0 or col >= self.cols):
            return False

        # Already picked
        if( self.__board[row][col] >= 0 ):
            return False

        # Toggle the Flag
        if( toggleFlag ):
            mod = -MineSweeper.__FLAG_MOD
            if( self.__board[row][col] < mod ):
                mod *= -1

            self.__board[row][col] += mod;                        
            return True

        # Flagged spaces cannot be picked
        if( self.__board[row][col] < -MineSweeper.__FLAG_MOD):
            return False


        self.__uncoverSpace(row, col)
        self.__score -= 1
        if( self.__board[row][col] == 0):
            # Hit a zero, uncover the spaces around self one
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    self.pickSpace(r,c)
        elif( self.__board[row][col] == self.MINE ):
            # Losing Free the score and time taken
            self.__gameOver = -1
            self.__startTime = -1*self.time
        
        # Winning!
        if( self.__score == self.__numMines ):
            self.__gameOver = 1
            self.__startTime = -1*self.time
        
        return True

    def __uncoverSpace(self, row, col):
        if( self.__board[row][col] >= 0 ):
            return self.__board[row][col]

        # Remove the flag
        if(self.__board[row][col] < -MineSweeper.__FLAG_MOD):
            self.__board[row][col] += MineSweeper.__FLAG_MOD

        # Uncover the space
        if(self.__board[row][col] < 0 ):
            self.__board[row][col] *= -1
        
        # Set the zero properly
        if(self.__board[row][col] == -MineSweeper.__COVERED_ZERO):
            self.__board[row][col] = 0

        return self.__board[row][col]

    def getSpace(self, row: int, col: int) -> int:
        '''
            Get the status of a space
            
            Args:
                {int} row the row to query (starting at zero)
                {int} col the column to query (starting at zero)
            
            Returns:
                {int} value at (row,col) if uncovered, OPEN if covered or invalid
        '''

        if( row < 0 or row >= self.rows or col < 0 or col >= self.cols):
            return self.OPEN

        # Game's Over... uncover the space!
        if(self.gameOver):
            self.__uncoverSpace(row, col)
            return self.__board[row][col]

        if( self.__board[row][col] < -MineSweeper.__FLAG_MOD ):
            return self.FLAG

        if( self.__board[row][col] < 0 ):
            return self.OPEN

        return self.__board[row][col]

    def startGame(self) -> None:
        '''
            Begins the game
        '''
        self.__startTime = time.time()

    @property
    def cols(self) -> int :
        '''
            Returns:
                number of columns in the game
        '''
        return len(self.__board[0])

    @property
    def rows(self) -> int:
        '''
            Returns:
                {int} number of rows in the game
        '''
        return len(self.__board)


    @property
    def gameOver(self) -> int:
        '''
            The game over status of the game
            
            Returns:
                {int} negative if loss, positive if win, zero otherwise
        '''
        return self.__gameOver

    @property
    def score(self) -> int:    
        '''
            Returns:
                {number} the calculated score of the game
        '''
        return self.__score

    @property
    def time(self) -> float:
        '''
            Returns:
                {int} seconds which have passed in the game
        '''

        if( self.__startTime < 0 ):
            return abs(self.__startTime)

        return round(time.time() - self.__startTime)

    @property
    def name(self) -> str:
        ''' 
            Returns:
                {string} name of the player
        '''
        return self.__name

    @name.setter
    def name(self, n: str ) -> None:
        '''
            Args:
                {string} n new name of the player
        '''
        pass
    
    def printBoard(self):
        for row in self.__board:
            print(row)


if __name__ == '__main__':
    game = MineSweeper(5,5)
    game.printBoard()
    game.pickSpace(1,1)
    print("\n\n\n\n")
    game.printBoard()
    print(game.gameOver)

