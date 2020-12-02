# pull it all together
import numpy as np
from game import*
from NN import*
import pandas as pd

# save numpy array as csv file
from numpy import asarray
from numpy import savetxt
# define data


# game interface and player control
# def number of games to play
def play_games(num_of_sims=300):
    # data to collect
    total_history = []
    red_winner = []
    blue_winner = []
    draws = []
    total_turns = []
    outcome = {
                "Red"   :   0,
                "Blue"  :   0, 
                "Draw"  :   0
    }

    for i in range(num_of_sims):
        history=[]
        winner=None
        num_turns=0
        
        history, winner, num_turns = game(player1_name="Red", player2_name="Blue", method1='longest_run',
                                          method2='random', display="T")
        total_history.append(history)
        total_turns.append(num_turns)
        if winner == "Red":
            red_winner.append(winner)
        elif winner == "Blue":
            blue_winner.append(winner)
        else:
            draws.append(winner)

    df = pd.DataFrame(total_history)
    
    df.to_csv('data.csv',index=False, header=False)

    outcome.update(Red = len(red_winner) / num_of_sims)
    outcome.update(Blue = len(blue_winner) / num_of_sims)
    outcome.update(Draw = len(draws) / num_of_sims)

    print(outcome)


play_games()
