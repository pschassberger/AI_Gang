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

# translate matrix into list
def get_states(game_board):
    my_states = []
    for r in range(ROW):
        for c in range(COLUMN):
            my_states.append(game_board[r][c])
    return my_states


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
def smart_move(game_board):
    

# function tur game state into a binary vector
def to_binary(game_state_list):
    binary_vector = []
    for i in game_state_list:
        if i == 0:
            binary_vector.append([1,0,0])
        elif i == 1:
            binary_vector.append([0,1,0])
        else:
            binary_vector.append([0,0,1])

    binary_vector = np.array(binary_vector)
    return binary_vector.flatten()

# append win or lose to record
def score_stats(game_binary, winner):
    binary_wins = []
    for game in range(len(game_binary)):
        if winner == 1:
            binary_wins.append(np.concatenate((game_binary[game], [1,0])))
        elif winner == 2:
            binary_wins.append(np.concatenate((game_binary[game], [0,1])))
    return binary_wins


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
    winner = None
    draw = None
    history = []
    binary_game = []
    
    
    # Select if we should diplay the game
    if display is not None:
        py.init()
        screen = py.display.set_mode(SCREEN_SIZE)
        draw_game_board(game_board, screen)
        py.display.update()

    
    # main game loop
    while game:

        history.append(to_binary(get_states(game_board.copy())))

        #timer to pause ai or random between turns
        # py.time.wait(100)
        #print(game_board)   

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
                    
                    #print(game_board)
                    winner = 1
                    turns+= 1
                    #history.append(to_binary(get_states(game_board.copy())))
                    binary_game = score_stats(history, 1)
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

                    #print(game_board)
                    winner = 2
                    turns+= 1
                    #history.append(to_binary(get_states(game_board.copy())))
                    binary_game = score_stats(history, 2)
                    if display is not None:
                        draw_game_board(game_board, screen)
                    game = False
        #update game with moves
        if display is not None:
            draw_game_board(game_board, screen)
        
        #check draw
        if check_draw(game_board):
            history.append(to_binary(get_states(game_board.copy())))
            game = False
            winner = None
            draw = True
        # update vars
        turns+= 1
        turn += 1
        turn = turn % 2

        # append win probabilitiea
        

        if not game:
            py.time.wait(500)

    # return outcomes
    if draw:
        pass
    else:
        return binary_game

'''    print(binary_game)
    

for i in range(100):
    game()'''