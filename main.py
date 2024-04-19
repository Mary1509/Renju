import re
import random

class RenjuGame:
    def __init__(self, size=19):
        self.size = size
        self.board = [['0' for _ in range(size)] for _ in range(size)]
        self.current_player = '1'
        self.winner = None
        self.leftmost = ()

    def print_board(self):
        for row in self.board:
            print(re.sub(r'[^\w]', ' ', str(row)))

    def make_move(self, row, col):
        if self.board[row][col] == '0':
            self.board[row][col] = self.current_player
            win, leftmost = self.check_win(row, col)
            if win:
                self.winner = self.current_player
                return win, leftmost
            self.current_player = '1' if self.current_player == '2' else '2'
            return False, None
        else:
            return False, None

    def check_win(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Right, Down, Diagonal, Anti-diagonal
        for dr, dc in directions:
            count = 1  
            count += self.count_in_direction(row, col, dr, dc)
            count += self.count_in_direction(row, col, -dr, -dc)
            if count >= 5:
                print(row+3, col+1)
                print(dr, dc)
                if dr == 1 & dc == -1:
                    self.find_leftmost(row, col, dr, dc)
                else:
                    self.find_leftmost(row, col, -dr, -dc)
                return True, (row - dr * count+1, col - dc * count+1)
        return False, None

    def find_leftmost(self, row, col, dr, dc):
        r, c = row + dr, col + dc
        while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.current_player:
            r += dr
            c += dc
        self.leftmost = (r-dr+3,c-dc+1)

    def count_in_direction(self, row, col, dr, dc):
        r, c = row + dr, col + dc
        count = 0
        while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == self.current_player:
            count += 1
            r += dr
            c += dc
        
        return count

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == '0':
                    return False
        return True

    def play_random_game(self):
        while not self.winner and not self.is_full():
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            win, leftmost = self.make_move(row, col)
            if win:
                return self.winner, leftmost
        return self.winner, None

# Example usage

n = int(input())
while n > 0:
    game = RenjuGame()
    winner, leftmost = game.play_random_game()
    game.print_board()
    if winner:
        print(f"{winner} wins!")
        print(game.leftmost)
    else:
        print("It's a draw!")
    n -= 1
