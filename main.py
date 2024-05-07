import re
import random
from itertools import islice
import sys 

BLACK = '1'
WHITE = '2'
EMPTY = '0'
WIN_CONDITION = 5

class RenjuGame:
    def __init__(self, size=19):
        self.size = size
        self.board = [['0' for _ in range(size)] for _ in range(size)]
        self.current_player = BLACK
        self.winner = None
        self.leftmost = ()

    def print_board(self, file):
        for row in self.board:
            print(re.sub(r'[\[\]\'\,]', '', str(row)), file=file)
        print('\n', file=file)

    def make_move(self, row, col):
        if self.board[row][col] == EMPTY:
            self.board[row][col] = self.current_player
            win = self.check_win(row, col)
            if win:
                self.winner = self.current_player
                return win
            self.current_player = BLACK if self.current_player == WHITE else WHITE
        
        return False

    def check_win(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for direction_row, direction_col in directions:
            count = 1  
            count += self.count_in_direction(row, col, direction_row, direction_col)
            count += self.count_in_direction(row, col, -direction_row, -direction_col)
            if count == WIN_CONDITION:
                if direction_row == 1 and direction_col == -1:
                    self.find_leftmost(row, col, direction_row, direction_col)
                else:
                    self.find_leftmost(row, col, -direction_row, -direction_col)
                return True
        
        return False

    def find_leftmost(self, row, col, direction_row, direction_col):
        row_move, col_move = row + direction_row, col + direction_col
        while 0 <= row_move < self.size and 0 <= col_move < self.size and self.board[row_move][col_move] == self.current_player:
            row_move += direction_row
            col_move += direction_col
        self.leftmost = (row_move-direction_row+1,col_move-direction_col+1)

    def count_in_direction(self, row, col, direction_row, direction_col):
        row_move, col_move = row + direction_row, col + direction_col
        count = 0
        while 0 <= row_move < self.size and 0 <= col_move < self.size and self.board[row_move][col_move] == self.current_player:
            count += 1
            row_move += direction_row
            col_move += direction_col
        return count

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == EMPTY:
                    return False
        return True

    def play_random_game(self):
        while not self.winner and not self.is_full():
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            win = self.make_move(row, col)
            if win:
                return self.winner
        return self.winner
    
    def scan_from_test(self, board):
        self.board = board
        for row in range(self.size):
            for col in range(self.size):
                if int(self.board[row][col]) != 0:
                    self.current_player = self.board[row][col]
                    win = self.check_win(row, col)
                    if win:
                        self.winner = self.board[row][col]
                        return self.winner
                    self.current_player = BLACK if self.current_player == WHITE else WHITE
                    
        return self.winner


n_args = len(sys.argv)
if n_args > 2:
    raise ValueError("Too many arguments")
else:
    if sys.argv[1] == 'test':
        result_file = open('output.txt', 'w')

        n = 0
        with open('input.txt', 'r') as fin:
            n = int(fin.readline())
            while n > 0:
                board = []
                line = fin.readline()
                if not line == '\n' and len(line) > 1:
                    board.append(line.replace('\n', '').split(' '))
                    for row in islice(fin, 18):
                        row = row.replace('\n', '').split(' ')
                        board.append(row)
                    game = RenjuGame()
                    winner = game.scan_from_test(board)
                    if winner:
                        print(f"{winner}", file=result_file)
                        print(re.sub(r'[\(\)\,]', '', str(game.leftmost)), file=result_file)
                    else:
                        print("0", file=result_file)
                    n -= 1
        result_file.close()
    
    elif sys.argv[1] == 'generate':
        try:
            n = int(input('Enter number of tests to generate: '))
            result_file =  open('input.txt', 'w')
            print(n, file=result_file)
            while n > 0:
                game = RenjuGame()
                winner = game.play_random_game()
                game.print_board(file=result_file)
                n -= 1
            result_file.close()
        except ValueError as e:
            print(e, file=sys.stderr)
    else:
        raise ValueError("Illegal argument")