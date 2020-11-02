# build basic model
import numpy as np
import pandas as pd
import csv

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout 
from keras.utils import to_categorical

file = open('data.csv')
data = csv.reader(file)

data= list(data)
training_data = np.array(data)

#find size of batch
size = training_data.shape
batch_size = size[1]

inputi = []
output = []
for dat in data:
    inputi.append(dat[1])
    output.append(dat[0])

X = np.array(data).reshape((-1, batch_size))
y = [0, 1, 2]
limit = int(0.8 * len(X))
X_train = X[:limit]
X_test = X[limit:]

print(X_train)

    

def nn_model(batch_size):
    layers = []
    layers.append(Dense(42, activation='relu', input_shape=(batch_size,)))
    layers.append(Dense(42, activation='relu'))
    layers.append(Dense(1, activation='softmax'))

    model = keras.Sequential(layers)
    model.compile(loss='categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])
