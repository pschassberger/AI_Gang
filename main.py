# Bring net and game togeter
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Softmax, Dropout

from game import game


"""
Main interface for interacting with the game and agent.
Simulates games with AI, player and random play options
Loads model specified in def sim

"""
#simulate a given amount of games with AI, player or random

def sim():
    total_games = 0
    my_model = keras.models.load_model('c4_model')

    score_board = { "AI"        : 0, 
                    "Player 2"  : 0}
    while True:
        total_games += 1
        winner = game(method_1="AI", method_2="random", model=my_model, display=True)

        if winner == 1:
            score_board["AI"] += 1
        else:
            score_board["Player 2"] += 1



    return score_board, total_games

scores, total_games = sim()
print("Number of Games: ", total_games)
for key, value in scores.items():
    print(key, ' : ', value)