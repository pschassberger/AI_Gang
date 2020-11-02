import numpy as np
import pygame as py
import sys
import math
from random import randint

BLUE = (51,153,255)
BLACK = (0,0,0)
RED = (204,0,102)
YELLOW = (255,255,102)

ROW = 6
COLUMN = 7
SIZE = 100
RADIUS = int(SIZE/2 - 5)

WIDTH = COLUMN * SIZE
HEIGHT = (ROW+1) * SIZE
SCREEN_SIZE = (WIDTH, HEIGHT)


# helpers
def initialize_game():
	game = np.zeros((ROW,COLUMN), dtype=int)
	return game

def place_player(game_board, row, col, player):
	game_board[row][col] = player


def valid_location(game_board, col):
	return game_board[ROW-1][col] == 0

def next_open_row(game_board, col):
	for row in range(ROW):
		if game_board[row][col] == 0:
			return row


# controler helpers
# ai moves
def ai_move():
    col = int(input("Enter a column number: "))
    return col
# random move
def random_move(game_board):
    col = randint(0, 6)
    while not valid_location(game_board, col):
        col = randint(0, 6)
    return col
# function to update outcomes
def stats(history, winner, turns):
    return history, winner, turn



# game states
# is draw, basic
def check_draw(game_board):
    if 0 not in game_board:
        return True
    else:
        return False

def winning_move(game_board, player):
	# Check horizontal locations for win
	for c in range(COLUMN-3):
		for r in range(ROW):
			if (game_board[r][c] == player and 
                game_board[r][c+1] == player and 
                game_board[r][c+2] == player and 
                game_board[r][c+3] == player):
				return True

	# Check vertical locations for win
	for c in range(COLUMN):
		for r in range(ROW-3):
			if (game_board[r][c] == player and 
                game_board[r+1][c] == player and 
                game_board[r+2][c] == player and 
                game_board[r+3][c] == player):
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN-3):
		for r in range(ROW-3):
			if (game_board[r][c] == player and 
                game_board[r+1][c+1] == player and 
                game_board[r+2][c+2] == player and 
                game_board[r+3][c+3] == player):
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN-3):
		for r in range(3, ROW):
			if (game_board[r][c] == player and 
                game_board[r-1][c+1] == player and 
                game_board[r-2][c+2] == player and 
                game_board[r-3][c+3] == player):
				return True

def draw_game_board(game_board, screen):
	for c in range(COLUMN):
		for r in range(ROW):
			py.draw.rect(screen, BLUE, (c*SIZE, r*SIZE+SIZE, SIZE, SIZE))
			py.draw.circle(screen, BLACK, (int(c*SIZE+SIZE/2), int(r*SIZE+SIZE+SIZE/2)), RADIUS)
	
	for c in range(COLUMN):
		for r in range(ROW):		
			if game_board[r][c] == 1:
				py.draw.circle(screen, RED, (int(c*SIZE+SIZE/2), HEIGHT-int(r*SIZE+SIZE/2)), RADIUS)
			elif game_board[r][c] == 2: 
				py.draw.circle(screen, YELLOW, (int(c*SIZE+SIZE/2), HEIGHT-int(r*SIZE+SIZE/2)), RADIUS)
	py.display.update()




# driver code for game
def game(player1_name="Red", player2_name="Blue", method='random', display=None):
    # initialize vars
    game_board = initialize_game()
    game = True
    turn = 0
    turns = 0
    history = []
    winner = None
    
    
    # Select if we should diplay the game
    if display is not None:
        py.init()
        screen = py.display.set_mode(SCREEN_SIZE)
        draw_game_board(game_board, screen)
        py.display.update()

    
    # main game loop
    while game:

        history.append(game_board.copy())

        
        # check for key events
        '''for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()'''


        
        #timer to pause ai or random between turns
        # py.time.wait(100)
        print(game_board)
       
        

        if display is not None:
            py.draw.rect(screen, BLACK, (0, 0, WIDTH, SIZE))
            
        
        if turn == 0:
            # ai or random move
            if method == 'random':
                col = random_move(game_board)
            else:
                col = ai_move()

            if valid_location(game_board, col):
                row = next_open_row(game_board, col)
                place_player(game_board, row, col, 1)
                game_board[row][col] == 1
                
                if winning_move(game_board, 1):
                    
                    print(game_board)
                    winner = player1_name
                    turns+= 1
                    history.append(game_board.copy())
                    if display is not None:
                        draw_game_board(game_board, screen)
                    game = False
      
        else:
            # ai or random move
            if method == 'random':
                col = random_move(game_board)
            else:
                col = ai_move()

            if valid_location(game_board, col):
                row = next_open_row(game_board, col)
                place_player(game_board, row, col, 2)
                

                if winning_move(game_board, 2):

                    print(game_board)
                    winner = player2_name
                    turns+= 1
                    history.append(game_board.copy())
                    if display is not None:
                        draw_game_board(game_board, screen)
                    game = False
        #update game with moves
        if display is not None:
            draw_game_board(game_board, screen)
        
        #check draw
        if check_draw(game_board):
            history.append(game_board.copy())
            game = False
            winner = None
        # update vars
        turns+= 1
        turn += 1
        turn = turn % 2
        

        if not game:
            py.time.wait(500)

    # return outcomes
    return history, winner, turns