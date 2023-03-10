import pandas as pd
import itertools
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.layers import Input, Dense
from keras.models import Model, load_model
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.metrics import accuracy_score
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.optimizers import SGD
from matplotlib import pyplot
import math

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.0001)

def get_mean(array): 
    sum = 0
    for x in array: 
        sum += x
    return sum / len(array)

def get_std_dev(numbers):
  # Return 0 if the input list is empty
  if not numbers.any():
    return 0

  # Calculate the mean of the numbers
  mean = get_mean(numbers)

  # Calculate the variance of the numbers
  variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)

  # Calculate the standard deviation from the variance
  std_dev = math.sqrt(variance)

  return std_dev

def get_acc_score(Y_proba, y_true): 
    mean = get_mean(Y_proba)
    std_dev = get_std_dev(Y_proba)
    thresh_high = mean + std_dev
    thresh_low = mean - std_dev
    predicted = 0
    predicted_right = 0
    for x in range(len(Y_proba)): 
        if Y_proba[x] < thresh_low: 
            predicted += 1
            if y_true[x] == 0: 
                predicted_right += 1
        elif Y_proba[x] > thresh_high: 
            predicted += 1
            if y_true[x] == 1: 
                predicted_right += 1
    if predicted == 0: return 0
    else: return (predicted_right/predicted, mean, std_dev)


# load the training data from a file
df = pd.read_excel('./total_data.xlsx').fillna(value=0)

# extract the binary output variable from the dataframe
y = df['hitOver'].values

# extract all input variables from the dataframe
all_input_variables = ['total', 'totalppg', 'size_of_spread', 'pct_overs_hit', 'pace', 'ortg', 'drtg', 'drb', 'threePAR', 'ts', 'ftr', 'd_tov', 'o_tov', 'ftperfga', 'points_over_average_ratio', 'hotness_ratio', 'std_dev', 'win_pct', 'rsw', 'win_pct_close', 'mov_a', 'injury_gmsc', 'injury_mins']

# define the required variables to be included in every combination
required_variables = ['size_of_spread', 'threePAR', 'injury_mins', 'std_dev', 'hotness_ratio', 'points_over_average_ratio', 'ftr', 'pct_overs_hit', 'total']

best_combo = ['total', 'size_of_spread', 'pct_overs_hit', 'ortg', 'drb', 'threePAR', 'ts', 'ftr', 'ftperfga', 'points_over_average_ratio', 'hotness_ratio', 'std_dev', 'win_pct', 'rsw', 'win_pct_close', 'injury_gmsc', 'injury_mins']

# # print the 25 best combinations and their brier scores
# for i, (combination, acc_score) in enumerate(best_acc_scores):
#     print(f"{str(i+1)}. {combination} with accuracy of {acc_score}")
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping

def run_model(combo, random_state): 
    X = df[list(combo)].values
    X = StandardScaler().fit_transform(X)
    # y = StandardScaler().fit_transform(y.reshape(len(y),1))[:,0]
    # split training and testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)

    # define the input shape
    input_shape = (X.shape[1],)

    # define the input layer
    inputs = Input(shape=input_shape)

    # define the hidden layer with L2 regularization
    hidden1 = Dense(100, activation='relu', kernel_regularizer=l2(0.01))(inputs)

    # define the output layer
    outputs = Dense(1, activation='sigmoid')(hidden1)

    # define the model
    model = Model(inputs=inputs, outputs=outputs)

    opt = SGD(learning_rate=0.01, momentum=0.9)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

    # fit the model to the training data with early stopping and a validation split
    history = model.fit(X_train, y_train, validation_split=0.2, epochs=30, batch_size=128, verbose = 0, callbacks=[EarlyStopping(monitor = 'val_loss', restore_best_weights = True, patience=30), reduce_lr])

    # evaluate the model
    _, train_acc = model.evaluate(X_train, y_train, verbose=0)
    _, test_acc = model.evaluate(X_test, y_test, verbose=0)
    
    Y_proba = model.predict(X_test)
    Y_all_predict = model.predict(X)
    df['ml_prob'] = Y_all_predict

    df.to_excel('./total_data.xlsx')

    print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

    acc_score = get_acc_score(Y_proba, y_test)
    mean = acc_score[1]
    std_dev = acc_score[2]
    acc_score = acc_score[0]

    print('Acc_score (threshold): %.3f' % acc_score)
    print(f'Mean was {mean} with a standard deviation of {std_dev}!')
    model.save('totals_model.h5')

    pyplot.clf()
    pyplot.subplot(211)
    pyplot.title('Loss')
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')
    pyplot.legend()

    # plot accuracy during training
    pyplot.subplot(212)
    pyplot.title('Accuracy')
    pyplot.plot(history.history['accuracy'], label='train')
    pyplot.plot(history.history['val_accuracy'], label='test')
    pyplot.legend()

    pyplot.show()

    return (test_acc, acc_score)


def get_best_combo(): 
    n = 0
    total_combos = 9908
    for r in range(len(required_variables)+7, len(all_input_variables) - 1):
        combinations = itertools.combinations(all_input_variables, r)
        for combination in combinations:
            if not all(var in combination for var in required_variables):
                continue
            n += 1
            print("Now %.3f percent of the way through!" % (100*n/total_combos))
            random_state = 20
            results = run_model(combination, random_state)
            if results[1] > 0.54: 
                print(f"Found combination {combination} with high acc_score!")
                results_array = []
                for x in range(3): 
                    results_array.append(run_model(combination, random_state+x)[1])
                if get_mean(results_array) > 0.524 and min(results_array) > 0.51: 
                    print(f"Found combination {combination} with high average and min acc_score at different random states!")
                    results_array = []
                    for y in range(3): 
                        results_array.append(run_model(combination, random_state+3+y)[0])
                    if get_mean(results_array) > 0.51 and min(results_array) > 0.5: 
                        print(f"Found the best combo! {combination}")
                        return combination

# get_best_combo()
run_model(best_combo, 20)