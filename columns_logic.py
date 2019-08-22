### columns_logic.py ###

class ColumnFullError(Exception):
    pass

class ColumnsLogic():

    def __init__(self):
        self.GameState = _new_game_board()
        self.Dropped = False #a bool phrase to indicate whether the string has been dropped
        self.Frozen = False
        self._Jewels = None
        self.BoardRow = len(self.GameState[0])-1
        self.BoardColumn = len(self.GameState)-2
        self._JewelInput = 0 
        self._ColumnIndex = 0
        self._ColumnDrop = 0


    def create_jewels(self, UserInput: str) -> None:
        '''Creates a str of jewels to drop into the board'''
        jewels = []
        jewels.append(UserInput[0])
        jewels.append(UserInput[1])
        jewels.append(UserInput[2])

        self._Jewels = jewels
        self._Dropped = False

    def column_drop(self, num: str) -> None:
        '''Updates the column the jewels will be dropped in'''
        self._ColumnDrop += int(num) 

    def drop_jewels(self) -> 'self.GameState':
        '''Adds a jewel into a specified column one at a time only if the slot below is empty
           or when all three jewels have fallen. Raises a ColumnFullError when the column is
           full before all three jewels are inputed into the board.'''
        jewels = self._Jewels
        column_num = self._ColumnDrop
        if self._JewelInput < 3:
           if self.GameState[column_num][self._ColumnIndex] == 0: 
                for x in range(self._JewelInput+1):
                    self.GameState[column_num][self._ColumnIndex-x] = '[' + str(jewels[2-x]) + ']'
                self._ColumnIndex += 1
                self._JewelInput += 1
                return self.GameState
          
        if self._JewelInput == 3:
            if self.GameState[column_num][self._ColumnIndex] != 0:
                for x in range(self._JewelInput):
                   self.GameState[column_num][self._ColumnIndex-(x+1)] = '|' + str(jewels[2-x]) +'|'
                self._ColumnIndex -= 1
                self.Dropped = True
                return self.GameState 
            elif self._ColumnIndex == self.BoardRow-1:
                for x in range(self._JewelInput):
                    self.GameState[column_num][self._ColumnIndex-x] = '|' + str(jewels[2-x]) +'|'
                self.GameState[column_num][self._ColumnIndex-3] = 0
                self.Dropped = True
                return self.GameState        
            else:
                for x in range(self._JewelInput):
                    self.GameState[column_num][self._ColumnIndex-x] = '[' + str(jewels[2-x]) + ']'
                self.GameState[column_num][self._ColumnIndex-3] = 0
                self._ColumnIndex += 1
                return self.GameState
        else:
            self.Dropped = True
            for x in range(self._JewelInput):
                self.GameState[column_num][self._ColumnIndex-(x+1)] = '|' + str(jewels[2-x]) + '|'
            raise ColumnFullError
            
    

    def shift_jewels(self, sign: str) -> 'self.GameState':
        '''Shifts a jewel either to the left or right. Does not shift the jewels if there is a jewel occupying
           the slot'''
        if self.Dropped == False:
            if sign == '>':
                if self._ColumnDrop != 3 and self.GameState[self._ColumnDrop+1][self._ColumnIndex-1] == 0:
                    for x in range(self._JewelInput):
                        self.GameState[self._ColumnDrop+1][self._ColumnIndex-(1+x)] = self.GameState[self._ColumnDrop][self._ColumnIndex-(1+x)]
                        self.GameState[self._ColumnDrop][self._ColumnIndex-(1+x)] = 0
                    self._ColumnDrop += 1
                return self.GameState
            if sign == '<':
                if self._ColumnDrop != 1 and self.GameState[self._ColumnDrop-1][self._ColumnIndex-1] == 0:
                    for x in range(self._JewelInput):
                        self.GameState[self._ColumnDrop-1][self._ColumnIndex-(1+x)] = self.GameState[self._ColumnDrop][self._ColumnIndex-(1+x)]
                        self.GameState[self._ColumnDrop][self._ColumnIndex-(1+x)] = 0
                    self._ColumnDrop -= 1
                return self.GameState


    def rotate_jewels(self) -> 'self.GameState':
        '''Rotates the order of the jewels but moving the bottom jewel up and the rest down. Can only rotate
           if jewels are falling or before they are frozen'''
        new_jewel_order = []
        new_jewel_order.append(self._Jewels[-1])
        new_jewel_order.append(self._Jewels[0])
        new_jewel_order.append(self._Jewels[1])

        self._Jewels = new_jewel_order
        for x in range(3):
            if self.Dropped == False:
                self.GameState[self._ColumnDrop][self._ColumnIndex-(1+x)] = '[' + str(new_jewel_order[2-x]) + ']'
            if self.Dropped == True:
                self.GameState[self._ColumnDrop][self._ColumnIndex-(1+x)] = '|' + str(new_jewel_order[2-x]) + '|'
        
        return self.GameState


    def freeze_jewels(self) -> 'self.GameState':
        '''After one move is made to a fallen jewel, the jewel is then frozen'''
        if self.Dropped:
            self.Dropped = False
            self.Frozen = True
            for x in range(self._JewelInput):
                self.GameState[self._ColumnDrop][self._ColumnIndex-(x)] = ' '+ str(self._Jewels[2-x]) + ' '
                
            self._JewelInput -= self._JewelInput

        return self.GameState

    def matching_jewels(self, column_num: int, index_num: int, coldelta: int, indelta: int)-> bool:
        '''Returns true if there is a match with the given location of a jewel with a given direction.
           False otherwise'''
        start_cell = self.GameState[column_num][index_num]
        if start_cell != 0:
            matching = 0
            for x in range(1, self.BoardColumn):
                if self._is_a_valid_column_number(column_num + coldelta*x) \
                and self._is_a_valid_index(index_num + indelta*x):
                    if start_cell[1] in str(self.GameState[column_num + coldelta*x][index_num + indelta*x]):
                        matching += 1
                    else:
                        break
                else:
                    break
            if matching >= 2:
                for x in range(matching+1):
                    self.GameState[column_num + coldelta*x][index_num + indelta*x] = \
                    str(self.GameState[column_num + coldelta*x][index_num + indelta*x]).replace(' ', '*')
                return True
            else:
                return False

    def find_matching_jewels(self, col: int, row: int)-> 'self.GameState':
        '''With a given location, checks all 8 directions to find a match. If there is at least
           one match found, it return the GameState'''
        matches = []
        test = [self.matching_jewels(col, row, 0, 1),
                self.matching_jewels(col, row, 1, 1),
                self.matching_jewels(col, row, 1, 0),
                self.matching_jewels(col, row, 1, -1),
                self.matching_jewels(col, row, 0, -1),
                self.matching_jewels(col, row, -1, -1),
                self.matching_jewels(col, row, -1, 0),
                self.matching_jewels(col, row, -1, 1) ]

        for x in test:
            if x:
                matches.append(x)
        if len(matches) == 0:
            return None
        else:
            for test in matches:
                return self.GameState
        
    def del_matched_jewels(self) -> 'self.GameState':
        '''Deletes matched the jewels and shifts jewels above downward'''
        for x in range(len(self.GameState)):
            for y in range(len(self.GameState[x])):
                if '*' in str(self.GameState[x][y]):
                    if y != 0:
                        for z in range(y):
                            self.GameState[x][y-z] = self.GameState[x][y-(z+1)]
                    else:
                        self.GameState[x][y] = 0
        return self.GameState

    def reset_column(self) -> None:
        '''Resets the Column Drop and Column Index number'''
        self._ColumnIndex = 0
        self._ColumnDrop = 0


    def _is_a_valid_column_number(self, column_num: int) -> bool:
        return 1 <= column_num <= self.BoardColumn

    def _is_a_valid_index(self, index_num: int) -> bool:
        return 0 <= index_num <= self.BoardRow

        


            
