import numpy as np
import pygame as py
import sys
import math


GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW = 6
COLUMN = 7
SIZE = 100
RADIUS = int(SIZE / 2 - 5)

WIDTH = COLUMN * SIZE
HEIGHT = (ROW + 1) * SIZE
size = (WIDTH, HEIGHT)

curr_game_state = ""


# helpers
def initialize_game():
    game = np.zeros((ROW, COLUMN))
    return game


def place_player(game_board, row, col, player):
    game_board[row][col] = player


def valid_location(game_board, col):
    return game_board[ROW - 1][col] == 0


def next_open_row(game_board, col):
    for row in range(ROW):
        if game_board[row][col] == 0:
            return row

def canPlayCol(col):
    if (game_board[ROW-1][col]) == 0:
        return True
    print("That column is full.")
    return False

# ai moves
def ai_move():
    col = -1
    while col < 0 or col >= COLUMN or not canPlayCol(col):
        col = int(input("Enter a valid column number: "))
    return col


def winning_move(game_board, player):
    # Check horizontal locations for win
    for c in range(COLUMN - 3):
        for r in range(ROW):
            if (game_board[r][c] == player and
                    game_board[r][c + 1] == player and
                    game_board[r][c + 2] == player and
                    game_board[r][c + 3] == player):
                return True

    # Check vertical locations for win
    for c in range(COLUMN):
        for r in range(ROW - 3):
            if (game_board[r][c] == player and
                    game_board[r + 1][c] == player and
                    game_board[r + 2][c] == player and
                    game_board[r + 3][c] == player):
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN - 3):
        for r in range(ROW - 3):
            if (game_board[r][c] == player and
                    game_board[r + 1][c + 1] == player and
                    game_board[r + 2][c + 2] == player and
                    game_board[r + 3][c + 3] == player):
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN - 3):
        for r in range(3, ROW):
            if (game_board[r][c] == player and
                    game_board[r - 1][c + 1] == player and
                    game_board[r - 2][c + 2] == player and
                    game_board[r - 3][c + 3] == player):
                return True


def draw_game_board(game_board):
    for c in range(COLUMN):
        for r in range(ROW):
            py.draw.rect(screen, GRAY, (c * SIZE, r * SIZE + SIZE, SIZE, SIZE))
            py.draw.circle(screen, BLACK, (int(c * SIZE + SIZE / 2), int(r * SIZE + SIZE + SIZE / 2)), RADIUS)

    for c in range(COLUMN):
        for r in range(ROW):
            if game_board[r][c] == 1:
                py.draw.circle(screen, RED, (int(c * SIZE + SIZE / 2), HEIGHT - int(r * SIZE + SIZE / 2)), RADIUS)
            elif game_board[r][c] == 2:
                py.draw.circle(screen, YELLOW, (int(c * SIZE + SIZE / 2), HEIGHT - int(r * SIZE + SIZE / 2)), RADIUS)
    py.display.update()


# initialize vars
game_board = initialize_game()
game = True
turn = 0
py.init()
screen = py.display.set_mode(size)
draw_game_board(game_board)
py.display.update()
# main game loop
while game:

    # check for key events
    py.event.get()

    print(np.flip(game_board, 0))

    py.draw.rect(screen, BLACK, (0, 0, WIDTH, SIZE))

    # Ask for Player 1 Input
    if turn == 0:

        col = ai_move()
        curr_game_state += str(col)

        if valid_location(game_board, col):
            row = next_open_row(game_board, col)
            place_player(game_board, row, col, 1)

            if winning_move(game_board, 1):
                game = False


    # player 2 input
    else:
        col = ai_move()
        curr_game_state += str(col)

        if valid_location(game_board, col):
            row = next_open_row(game_board, col)
            place_player(game_board, row, col, 2)

            if winning_move(game_board, 2):
                game = False

    draw_game_board(game_board)

    turn += 1
    turn = turn % 2

    if not game:
        py.time.wait(2000)

