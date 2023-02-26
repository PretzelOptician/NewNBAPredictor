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
import math
from memory_profiler import profile

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


from tensorflow.keras import backend as K

import keras.backend as K

# def custom_loss(y_true, y_pred):
#     # tf.debugging.check_numerics(y_true, 'y_true contains NaN or inf')
#     # tf.debugging.check_numerics(y_pred, 'y_pred contains NaN or inf')
#     tf.print("y_pred values: ", tf.strings.as_string(y_pred))
#     tf.print("y_true: ", y_true)
#     y_true = tf.cast(y_true, dtype='float32')
#     prob = y_pred
#     flipped_prob = 1 - prob
#     diff_from_zero = prob - 0.5
#     over_50_percent = ((diff_from_zero+K.epsilon())/(K.abs(diff_from_zero+K.epsilon()))+1)/2
#     diff_from_zero = flipped_prob - 0.5
#     under_50_percent = ((diff_from_zero+K.epsilon())/(K.abs(diff_from_zero+K.epsilon()))+1)/2
#     absolute_probs = over_50_percent * prob + under_50_percent * flipped_prob
#     mean = K.mean(absolute_probs)
#     std_dev = K.std(absolute_probs)
#     threshold = mean + std_dev
#     print("threshold: ", threshold)

#     over = prob - threshold
#     # print("over: ", over)
#     under = flipped_prob - threshold

#     pred_over = (((over+K.epsilon()) / (K.abs(over + K.epsilon()))) + 1) / 2
#     # print("pred_over: ", pred_over)
#     pred_over_sum = K.sum(pred_over)
#     print("pred_over_sum: ", pred_over_sum)
#     pred_correct_over = pred_over * y_true
#     # print("pred_correct_over: ", pred_correct_over)
#     pred_over_sum_correct = K.sum(pred_correct_over)
#     print("pred_over_sum_correct: ", pred_over_sum_correct)

#     pred_under = (((under+K.epsilon()) / (K.abs(under + K.epsilon()))) + 1) / 2
#     # print("pred_under: ", pred_under)
#     pred_under_sum = K.sum(pred_under)
#     pred_correct_under = pred_under * (1 - y_true)
#     pred_under_sum_correct = K.sum(pred_correct_under)
#     if (pred_over_sum + pred_under_sum) == 0: acc = 0
#     acc = (pred_under_sum_correct + pred_over_sum_correct) / (pred_over_sum + pred_under_sum)
#     loss = 1 - acc

#     return loss

acc_scores = []

# load the training data from a file
df = pd.read_excel('./total_data.xlsx').fillna(value=0)

# extract the binary output variable from the dataframe
y = df['hitOver'].values

# extract all input variables from the dataframe
all_input_variables = ['total', 'totalppg', 'size_of_spread', 'pct_overs_hit', 'pace', 'ortg', 'drtg', 'drb', 'threePAR', 'ts', 'ftr', 'd_tov', 'o_tov', 'ftperfga', 'points_over_average_ratio', 'hotness_ratio', 'std_dev', 'win_pct', 'rsw', 'win_pct_close', 'mov_a', 'injury_gmsc', 'injury_mins']

# define the required variables to be included in every combination
required_variables = ['size_of_spread', 'threePAR', 'injury_mins', 'std_dev', 'hotness_ratio', 'points_over_average_ratio', 'ftr', 'pct_overs_hit', 'total']

# # print the 25 best combinations and their brier scores
# for i, (combination, acc_score) in enumerate(best_acc_scores):
#     print(f"{str(i+1)}. {combination} with accuracy of {acc_score}")
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping

best_acc = 0
total_combos = 12911
n = 0
for r in range(len(required_variables)+6, len(all_input_variables) - 1):
    combinations = itertools.combinations(all_input_variables, r)
    for combination in combinations:
        if not all(var in combination for var in required_variables):
            continue
        n += 1
        print("Now %.3f percent of the way through!" % (100*n/total_combos))
        X = df[list(combination)].values.astype(np.float32)
        X = StandardScaler().fit_transform(X)
        # y = StandardScaler().fit_transform(y.reshape(len(y),1))[:,0]
        # split training and testing data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2)

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
        print('Threshold accuracy score: %.3f' % (acc_score))

        acc_scores.append((combination, acc_score))
        sorted_acc_scores = sorted(acc_scores, key=lambda x: x[1], reverse=True)
        if len(sorted_acc_scores) > 50: 
            acc_scores = sorted_acc_scores[:50]

        if acc_score > best_acc: # plot loss during training
            print("Found new best combo! The combo for this was: ", list(combination))
    
            best_acc = acc_score
            best_combo = list(combination)
            model.save('totals_model.h5')
        del X

print(f"Best threshold test score was {best_acc} for variable combo {list(combination)}")
sorted_acc_scores = sorted(acc_scores, key=lambda x: x[1], reverse=True)
print("Top 50 combinations:")
for i in range(min(50, len(sorted_combined))):
    print(f"{i+1}. Combination: {sorted_combined[i][0]}\nAccuracy score: {sorted_combined[i][1]}\n")