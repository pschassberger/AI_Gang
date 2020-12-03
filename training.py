# pull it all together
import numpy as np
from game import*
import pandas as pd
import csv
# define data
"""
Create training data for NN, set method of player and number of simulations.
Data will be stored and manipulated in a dataframe and save it to a csv
Adjust num_sims for more/less games
"""
#helper functions
def clean_data(df_games):
    # create df based on only volumns to id repeats
    clean_data = df_games.copy()
    game_data = pd.DataFrame(clean_data, columns=[x+1 for x in range(126)])

    doubles = game_data[game_data.duplicated(keep=False)]  
    duplicate = list(doubles.index)
    temp = duplicate.copy()
    
    # check values to see wuch rows are equal, append score for each
    for index in duplicate:
        temp.remove(index)
        for value in temp:
            # if equal append score and delete duplicate
            initial_pt = list(game_data.iloc[index])
            chk_pt = list(game_data.iloc[value])
            if (initial_pt == chk_pt):
                player1_score = int(clean_data.at[value, "Player_1 Wins"])
                player2_score = int(clean_data.at[value, "Player_2 Wins"])

                clean_data.at[clean_data.index[index], "Player_1 Wins"] += player1_score 
                clean_data.at[clean_data.index[index], "Player_2 Wins"] += player2_score
 
                temp.remove(value)
                duplicate.remove(value)
                

    # drop all similar rows after updating scores
    clean_data.drop_duplicates(subset=[x+1 for x in range(126)], keep="first", inplace=True)
    return clean_data
                
    
# check that no doubles exist
def check(df_games):
    game_data = pd.DataFrame(df_games, columns=[x+1 for x in range(126)])
    doubles = game_data[game_data.duplicated(keep=False)]
    print("oi", doubles)
    
# game interface and player control
# def number of games to play
def play_games(num_of_sims=10000):
    # data to collect
    total_history = []

    for i in range(num_of_sims):
        history=[]
        # call game for data collection
        history = game(player1_name="Red", player2_name="Blue", method_1="random", method_2="random", model=None, display=False, training=True)
        total_history += history


    # store data in df and save to csv 
    training_data = pd.DataFrame(total_history)
    training_data.columns = [x+1 for x in range(126)] + ["Player_1 Wins", "Player_2 Wins"]
    # clean data
    data = clean_data(training_data)
    check(data)
    # save training data to csv
    data.to_csv('big_data_c4.csv')
    

play_games()


#refine training data, add equal rows and add scores
