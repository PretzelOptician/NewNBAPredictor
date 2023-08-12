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
INT_MAX = float(1e50)

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

def get_season_balance(Y_proba, y_true): 
    balance = 1
    for i, result in enumerate(Y_proba, start=len(Y_proba)-500): 
        try: 
            if Y_proba[i] > 0.5236: 
                bet = (Y_proba[i] - (1 - Y_proba[i])/0.91)*balance
                print(f"Betting over on game {i} with bet as {100*bet}% of original balance.")
                if y_true[i] == 1: 
                    balance += 0.91*bet
                    print(f"Bet won! Now have {100*balance}% of original balance left.")
                else: 
                    balance -= bet
                    print(f"Bet lost! Now have {100*balance}% of original balance left.")
            elif Y_proba[i] < 0.4764: 
                bet = ((1 - Y_proba[i]) - (Y_proba[i])/0.91)*balance
                print(f"Betting under on game {i} with bet as {100*bet}% of original balance.")
                if y_true[i] == 0: 
                    balance += 0.91*bet
                    print(f"Bet won! Now have {100*balance}% of original balance left.")
                else: 
                    balance -= bet
                    print(f"Bet lost! Now have {100*balance}% of original balance left.")
            if balance <= 0.001: 
                print(f"Ran out of money on game {i} :(")
                return 0.0
        except IndexError: 
            return balance
    return balance

# load the training data from a file
df = pd.read_excel('./historic_data/total_data.xlsx').fillna(value=0)

# extract the binary output variable from the dataframe
y = df['hitOver'].values
y = y.astype(float)

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

def profit_loss_kelly_criterion(y_true, y_pred): 
    over_bet = 1 / (tf.ones_like(y_pred) + tf.exp(-(y_pred - tf.fill(tf.shape(y_pred), 0.5236)) * INT_MAX)) #PRODUCES A TENSOR THAT IS 1 IF THE PROBABILITY IS GREATER THAN 0.5236 AND 0 OTHERWISE
    under_bet = 1 / (tf.ones_like(y_pred) + tf.exp(-((tf.ones_like(y_pred) - y_pred) - tf.fill(tf.shape(y_pred), 0.5236)) * INT_MAX)) #PRODUCES A TENSOR THAT IS 1 IF THE PROBABILITY IS LESS THAN 0.4764 AND 0 OTHERWISE
    profit_if_over_bet_and_loss = -1*((y_pred) - (tf.ones_like(y_pred) - y_pred)/0.91)
    profit_if_over_bet_and_win = 0.91*((y_pred) - (tf.ones_like(y_pred) - y_pred)/0.91)
    profit_if_over_bet = profit_if_over_bet_and_win*y_true + profit_if_over_bet_and_loss*(tf.ones_like(y_true) - y_true)
    profit_if_under_bet_and_loss = -1*((tf.ones_like(y_pred) - y_pred) - y_pred/0.91)
    profit_if_under_bet_and_win = 0.91*((tf.ones_like(y_pred) - y_pred) - y_pred/0.91)
    profit_if_under_bet = profit_if_under_bet_and_win*(tf.ones_like(y_true) - y_true) + profit_if_under_bet_and_loss*y_true
    profit = profit_if_over_bet*over_bet + profit_if_under_bet*under_bet
    return -1*profit

