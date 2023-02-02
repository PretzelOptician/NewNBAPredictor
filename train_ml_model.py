import pandas as pd
from keras.layers import Input, Dense
from keras.models import Model
from sklearn.model_selection import train_test_split


## ALL CHATGPT CODE LMAO

# load the training data from a file
df = pd.read_excel('./spread_data_large_fixed.xlsx').fillna(value=0)

# extract input variables from the dataframe
X = df[['total', 'spread', 'pct_spreads_hit_h', 'pct_spreads_hit_a', 'ppg_h', 'ppg_a', 'pace_h', 'pace_a', 'ortg_h', 'ortg_a', 'drtg_h', 'drtg_a', 'drb_h', 'drb_a', 'threePAR_h', 'threePAR_a', 'ts_h', 'ts_a', 'ftr_h', 'ftr_a', 'd_tov_h', 'd_tov_a', 'o_tov_h', 'o_tov_a', 'ftperfga_h', 'ftperfga_a', 'points_over_average_ratio_h', 'points_over_average_ratio_a', 'hotness_ratio_h', 'hotness_ratio_a', 'std_dev_h', 'std_dev_a', 'win_pct_h', 'win_pct_a', 'rsw_h', 'rsw_a', 'win_pct_close_h', 'win_pct_close_a', 'sos_h', 'sos_a', 'mov_a_h', 'mov_a_a', 'injury_gmsc_h', 'injury_gmsc_a', 'injury_mins_h', 'injury_mins_a']].values

# extract the binary output variable from the dataframe
y = df['home_spread_hit'].values

# split training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# define the input shape
input_shape = (X.shape[1],)

# define the input layer
inputs = Input(shape=input_shape)

# define the hidden layer
hidden1 = Dense(24, activation='relu')(inputs)

# define the output layer
outputs = Dense(1, activation='sigmoid')(hidden1)

# define the model
model = Model(inputs=inputs, outputs=outputs)

# compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the model to the training data
model.fit(X, y, epochs=12, batch_size=32)

# save the model to a file
model.save('model.h5')
