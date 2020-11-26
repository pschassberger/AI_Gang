import numpy as np
import pygame as py
import sys
import math
from random import randint
import tensorflow as tf
import tensorflow.keras as keras
import keras.backend as K

"""
Main code for the game and helper functions to place tokens and visualize.
"""

# constants
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
def model_load(model='c4_model'):
    my_model = keras.models.load_model(model)
    return my_model
# ai moves
def ai_move(game_board, my_model, player):
    possible_moves = []
    for move in range(7):
        dummy = game_board.copy()
        if valid_location(dummy, move):
            row = next_open_row(dummy, move)
            place_player(dummy, row, move, player)
            possible_moves.append(to_binary(get_states(dummy)))       
    #load model
    #my_model = keras.models.load_model('c4_model')
    predictions = my_model.predict(np.array(possible_moves), batch_size=7)
    K.clear_session()
    #get highest prediction move
    if player == 1:
        best_col = np.argmax(predictions[:,0])
        return best_col
    else:
        best_col = np.argmax(predictions[:,1])
        return best_col   

# random move
def random_move(game_board):
    col = randint(0, 6)
    while not valid_location(game_board, col):
        col = randint(0, 6)
    return col

#moves by user
def user_move(game_board):
    col = int(input("Enter a column number: "))
    return col
    

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

#longest
def place_chip(board, col, player):
    row = next_open_row(board, col)
    board[row][col] = player
    return board
#longest run
def find_longest_run(new_board, player):
    horizontal_longest = 0
    vertical_longest = 0
    positive_longest = 0
    negative_longest = 0

    # Check longest horizontal streak
    for c in range(COLUMN - 3):
        for r in range(ROW):
            local_longest = 1
            if new_board[r][c] == player:
                local_longest += 1
                if new_board[r][c + 1] == player:
                    local_longest += 1
                    if new_board[r][c + 2] == player:
                        local_longest += 1
                        if new_board[r][c + 3] == player:
                            local_longest += 1
            if local_longest > horizontal_longest:
                horizontal_longest = local_longest

    for c in range(COLUMN):
        for r in range(ROW - 3):
            local_longest = 1
            if new_board[r][c] == player:
                local_longest += 1
                if new_board[r + 1][c] == player:
                    local_longest += 1
                    if new_board[r + 2][c] == player:
                        local_longest += 1
                        if new_board[r + 3][c] == player:
                            local_longest += 1
            if local_longest > vertical_longest:
                vertical_longest = local_longest

    for c in range(COLUMN - 3):
        for r in range(ROW - 3):
            local_longest = 1
            if new_board[r][c] == player:
                local_longest += 1
                if new_board[r + 1][c + 1] == player:
                    local_longest += 1
                    if new_board[r + 2][c + 2] == player:
                        local_longest += 1
                        if new_board[r + 3][c + 3] == player:
                            local_longest += 1
            if local_longest > positive_longest:
                positive_longest = local_longest

    for c in range(COLUMN - 3):
        for r in range(3, ROW):
            local_longest = 1
            if new_board[r][c] == player:
                local_longest += 1
                if new_board[r - 1][c + 1] == player:
                    local_longest += 1
                    if new_board[r - 2][c + 2] == player:
                        local_longest += 1
                        if new_board[r - 3][c + 3] == player:
                            local_longest += 1
            if local_longest > negative_longest:
                negative_longest = local_longest

    return max(horizontal_longest, vertical_longest, positive_longest, negative_longest)


def longest_run(curr_board, player):
    longest = [0, 0, 0, 0, 0, 0, 0]
    for col in range(0, COLUMN):
        if curr_board[ROW-1][col] == 0:
            new_board = place_chip(curr_board.copy(), col, player)
            longest[col] = find_longest_run(new_board.copy(), player)

    max_run = max(longest)
    possible_cols = []
    for i in range(len(longest)):
        if i == max_run:
            possible_cols.append(i)

    return possible_cols[randint(0, len(possible_cols)-1)]



# driver code for game
def game(player1_name="Red", player2_name="Blue", method_1=None, method_2=None, model=None, display=False, training=False):
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
    if display is not False:
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

        if display is True:
            py.draw.rect(screen, BLACK, (0, 0, WIDTH, SIZE))
            
        
        if turn == 0:
            # ai or random move
            if method_1 == "random":
                col = random_move(game_board)
            elif method_1 == "player":
                col = user_move(game_board)
            elif method_1 == "AI":
                col = ai_move(game_board, model, 1)
            elif method_1 == "longest_run":
                col = longest_run(game_board, 1)

            if valid_location(game_board, col):
                row = next_open_row(game_board, col)
                place_player(game_board, row, col, 1)
                
                if winning_move(game_board, 1):
                    winner = 1
                    turns+= 1
                    binary_game = score_stats(history, 1)
                    if display is True:
                        draw_game_board(game_board, screen)
                    game = False
      
        else:
            # ai or random move
            if method_2 == 'random':
                col = random_move(game_board)
            elif method_2 == 'player':
                col = user_move(game_board)
            elif method_2 == "AI":
                col = ai_move(game_board, model, 2)
            elif method_2 == "longest_run":
                col = longest_run(game_board, 2)


            if valid_location(game_board, col):
                row = next_open_row(game_board, col)
                place_player(game_board, row, col, 2)

                if winning_move(game_board, 2):
                    winner = 2
                    turns+= 1
                    binary_game = score_stats(history, 2)
                    if display is True:
                        draw_game_board(game_board, screen)
                    game = False


        #update game with moves
        if display is True:
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
        if not game:
            py.time.wait(500)

    # return outcomes
    if training:
        return binary_game
    else:
        return winner
    
