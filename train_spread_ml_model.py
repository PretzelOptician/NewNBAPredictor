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
    else: return predicted_right/predicted


# load the training data from a file
df = pd.read_excel('./spread_data.xlsx').fillna(value=0)

# extract the binary output variable from the dataframe
y = df['home_spread_hit'].values

# extract all input variables from the dataframe
all_input_variables = ['total', 'spread', 'pct_spreads_hit_h', 'pct_spreads_hit_a', 'ppg_h', 'ppg_a', 'pace_h', 'pace_a', 'ortg_h', 'ortg_a', 'drtg_h', 'drtg_a', 'drb_h', 'drb_a', 'threePAR_h', 'threePAR_a', 'ts_h', 'ts_a', 'ftr_h', 'ftr_a', 'd_tov_h', 'd_tov_a', 'o_tov_h', 'o_tov_a', 'ftperfga_h', 'ftperfga_a', 'points_over_average_ratio_h', 'points_over_average_ratio_a', 'hotness_ratio_h', 'hotness_ratio_a', 'std_dev_h', 'std_dev_a', 'win_pct_h', 'win_pct_a', 'rsw_h', 'rsw_a', 'win_pct_close_h', 'win_pct_close_a', 'sos_h', 'sos_a', 'mov_a_h', 'mov_a_a', 'injury_gmsc_h', 'injury_gmsc_a', 'injury_mins_h', 'injury_mins_a']

# define the required variables to be included in every combination
required_variables = ['spread', 'pace_h', 'pace_a', 'ortg_h', 'ortg_a', 'drb_h', 'drb_a', 'threePAR_h', 'threePAR_a', 'ts_h', 'ts_a', 'ftr_h', 'ftr_a', 'd_tov_h', 'd_tov_a', 'o_tov_h', 'o_tov_a', 'ftperfga_h', 'ftperfga_a', 'points_over_average_ratio_h', 'points_over_average_ratio_a', 'hotness_ratio_h', 'hotness_ratio_a', 'std_dev_h', 'std_dev_a', 'win_pct_h', 'win_pct_a', 'rsw_h', 'rsw_a', 'ratings_2k_h', 'ratings_2k_a', 'win_pct_close_h', 'win_pct_close_a', 'sos_h', 'sos_a', 'mov_a_h', 'mov_a_a', 'injury_mins_h', 'injury_mins_a', 'drtg_h', 'drtg_a']

# best_combo = ['total', 'size_of_spread', 'pct_overs_hit', 'ortg', 'drb', 'threePAR', 'ts', 'ftr', 'ftperfga', 'points_over_average_ratio', 'hotness_ratio', 'std_dev', 'win_pct', 'rsw', 'win_pct_close', 'injury_gmsc', 'injury_mins']

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
    history = model.fit(X_train, y_train, validation_split=0.2, epochs=100, verbose = 0, callbacks=[EarlyStopping(monitor = 'val_loss', restore_best_weights = True, patience=30), reduce_lr])

    # evaluate the model
    _, train_acc = model.evaluate(X_train, y_train, verbose=0)
    _, test_acc = model.evaluate(X_test, y_test, verbose=0)

    Y_proba = model.predict(X_test)

    print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

    acc_score = get_acc_score(Y_proba, y_test)

    print('Acc_score (threshold): %.3f' % acc_score)
    model.save('spread_model.h5')

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
import itertools

def get_best_combo(data, target, random_state=0):
    var_list = list(data.columns)
    var_pairs = set([v[:-2] for v in var_list if v.endswith(('_h', '_a'))])

    # Remove variables that can't be split up
    var_list = [v for v in var_list if not v.endswith(('_h', '_a'))]

    best_combo = None
    best_test_acc = 0
    best_acc_score = 0

    for combo_len in range(len(var_list)):
        for var_set in itertools.combinations(var_list, combo_len+1):
            # Check if variable pairs are split up
            split_pairs = var_pairs.intersection([v[:-2] for v in var_set])
            if any([p + '_h' not in var_set or p + '_a' not in var_set for p in split_pairs]):
                continue

            # Train and evaluate the model
            test_acc, acc_score = run_model(data, target, list(var_set), random_state)
            if test_acc > best_test_acc or (test_acc == best_test_acc and acc_score > best_acc_score):
                best_combo = var_set
                best_test_acc = test_acc
                best_acc_score = acc_score

    return best_combo, best_test_acc, best_acc_score

# get_best_combo()
run_model(all_input_variables, 25)