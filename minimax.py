import numpy as np
import random
from game import *

def best_move(game_state, player, col):
    score = 0

    

    for c in range(COLUMN-3):
		for r in range(ROW):
			if (game_board[r][c] == player and 
                game_board[r][c+1] == player and 
                game_board[r][c+2] == player):
				score += 100
            if (game_board[r][c] == player and 
                game_board[r][c+1] == player):
				score += 50
            if (game_board[r][c] == player):
				score += 10

	# Check vertical locations for win
	for c in range(COLUMN):
		for r in range(ROW-3):
			if (game_board[r][c] == player and 
                game_board[r+1][c] == player and 
                game_board[r+2][c] == player):
				score += 100
            if (game_board[r][c] == player and 
                game_board[r+1][c] == player):
				score += 50
            if (game_board[r][c] == player):
				score += 10

	# Check positively sloped diaganols
	for c in range(COLUMN-3):
		for r in range(ROW-3):
			if (game_board[r][c] == player and 
                game_board[r+1][c+1] == player and 
                game_board[r+2][c+2] == player):
				score += 100
            if (game_board[r][c] == player and 
                game_board[r+1][c+1] == player):
				score += 50
            if (game_board[r][c] == player):
				score += 10

	# Check negatively sloped diaganols
	for c in range(COLUMN-3):
		for r in range(3, ROW):
			if (game_board[r][c] == player and 
                game_board[r-1][c+1] == player and 
                game_board[r-2][c+2] == player):
				score += 100
            if (game_board[r][c] == player and 
                game_board[r-1][c+1] == player):
				score += 50
            if (game_board[r][c] == player):
				score += 10


    if (3 in a row) + 100
    if (2 in a row) + 50
    if (1) + 10
    if (None) - 100

def minimax(game_state, player, turn, score, depth):

    # check base case or win
    if (winning_move(game_state, player)):
        return
    else:

        #recursive game tree geberation
        for i in range(4):
            
            #check if col has a spot
            if (turn == 0):
                if valid_location(game_state, i):
                    row = next_open_row(game_state, i)
                    place_player(game_state, row, col, 1)
                   

                    # update vars
                    turn += 1
                    turn = turn % 2
                    depth -= 1
                    minimax(game_state, player, turn, score, depth)

            else:
                if valid_location(game_state, i):
                    row = next_open_row(game_state, i)
                    place_player(game_state, row, col, 1)
                

                    # update vars
                    turn += 1
                    turn = turn % 2
                    depth -= 1
                    minimax(game_state, player, turn, score, depth)



game_state = initialize_game()