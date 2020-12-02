


from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Softmax, Dropout
from keras.wrappers.scikit_learn import KerasRegressor

from game import valid_location, next_open_row, to_binary, get_states, place_player


# Import data in a 80/20 train test split
# import into df
data = pd.read_csv("data_c4.csv", index_col=False)
#print(data.head())
training_data = data.copy()
training_data = training_data.drop(["Player_1 Wins", "Player_2 Wins"], axis=1)
#split into labels and targets
features = np.array(training_data.drop(["Player_1_Win_Percent","Player_2_Win_Percent"], axis=1))
labels = np.array(training_data.drop([str(x+1) for x in range(126)], axis=1))
#split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

print(X_train.shape)

#define model params
def model(optimizer="adam", loss="KLDivergence", metrics=['accuracy']):
    layers = []
    layers.append(Dense(126, activation='relu', input_shape=(126,)))
    layers.append(Dropout(0.2))
    layers.append(Dense(252, activation='relu'))
    layers.append(Dropout(0.2))
    layers.append(Dense(126, activation='relu'))
    layers.append(Dropout(0.2))
    layers.append(Dense(2,  activation='softmax'))

    model = Sequential(layers=layers)
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics, loss_weights=None, weighted_metrics=None, run_eagerly=None)

    return model

# load, train, save model

model = model()
#fit model
model.fit(X_train, y_train, epochs=160, validation_data=(X_test, y_test), verbose=0)
model.summary()
model.evaluate(X_test, y_test)

#save model
model.save('c4_model')

