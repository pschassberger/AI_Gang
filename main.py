# pull it all together
import numpy as np
from game import*
from NN import*

# save numpy array as csv file
from numpy import asarray
from numpy import savetxt
# define data



# game interface and player control
# def number of games to play
def play_games(num_of_sims=1000):
    # data to collect
    total_history = []
    total_winner = []
    total_turns = []

    for i in range(num_of_sims):
        history=[]
        winner=None
        num_turns=0
        
        history, winner, num_turns = game(player1_name="Red", player2_name="Blue", method='random', display=None)
        total_history.append(history)
        total_winner.append(winner)
        total_turns.append(num_turns)
    print(total_history)
        

play_games()

