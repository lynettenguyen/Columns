### columns_ui.py ###

import columns_logic

def main_program() -> None:
    '''Allows a user to play the game columns'''
    game = columns_logic.ColumnsLogic()
    type_of_board = str(input())

    if type_of_board == 'EMPTY':
        columns_logic.printed_board(game.GameState)
    if type_of_board == 'CONTENTS':
        columns_logic.printed_board(columns_logic.contents(game.GameState))
        matches = 0
        while True:
            for x in range(game.BoardColumn):
                for y in range(game.BoardRow-1):
                    if game.find_matching_jewels(1+x, game.BoardRow-(y+1)) != None: #hardcode
                        matches += 1
            if matches == 0:
                break
            else:
                columns_logic.printed_board(game.GameState)
                game.del_matched_jewels()
                columns_logic.printed_board(game.GameState)
                matches = 0
                
    while True:
        user_input = str(input())
        user_input = user_input.split()
        command = user_input[0]
        try: 
            if command == 'F':
                column_drop = user_input[1]
                jewels = ''
                for jewel in user_input[2:]:
                    jewels += jewel
                game.create_jewels(jewels)
                game.column_drop(column_drop)
                columns_logic.printed_board(game.drop_jewels())
                next_move = str(input())
                while True:
                    if next_move == 'Q':
                        command = 'Q'
                        break
                    elif next_move == '':
                        columns_logic.printed_board(game.drop_jewels())
                        next_move = str(input())
                    elif next_move in '><':
                        columns_logic.printed_board(game.shift_jewels(next_move))
                        next_move = str(input())
                    elif next_move == 'R':
                        columns_logic.printed_board(game.rotate_jewels())
                        next_move = str(input())
                        
                    if game.Dropped == True:
                        game.freeze_jewels()
                        
                    if game.Frozen == True:
                        game.Frozen = False
                        columns_logic.printed_board(game.GameState)
                        matches = 0
                        while True:
                            for x in range(game.BoardColumn):
                                for y in range(game.BoardRow-1):
                                    if game.find_matching_jewels(1+x, game._ColumnIndex-y) != None:
                                        matches += 1
                            if matches == 0:
                                break
                            else:
                                columns_logic.printed_board(game.GameState)
                                game.del_matched_jewels()
                                columns_logic.printed_board(game.GameState)
                                matches = 0
                                    
                        game.reset_column()
                        break
                                

            if command == 'Q':
                break
        except columns_logic.ColumnFullError:
            print('GAME OVER')
            break
            

if __name__ == '__main__':
    main_program()

        

        
