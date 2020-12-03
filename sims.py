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
Main interface for simulating the game and agent.
Simulates games with AI, player and random play options
Loads model specified in def sim
Prints number of wins, specify number_sims

"""
#simulate a given amount of games with AI, player or random
number_sims=100
def sim(number_sims):
    my_model = keras.models.load_model('c4_model')

    score_board = { "AI"        : 0, 
                    "Player 2"  : 0}
    for i in range(number_sims):
        winner = game(method_1="AI", method_2="random", model=my_model, display=False)
        if winner == 1:
            score_board["AI"] += 1
        else:
            score_board["Player 2"] += 1
    return score_board
scores = sim(number_sims)
print("Number of Simulated Games: ", number_sims)
for key, value in scores.items():
    print(key, ' : ', value)