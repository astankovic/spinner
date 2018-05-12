import numpy as np
from sklearn import preprocessing
import tensorflow as tf
from keras import Sequential


def get_train_test(timeseries, sequence_length=10,
                   train_size=0.9, roll_mean_window=5,
                   normalize=True, scale=False):
    #smoothen series
    if roll_mean_window:
        timeseries = timeseries.rolling(roll_mean_window).mean().dropna()

    #create windows
    result = []
    for index in range(len(timeseries) - sequence_length):
        result.append(timeseries[index: index + sequence_length])

    #normalize data as a variation of 0th index
    if normalize:
        normalised_data = []
        for window in result:
            normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
            normalised_data.append(normalised_window)

    #split test train data
    result = np.array(result)
    row = round(train_size * result.shape[0])

    train = result[:int(row), :]
    test = result[int(row):, :]

    #scale data
    scaler = None
    if scale:
        scaler = MinMaxScaler(feature_range=(0,1))
        train = scaler.fit_transform(train)
        test = scaler.fit_transform(test)

    #split independent and dependent variables
    x_train = train[:, :-1]
    y_train = train[:, -1]

    x_test = test[:, :-1]
    y_test = test[:, -1]

    #transform for LSTM input
    x_train = np.reshape(x_train, (x_train.shape[0],
                                   x_train.shape[1],
                                   1))
    x_test = np.reshape(x_test, (x_test.shape[0],
                                 x_test.shape[1],
                                 1))

    return x_train, y_train, x_test, y_test, scaler


def get_seq_model(hidden_units=4, input_shape=(1,1), verbose=False):
    
    model = Sequential()

    #input shape = timesteps * features
    model.add(LSTM(input_shape=input_shape,
                   units=hidden_units,
                   return_sequences=True
    ))

    #TimeDistributedDense uses processing for all time steps
    model.add(TimeDistributed(Dense(1)))
    start = time.time()
    