def _new_game_board() -> [[int]]:
    '''Creates a new board based on the numbers given, num_row must be at least
       4 and num_column must be at least 3. The current board will be comprised
       of the integer 0 which will represent an empty slot'''
    num_row = int(input())
    num_column = int(input())
    board = []
    
    if num_row < 4 or num_column < 3:
        print('Error')
    else:
        for col in range(num_column+2):
            board.append([])
            for row in range(num_row+1):
                board[-1].append(0)

        return board 

def printed_board(board: [[str]]) -> 'user friendly board':
    '''With a given board, creates a copy that is user friendly by
       adding vertical and horizontal lines'''
    new_board = ''
    for col in board:
        col[-1] = '---'
        board[0][-1] = ' '
        board[-1][-1] = ' '
        for x in range(len(col)-1):
            board[0][x] = '|'
            board[-1][x] = '|'
    for x in range(len(col)):
        new_row = ''
        for row in board:
            new_row += str(row[x])
            new_row = new_row.replace('0', '   ')
        new_board += new_row + '\n'
        
    print(new_board, end='')

    
def empty() -> 'board':
    '''Prints out a empty board based on user's board dimensions'''
    printed_board(_new_game_board())

def contents(board: [['int']]) -> 'board': 
    '''Prints out a board based on the user's board dimensions and what contents
       the user wants'''
    for column in board:
        num_row = len(column)-1
    num_column = len(board)-2
    contents = []
    for x in range(num_row):
        contents.append(str(input()))
    for new_row in contents:
        if len(new_row) != num_column:
            print('Error')

    columns = []
    for x in range(num_column):
        content_row = []
        for y in range(len(contents)):
            if contents[y][x] == ' ':
                pass
            else:
                content_row.append(contents[y][x])
        columns.append(content_row)

    for x in range(len(columns)):
        for y in range(1, len(columns[x])+1):
            board[x+1][-(y+1)] = ' '+str(columns[x][-y])+ ' '
    return board



    
    
    


