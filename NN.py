


from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Softmax, Dropout




# Import data in a 80/20 train test split
# import into df
data = pd.read_csv("test_edit.csv", index_col=False)
#print(data.head())
training_data = data.copy()
training_data = training_data.drop(["Player_1 Wins", "Player_2 Wins"], axis=1)
#split into labels and targets
features = np.array(training_data.drop(["Player_1_Win_Percent","Player_2_Win_Percent"], axis=1))
labels = np.array(training_data.drop([str(x+1) for x in range(126)], axis=1))
#split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=42)

print(X_train.shape)


def model():
    layers = []
    layers.append(Dense(126, activation='relu', input_shape=(126,)))
    layers.append(Dropout(0.05))
    layers.append(Dense(126, activation='relu'))
    layers.append(Dropout(0.05))
    layers.append(Dense(2,  activation='softmax'))

    model = keras.Sequential(layers=layers)

    return model


model = model()

#compile model
model.compile(optimizer="adam", loss="KLDivergence", metrics="mse", loss_weights=None,
    weighted_metrics=None, run_eagerly=None)

#fit model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=500)

model.summary()



