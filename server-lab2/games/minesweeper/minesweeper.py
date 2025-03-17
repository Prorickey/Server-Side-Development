import random
import time

class MineSweeper:
    '''
    The Public Interface is not allowed to change!
    Make sure you add a JSDoc comment to every non-private method or attribute
    '''
    
    # Static value modifiers
    __COVERED_ZERO = -10
    __FLAG_MOD = 10
    __PERCENT_CHANCE_MINE = 20

    __OPEN = -1
    @property
    def OPEN():
        '''
        @return {int} value representing a selectable space
        '''
        
        return MineSweeper.__OPEN

    __FLAG = -2
    @property
    def FLAG():
        '''
        @return {int} value representing a flag placemnt
        '''
        return MineSweeper.__FLAG

    __MINE = 9
    @property
    def MINE():
        '''Returns an integer value representing a mine.'''
        return MineSweeper.__MINE

    def __init__(self, rows, cols):
        '''
        Create a populating MineSweeper board
        @param rows number of rows in the game
        @param cols number of columns in the game
        '''
        
        self.__numMines = 0
        self.__startTime = 0
        self.__gameOver = 0

        self.__board = []
        '''
        2D list
        0-8: uncovered number of mines around space
        9: uncovered mine
        negative: covered equivalent
        -10: covered zero
        < -10: flagged equivalent of negative
        '''

        for row in range(rows):
            r = []
            for col in range(cols):
                r.append(0)
            
            self.__board.append(r)
        

        self.__resetBoard()
    
    def __resetBoard(self):

        self.__score = self.rows*self.cols
        
        # Reset the board to zeros
        for row in range(self.rows):
            for col in range(self.cols):
                self.__board[row][col] = 0

        # Place mines and calculate board spaces
        for row in range(self.rows):
            for col in range(self.cols):
                isMine = random.randint(0, 100) < self.__PERCENT_CHANCE_MINE
                if isMine:
                    self.__board[row][col] = -self.__MINE
                    self.__numMines += 1

                    # Deduct one from adjacent spaces
                    for r in range(row-1, row+1):
                        for c in range(col-1, col+1):

                            if r >= 0 and r < self.rows and c >= 0 and c < self.cols:
                                if self.__board[r][c] != -self.__MINE:
                                    self.__board[r][c] -= 1
        
        # Set zeros to their covered values
        for row in range(self.rows):
            for col in range(self.cols):
                if self.__board[row][col] == 0:
                    self.__board[row][col] = MineSweeper.__COVERED_ZERO


    def pickSpace(self, row, col, toggleFlag = False):
        '''
        Picks a space and enforces rules of MineSweeper
        
        @param {int} row row to select (start at zero)
        @param {int} col column to select (start at zero)
        @param {bool} toogleFlag true to toggle a flag placement
        @return {boolean} true if the move was valid, false otherwise
        '''
        
        if self.__gameOver != None:
            return False
        
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False


        # Already picked
        if self.__board[row][col] >= 0:
            return False

        # Toggle the Flag
        if toggleFlag:
            mod = -MineSweeper.__FLAG_MOD
            if self.__board[row][col] < mod:
                mod *= -1
            
            self.__board[row][col] += mod;                        
            return True
    

        # Flagged spaces cannot be picked
        if self.__board[row][col] < -MineSweeper.__FLAG_MOD:
            return False


        self.__uncoverSpace(row, col)
        self.__score -= 1

        if self.__board[row][col] == 0:
            # Hit a zero, uncover the spaces around self one
            for r in range(row-1, row+1):
                for c in range(col-1, col+1):
                    self.pickSpace(r,c)
                
        elif self.__board[row][col] == self.__MINE:
            # Losing Free the score and time taken
            self.__gameOver = -1
            self.__startTime = -1*self.time

        
        # Winning!
        if self.__score == self.__numMines:
            self.__gameOver = 1
            self.__startTime = -1*self.time
        
    def __uncoverSpace(self, row, col):
        if self.__board[row][col] >= 0:
            return self.__board[row][col]

        # Remove the flag
        if self.__board[row][col] < -MineSweeper.__FLAG_MOD:
            self.__board[row][col] += MineSweeper.__FLAG_MOD

        # Uncover the space
        if self.__board[row][col] < 0:
            self.__board[row][col] *= -1

        # Set the zero properly
        if self.__board[row][col] == -MineSweeper.__COVERED_ZERO:
            self.__board[row][col] = 0
        
        return self.__board[row][col]

    def getSpace(self, row, col):
        '''
        Get the status of a space
        @param {int} row the row to query (starting at zero)
        @param {int} col the column to query (starting at zero)
        @return {int} value at (row,col) if uncovered, OPEN if covered or invalid
        '''

        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return self.OPEN

        # Game's Over... uncover the space!
        if self.gameOver:
            self.__uncoverSpace(row, col)
            return self.__board[row][col]

        if self.__board[row][col] < -MineSweeper.__FLAG_MOD:
            return self.FLAG
        

        if self.__board[row][col] < 0:
            return self.OPEN

        return self.__board[row][col]

    def startGame(self):
        '''Begins the game'''
        self.__startTime = round(time.time() * 1000)

    @property
    def cols(self):
        '''Returns an integer representing the number of columsn.'''
        return len(self.__board[0])

    @property
    def rows(self):
        '''Returns an integer that represents the number of rows.'''
        return len(self.__board)

    @property
    def gameOver(self):
        '''
        The game over status of the game
        @return {int} negative if loss, positive if win, zero otherwise
        '''

        return self.__gameOver

    @property
    def score(self):
        '''@return {number} the calculated score of the game'''
        return self.__score

    @property
    def time(self):
        '''@return {int} seconds which have passed in the game'''
        if self.__startTime <= 0:
            return abs(self.__startTime)

        return round(time.time() * 1000) - self.__startTime

    @property
    def name():
        '''Returns the name of the player as a string'''

    @name.setter
    def name(self, n):
        '''Sets the name of the player'''

    def printBoard(self):
        for row in self.__board:
            print(row)

    def get_board(self):
        '''Returns the board as a dictionary'''

        board = dict()
        for row in range(self.rows):
            for col in range(self.cols):
                board[f"{row},{col}"] = self.getSpace(row, col)

        return board

if __name__ == '__main__':
    game = MineSweeper(5, 5)
    game.pickSpace(1,1)
    game.printBoard()
    print(game.gameOver)