def custom_mse(y_true, y_pred): 
    # over_bet = 1 / (tf.ones_like(y_pred) + tf.exp(-(y_pred - tf.fill(tf.shape(y_pred), 0.5236)) * INT_MAX)) #PRODUCES A TENSOR THAT IS 1 IF THE PROBABILITY IS GREATER THAN 0.5236 AND 0 OTHERWISE
    over_bet = (1 + y_true)
    return tf.reduce_mean(over_bet)
    diff = y_true - y_pred
    return tf.reduce_mean(sq)
    return tf.reduce_mean(tf.math.square(y_true - y_pred))
    # over_bet = 1 / (tf.ones_like(y_pred) + tf.exp(-(y_pred - tf.fill(tf.shape(y_pred), 0.5236)) * INT_MAX)) #PRODUCES A TENSOR THAT IS 1 IF THE PROBABILITY IS GREATER THAN 0.5236 AND 0 OTHERWISE
    # under_bet = 1 / (tf.ones_like(y_pred) + tf.exp(-((tf.ones_like(y_pred) - y_pred) - tf.fill(tf.shape(y_pred), 0.5236)) * INT_MAX)) #PRODUCES A TENSOR THAT IS 1 IF THE PROBABILITY IS LESS THAN 0.4764 AND 0 OTHERWISE
    # profit_if_over_bet_and_loss = -1*((y_pred) - (tf.ones_like(y_pred) - y_pred)/0.91)
    # profit_if_over_bet_and_win = 0.91*((y_pred) - (tf.ones_like(y_pred) - y_pred)/0.91)
    # profit_if_over_bet = profit_if_over_bet_and_win*y_true + profit_if_over_bet_and_loss*(tf.ones_like(y_true) - y_true)
    # profit_if_under_bet_and_loss = -1*((tf.ones_like(y_pred) - y_pred) - y_pred/0.91)
    # profit_if_under_bet_and_win = 0.91*((tf.ones_like(y_pred) - y_pred) - y_pred/0.91)
    # profit_if_under_bet = profit_if_under_bet_and_win*(tf.ones_like(y_true) - y_true) + profit_if_under_bet_and_loss*y_true
    # print(-1*profit_if_over_bet*over_bet + -1*profit_if_under_bet*under_bet)
    # return tf.reduce_mean(over_bet)

def profit_loss(y_true, y_pred):
    sign_tensor = 1 / (tf.ones_like(y_pred) + tf.exp(-y_pred * float('inf')))
    loss = -y_pred * (1.91 * y_true - tf.ones_like(y_pred) + 0.09 * (tf.ones_like(y_pred) - sign_tensor))
    print(loss)
    return loss

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
    hidden2 = Dense(100, activation='relu')(hidden1)
    hidden3 = Dense(50, activation='relu')(hidden2)

    # define the output layer probability
    outputs = Dense(1, activation='sigmoid')(hidden3)

    # define the model
    model = Model(inputs=inputs, outputs=outputs)

    opt = SGD(learning_rate=0.01, momentum=0.9)
    model.compile(loss=custom_mse, optimizer=opt, metrics=['accuracy'], run_eagerly=True)

    # fit the model to the training data with early stopping and a validation split
    history = model.fit(X_train, y_train, validation_split=0.2, epochs=300, batch_size=512, verbose = 0, callbacks=[EarlyStopping(monitor = 'val_loss', restore_best_weights = True, patience=30), reduce_lr])

    # evaluate the model
    _, train_acc = model.evaluate(X_train, y_train, verbose=0)
    _, test_acc = model.evaluate(X_test, y_test, verbose=0)
    
    Y_proba = model.predict(X_test)
    print(Y_proba)
    Y_all_predict = model.predict(X)
    df['balance_to_place'] = Y_all_predict

    df.to_excel('./historic_data/total_data.xlsx')

    print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

    season_balance = 100*get_season_balance(Y_proba, y_test)
    print(f'Percent of original balance remaining after simulating last 500 games with model: {season_balance}%.')

    # print('Acc_score (threshold): %.3f' % acc_score)
    # print(f'Mean was {mean} with a standard deviation of {std_dev}!')
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

    return season_balance

# get_best_combo()
run_model(all_input_variables, 20)
# new_tensor = tf.constant([[0.45], [0.51], [0.52], [0.56], [0.3]])
# true = tf.constant([[0.0], [0.0], [0.0], [1.0], [1.0]])
# profit_loss_kelly_criterion(true, new_tensor)