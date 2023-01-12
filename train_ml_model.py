import pandas as pd
from keras.layers import Input, Dense
from keras.models import Model

## ALL CHATGPT CODE LMAO

# load the training data from a file
df = pd.read_excel('./spread_data.xlsx')

# extract input variables from the dataframe
X = df[['total', 'spread', 'pct_spreads_hit_h', 'pct_spreads_hit_a', 'ppg_h', 'ppg_a', 'pace_h', 'pace_a', 'ortg_h', 'ortg_a', 'drtg_h', 'drtg_a', 'drb_h', 'drb_a', 'threePAR_h', 'threePAR_a', 'ts_h', 'ts_a', 'ftr_h', 'ftr_a', 'd_tov_h', 'd_tov_a', 'o_tov_h', 'o_tov_a', 'ftperfga_h', 'ftperfga_a', 'points_over_average_ratio_h', 'points_over_average_ratio_a', 'hotness_ratio_h', 'hotness_ratio_a', 'std_dev_h', 'std_dev_a', 'win_pct_h', 'win_pct_a', 'rsw_h', 'rsw_a', 'ratings_2k_h', 'ratings_2k_a', 'win_pct_close_h', 'win_pct_close_a', 'sos_h', 'sos_a', 'mov_a_h', 'mov_a_a']].values

# extract the binary output variable from the dataframe
y = df['home_spread_hit'].values

# define the input shape
input_shape = (X.shape[1],)

# define the input layer
inputs = Input(shape=input_shape)

# define the hidden layer
hidden = Dense(8, activation='relu')(inputs)

# define the output layer
outputs = Dense(1, activation='sigmoid')(hidden)

# define the model
model = Model(inputs=inputs, outputs=outputs)

# compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the model to the training data
model.fit(X, y, epochs=10, batch_size=32)

# save the model to a file
model.save('model.h5')
