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
"""
#simulate a given amount of games with AI, player or random
def sim(number_sims=5):
    my_model = keras.models.load_model('c4_model')

    score_board = { "Player 1" : 0, 
                    "Player 2" : 0}
    for i in range(number_sims):
        winner = game(method_1="AI", method_2="AI", model=my_model, display=True)
        if winner == 1:
            score_board["Player 1"] += 1
        else:
            score_board["Player 2"] += 1
    return score_board
scores = sim()
print(scores)