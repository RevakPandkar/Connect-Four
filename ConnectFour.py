import pygame
import random
from copy import deepcopy


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

    def get_free_row_num(self, column):
        if self.board[0][column] != ' ':
            return -1

        for row in range(len(self.board) - 1, -1, -1):
            if self.board[row][column] == ' ':
                return row

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

    def minimax(self, is_maximizing, depth, alpha, beta):
        if self.game_over() or depth == 0:
            return [self.evaluate_board(), '']

        available_moves = self.available_moves()
        # best_move = ''
        # best_move = random.choice(available_moves)
        random.shuffle(available_moves)
        best_move = available_moves[0]

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


def draw_board(win):
    # for i in range(1,8):
    #     pygame.draw.line(win, (255, 255, 255), (100, i * 100), (800, i * 100), 4)
    for i in range(1, 9):
        pygame.draw.line(win, (255, 255, 255), (i * 100, 100), (i * 100, 700), 4)
    pygame.draw.line(win, (255, 255, 255), (100, 700), (800, 700), 4)
    pygame.display.update()


def draw_symbol(win, symbol, symbol_pos):
    if symbol == 'X':
        pygame.draw.circle(win, (255, 0, 0), (symbol_pos[0], symbol_pos[1]), 43)

    elif symbol == 'O':
        pygame.draw.circle(win, (255, 255, 0), (symbol_pos[0], symbol_pos[1]), 43)


def draw_start_screen(win):
    win.fill((0, 0, 0))
    game_name = title_font.render('Connect Four', True, (255, 255, 255))
    game_name_rect = game_name.get_rect(center=(600, 200))
    win.blit(game_name, game_name_rect)

    pvp_button = pygame.Surface((250, 65))
    pvp_button.fill('White')
    pvp_button_rect = pvp_button.get_rect(center=(600, 375))
    win.blit(pvp_button, pvp_button_rect)

    pvp_text = button_font.render('Vs. Player', True, (0, 0, 0))
    pvp_text_rect = pvp_text.get_rect(center=(600, 375))
    win.blit(pvp_text, pvp_text_rect)

    pvc_button1 = pygame.Surface((350, 65))
    pvc_button1.fill('White')
    pvc_button1_rect = pvc_button1.get_rect(center=(600, 475))
    win.blit(pvc_button1, pvc_button1_rect)

    pvc_text1 = button_font.render('Vs. Comp as Red', True, (0, 0, 0))
    pvc_text1_rect = pvc_text1.get_rect(center=(600, 475))
    win.blit(pvc_text1, pvc_text1_rect)

    pvc_button2 = pygame.Surface((400, 65))
    pvc_button2.fill('White')
    pvc_button2_rect = pvc_button2.get_rect(center=(600, 575))
    win.blit(pvc_button2, pvc_button2_rect)

    pvc_text2 = button_font.render('Vs. Comp as Yellow', True, (0, 0, 0))
    pvc_text2_rect = pvc_text2.get_rect(center=(600, 575))
    win.blit(pvc_text2, pvc_text2_rect)

    game_active = False
    pvp = False
    playerSym = ""

    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if pvp_button_rect.collidepoint(mouse_pos):
            game_active = True
            pvp = True
        if pvc_button1_rect.collidepoint(mouse_pos):
            game_active = True
            pvp = False
            playerSym = "X"
        if pvc_button2_rect.collidepoint(mouse_pos):
            game_active = True
            pvp = False
            playerSym = "O"

    return game_active, pvp, playerSym


def draw_win_message(win, winning_symbol):
    if winning_symbol == 'X':
        winning_symbol = 'Red'
        win_msg = win_msg_font.render(f'{winning_symbol} wins!', True, (255, 255, 255))
        win_msg_rect = win_msg.get_rect(center=(1000, 200))
    elif winning_symbol == 'O':
        winning_symbol = 'Yellow'
        win_msg = win_msg_font.render(f'{winning_symbol} wins!', True, (255, 255, 255))
        win_msg_rect = win_msg.get_rect(center=(1000, 200))
    else:
        win_msg = win_msg_font.render("It's a Tie", True, (255, 255, 255))
        win_msg_rect = win_msg.get_rect(center=(1000, 200))

    win.blit(win_msg, win_msg_rect)

    restart_button = pygame.Surface((175, 50))
    restart_button.fill('White')
    restart_button_rect = restart_button.get_rect(center=(1000, 350))
    win.blit(restart_button, restart_button_rect)

    restart_text = button_font.render('Restart', True, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=(1000, 350))
    win.blit(restart_text, restart_text_rect)

    main_menu_button = pygame.Surface((250, 50))
    main_menu_button.fill('White')
    main_menu_button_rect = main_menu_button.get_rect(center=(1000, 425))
    win.blit(main_menu_button, main_menu_button_rect)

    main_menu_text = button_font.render('Main Menu', True, (0, 0, 0))
    main_menu_text_rect = main_menu_text.get_rect(center=(1000, 425))
    win.blit(main_menu_text, main_menu_text_rect)

    restart = False
    main_menu = False

    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if restart_button_rect.collidepoint(mouse_pos):
            restart = True
        if main_menu_button_rect.collidepoint(mouse_pos):
            main_menu = True

    return restart, main_menu


