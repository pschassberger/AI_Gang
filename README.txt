ML Semester Project

    Write a game of connect four and train two agents to play
against each other. 

Method:
    In order to build a agent capable of making favorable decisions we decided to build a training data set of 1000 games, played by players choosing a column at random.
    The individual game states where then saved as a flat binary vector with an associated win/loss column and appended to a csv file with all duplicate game states removed
    for training. Our NN then trained on the generated data to anticipate the probability of a particular move ending in a win. The model is then saved and called
    for each turn in the game to make an autonomous decision.
Game Interface:
    The game is built using pygame and traditional ML libraries, all located in the associated pipfile.
Model:
    Our model is a 5 layer keras model, utilizing Dense layers followed by dropout layers to prevent over fitting. Various hyperparamters have been tested and we have 
    settled on the parameters outlined in NN.py.


How to Play:

    Run main.py for a player vs AI game, it will prompt until the user terminates the game.
    All other .py files are for training and simulating, each file has methods outlined
    Models are saved to file, c4_model, c4_model_l