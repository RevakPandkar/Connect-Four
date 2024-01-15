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
                break

    def available_moves(self):
        available_moves = []
        for col in range(len(self.board[0])):
            if self.board[0][col] == ' ':
                available_moves.append(col)

        return available_moves

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

        elif self.check_win('O'):
            return -float('inf')

        else:
            # return self.random_eval()
            x_streaks = self.count_streaks('X')
            o_streaks = self.count_streaks('O')

            return x_streaks - o_streaks

    def random_eval(self):
        return random.randint(-100, 100)

    def count_streaks(self, symbol):
        count = 0

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] != symbol:
                    continue

                # Right Streaks
                if col < len(self.board[0]) - 3:
                    num_in_streak = 0
                    for i in range(4):
                        if self.board[row][col + i] == symbol:
                            num_in_streak += 1
                        elif self.board[row][col + i] != ' ':
                            num_in_streak = 0
                            break
                    count += num_in_streak

                # Left Streaks
                if col > 2:
                    num_in_streak = 0
                    for i in range(4):
                        if self.board[row][col - i] == symbol:
                            num_in_streak += 1
                        elif self.board[row][col - i] != ' ':
                            num_in_streak = 0
                            break
                    count += num_in_streak

                # Down-Right Streaks
                if col < len(self.board[0]) - 3 and row < len(self.board) - 3:
                    num_in_streak = 0
                    for i in range(4):
                        if self.board[row + i][col + i] == symbol:
                            num_in_streak += 1
                        elif self.board[row + i][col + i] != ' ':
                            num_in_streak = 0
                            break
                    count += num_in_streak

                # Up-Right Streaks
                if col < len(self.board[0]) - 3 and row > 2:
                    num_in_streak = 0
                    for i in range(4):
                        if self.board[row - i][col + i] == symbol:
                            num_in_streak += 1
                        elif self.board[row - i][col + i] != ' ':
                            num_in_streak = 0
                            break
                    count += num_in_streak

                # Up-Left Streaks
                if col > 2 and row > 2:
                    num_in_streak = 0
                    for i in range(4):
                        if self.board[row - i][col - i] == symbol:
                            num_in_streak += 1
                        elif self.board[row - i][col - i] != ' ':
                            num_in_streak = 0
                            break
                    count += num_in_streak

                # Down-Left Streaks
                if col > 2 and row < len(self.board) - 3:
                    num_in_streak = 0
                    for i in range(4):
                        if self.board[row + i][col - i] == symbol:
                            num_in_streak += 1
                        elif self.board[row + i][col - i] != ' ':
                            num_in_streak = 0
                            break
                    count += num_in_streak

                # Up Streaks
                if row > 2:
                    num_in_streak = 0
                    for i in range(4):
                        if self.board[row - i][col] == symbol:
                            num_in_streak += 1
                        elif self.board[row - i][col] == ' ':
                            break
                        else:
                            num_in_streak = 0
                            break
                    count += num_in_streak

                # Down Streaks
                if row < len(self.board) - 3:
                    num_in_streak = 0
                    for i in range(4):
                        if self.board[row + i][col] == symbol:
                            num_in_streak += 1
                        else:
                            num_in_streak = 0
                            break
                    count += num_in_streak

        return count

    def minimax(self, is_maximizing, depth, alpha, beta):
        if self.game_over() or depth == 0:
            return [self.evaluate_board(), '']

        available_moves = self.available_moves()
        best_move = random.choice(available_moves)

        if is_maximizing:
            best_value = -float('inf')
            symbol = 'X'
        else:
            best_value = float('inf')
            symbol = 'O'

        for col in available_moves:
            new_board = deepcopy(self)
            new_board.select_space(col, symbol)
            value = new_board.minimax(not is_maximizing, depth - 1, alpha, beta)[0]
            if is_maximizing:
                if value > best_value:
                    best_value = value
                    best_move = col
                    alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = col
                    beta = min(beta, best_value)
            if alpha >= beta:
                break

        return [best_value, best_move]


game = ConnectFour()
player1Turn = True
pvp = False
playerTurn = True

while not game.board_full():
    if pvp:
        game.print_board()
        if player1Turn:
            column = int(input('Player 1 - Enter the column (1-7): ')) - 1
            symbol = 'X'
        else:
            column = int(input('Player 2 - Enter the column (1-7): ')) - 1
            symbol = 'O'

        if column < 0 or column >= game.columns:
            print('Invalid column. Try again')
            continue

        if game.board[0][column] != ' ':
            print('Column is full. Try again')
            continue

        game.select_space(column, symbol)
        player1Turn = not player1Turn

        if game.check_win(symbol):
            game.print_board()
            print(f'{symbol} wins')
            break
    else:
        game.print_board()
        if playerTurn:
            column = int(input('Player - Enter the column (1-7): ')) - 1
            symbol = 'X'

            if column < 0 or column >= game.columns:
                print('Invalid column. Try again')
                continue

            if game.board[0][column] != ' ':
                print('Column is full. Try again')
                continue

            game.select_space(column, symbol)
            playerTurn = not playerTurn

            if game.check_win(symbol):
                game.print_board()
                print(f'{symbol} wins')
                break
        else:
            symbol = 'O'
            best_move = game.minimax(False, 7, -float('inf'), float('inf'))[1]
            game.select_space(best_move, symbol)
            playerTurn = not playerTurn

            if game.check_win(symbol):
                game.print_board()
                print(f'{symbol} wins')
                break

else:
    game.print_board()
    print('Its a Tie')
