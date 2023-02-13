import pandas as pd
import itertools
import numpy as np
from keras.layers import Input, Dense
from keras.models import Model, load_model
from sklearn.model_selection import train_test_split

# load the training data from a file
df = pd.read_excel('./total_data.xlsx').fillna(value=0)

# extract the binary output variable from the dataframe
y = df['hitOver'].values

# extract all input variables from the dataframe
all_input_variables = ['total', 'totalppg', 'size_of_spread', 'pct_overs_hit', 'pace', 'ortg', 'drtg', 'drb', 'threePAR', 'ts', 'ftr', 'd_tov', 'o_tov', 'ftperfga', 'points_over_average_ratio', 'hotness_ratio', 'std_dev', 'win_pct', 'rsw', 'win_pct_close', 'mov_a', 'injury_gmsc', 'injury_mins']

# define the required variables to be included in every combination
required_variables = ['size_of_spread', 'threePAR', 'injury_mins', 'std_dev', 'hotness_ratio', 'points_over_average_ratio', 'ftr', 'pct_overs_hit', 'total']

# initialize a list to store the 25 best combinations with the corresponding brier scores
best_brier_scores = []

# try all combinations of input variables with required variables included
for r in range(len(required_variables)+2, len(all_input_variables) + 1):
    combinations = itertools.combinations(all_input_variables, r)
    for combination in combinations:
        if not all(var in combination for var in required_variables):
            continue

        X = df[list(combination)].values
        # split training and testing data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=22)

        # define the input shape
        input_shape = (X.shape[1],)

        # define the input layer
        inputs = Input(shape=input_shape)

        # define the hidden layer
        hidden1 = Dense(16, activation='relu')(inputs)
        hidden2 = Dense(24, activation='relu')(hidden1)

        # define the output layer
        outputs = Dense(1, activation='sigmoid')(hidden2)

        # define the model
        model = Model(inputs=inputs, outputs=outputs)

        # compile the model with mean squared error as the loss function
        model.compile(loss='binary_crossentropy', optimizer='adam')

        # fit the model to the training data
        model.fit(X_train, y_train, epochs=20, batch_size=128, validation_data=(X_test, y_test))

        # make predictions on all the data
        Y_proba = model.predict(X)
        df['ml_prob'] = Y_proba

        # calculate the brier score on the predictions
        brier_score = ((y - Y_proba) ** 2).mean()

        print("Current combination: ", combination)
        print("Brier score of this combination: ", brier_score)

        # add the current combination and brier score to the list of best brier
        best_brier_scores.append((combination, brier_score))

# sort the list of best brier scores in ascending order
best_brier_scores.sort(key=lambda x: x[1])

# keep only the top 25 combinations with the best brier scores
best_brier_scores = best_brier_scores[:25]

# print the 25 best combinations and their brier scores
print("[")
for i, (combination, brier_score) in enumerate(best_brier_scores):
    print(f"[{combination}],")
print("]")