def get_col_symbol_pos(mouse_pos):
    symbol_pos = ()
    col_num = mouse_pos[0] // 100 - 1

    if 0 <= col_num <= 6 and mouse_pos[1] < 700:
        row_num = game.get_free_row_num(col_num)
        if row_num != -1:
            symbol_pos = ((col_num + 1) * 100 + 50, (row_num + 1) * 100 + 50)

    return col_num, symbol_pos


def get_comp_symbol_pos(comp_move):
    row_num = game.get_free_row_num(comp_move)
    symbol_pos = ((comp_move + 1) * 100 + 50, (row_num + 1) * 100 + 50)
    return symbol_pos


WIN_WIDTH = 1200
WIN_HEIGHT = 750

pygame.init()
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Connect Four')
button_font = pygame.font.SysFont('timesnewroman', 45)
win_msg_font = pygame.font.SysFont('timesnewroman', 60)
title_font = pygame.font.SysFont('timesnewroman', 90)

game = ConnectFour()
game_active = False
game_over = False
draw_black_screen = True
wait_for_input = 0
winning_symbol = ''

AI_LEVEL = 5

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if game_active:
        if draw_black_screen:
            win.fill((0, 0, 0))
            draw_black_screen = False

        wait_for_input += 2
        if wait_for_input > 70:
            wait_for_input = 70
        draw_board(win)

        if not game_over:
            if pvp:
                if wait_for_input > 60 and pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    col_num, symbol_pos = get_col_symbol_pos(mouse_pos)
                    if symbol_pos != ():
                        if player1Turn:
                            symbol = 'X'
                        else:
                            symbol = 'O'

                        wait_for_input = 0
                        player1Turn = not player1Turn
                        draw_symbol(win, symbol, symbol_pos)
                        game.select_space(col_num, symbol)
                        game.print_board()
                        if game.check_win(symbol):
                            print(f'{symbol} wins!')
                            winning_symbol = symbol
                            game_over = True
                        elif game.board_full():
                            print('Its a Tie')
                            game_over = True
            else:
                if playerTurn:
                    if wait_for_input > 60 and pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        col_num, symbol_pos = get_col_symbol_pos(mouse_pos)
                        if symbol_pos != ():
                            wait_for_input = 0
                            playerTurn = not playerTurn
                            draw_symbol(win, playerSym, symbol_pos)
                            game.select_space(col_num, playerSym)
                            game.print_board()
                            if game.check_win(playerSym):
                                print(f'{playerSym} wins!')
                                winning_symbol = playerSym
                                game_over = True
                            elif game.board_full():
                                print('Its a Tie')
                                game_over = True
                else:
                    if wait_for_input > 45:
                        best_move = game.minimax(is_maximizing, AI_LEVEL, -float('inf'), float('inf'))[1]
                        symbol_pos = get_comp_symbol_pos(best_move)
                        draw_symbol(win, compSym, symbol_pos)
                        game.select_space(best_move, compSym)
                        playerTurn = not playerTurn
                        game.print_board()
                        if game.check_win(compSym):
                            print(f'{compSym} wins!')
                            winning_symbol = compSym
                            game_over = True
                        elif game.board_full():
                            print('Its a Tie')
                            game_over = True

        else:
            restart, main_menu = draw_win_message(win, winning_symbol)
            if restart:
                game = ConnectFour()
                draw_black_screen = True
                game_over = False
                player1Turn = True
                if playerSym == "X":
                    playerTurn = True
                else:
                    playerTurn = False

            elif main_menu:
                game = ConnectFour()
                game_active = False
                game_over = False
                draw_black_screen = True

    else:
        game_active, pvp, playerSym = draw_start_screen(win)

        if pvp:
            player1Turn = True
        else:
            if playerSym == "X":
                playerTurn = True
                compSym = "O"
                is_maximizing = False
            else:
                playerTurn = False
                compSym = "X"
                is_maximizing = True

    pygame.display.update()
