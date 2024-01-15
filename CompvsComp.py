from copy import deepcopy
import random


class ConnectFour:
    rows = 6
    columns = 7

    def __init__(self):
        self.board = [[' '] * self.columns for _ in range(self.rows)]

    def check_win(self, symbol):
        # Horizontally
        for row in range(len(self.board)):
            for col in range(len(self.board[0]) - 3):
                if all(self.board[row][col + i] == symbol for i in range(4)):
                    return True

        # Vertically
        for row in range(len(self.board) - 3):
            for col in range(len(self.board[0])):
                if all(self.board[row + i][col] == symbol for i in range(4)):
                    return True

        # Diagonally in \ direction
        for row in range(len(self.board) - 3):
            for col in range(len(self.board[0]) - 3):
                if all(self.board[row + i][col + i] == symbol for i in range(4)):
                    return True

        # Diagonally in / direction
        for row in range(len(self.board) - 3):
            for col in range(3, len(self.board[0])):
                if all(self.board[row + i][col - i] == symbol for i in range(4)):
                    return True

        return False

    def select_space(self, column, symbol):
        for row in range(len(self.board) - 1, -1, -1):
            if self.board[row][column] == ' ':
                self.board[row][column] = symbol
                return True

        return False

    def board_full(self):
        for row in self.board:
            if ' ' in row:
                return False

        return True

    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
        print("--------------------------")
        print()

    def game_over(self):
        if self.check_win('X') or self.check_win('O') or self.board_full():
            return True

        return False

    def evaluate_board(self):
        if self.check_win('X'):
            return float('inf')

        if self.check_win('O'):
            return -float('inf')

        return self.random_eval()

    def random_eval(self):
        return random.randint(-100, 100)

    def minimax(self, is_maximizing, depth, alpha, beta):
        if self.game_over() or depth == 0:
            return [self.evaluate_board(), '']

        best_move = ''
        if is_maximizing:
            best_value = -float('inf')
            symbol = 'X'
        else:
            best_value = float('inf')
            symbol = 'O'

        for col in range(len(self.board[0])):
            new_board = deepcopy(self)
            if new_board.select_space(col, symbol):
                value = new_board.minimax(not is_maximizing, depth - 1, alpha, beta)[0]
                if is_maximizing:
                    if value >= best_value:
                        best_value = value
                        best_move = col
                        alpha = max(alpha, best_value)
                else:
                    if value <= best_value:
                        best_value = value
                        best_move = col
                        beta = min(beta, best_value)
                if alpha >= beta:
                    break

        return [best_value, best_move]


game = ConnectFour()
comp1Turn = True

while not game.board_full():
    game.print_board()
    if comp1Turn:
        symbol = 'X'
        best_move = game.minimax(True, 4, -float('inf'), float('inf'))[1]
        game.select_space(best_move, symbol)
        comp1Turn = not comp1Turn

        if game.check_win(symbol):
            game.print_board()
            print(f'{symbol} wins')
            break
    else:
        symbol = 'O'
        best_move = game.minimax(False, 4, -float('inf'), float('inf'))[1]
        game.select_space(best_move, symbol)
        comp1Turn = not comp1Turn

        if game.check_win(symbol):
            game.print_board()
            print(f'{symbol} wins')
            break

else:
    game.print_board()
    print('Its a Tie')
