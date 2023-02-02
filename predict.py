import pandas as pd
from keras.models import load_model

# load the model from the file
model = load_model('model.h5')

# load the data for which you want to make predictions
df_new = pd.read_excel('./current_games_spread.xlsx').fillna(value=0)

# extract input variables from the new dataframe
X_new = df_new[['total', 'spread', 'pct_spreads_hit_h', 'pct_spreads_hit_a', 'ppg_h', 'ppg_a', 'pace_h', 'pace_a', 'ortg_h', 'ortg_a', 'drtg_h', 'drtg_a', 'drb_h', 'drb_a', 'threePAR_h', 'threePAR_a', 'ts_h', 'ts_a', 'ftr_h', 'ftr_a', 'd_tov_h', 'd_tov_a', 'o_tov_h', 'o_tov_a', 'ftperfga_h', 'ftperfga_a', 'points_over_average_ratio_h', 'points_over_average_ratio_a', 'hotness_ratio_h', 'hotness_ratio_a', 'std_dev_h', 'std_dev_a', 'win_pct_h', 'win_pct_a', 'rsw_h', 'rsw_a', 'win_pct_close_h', 'win_pct_close_a', 'sos_h', 'sos_a', 'mov_a_h', 'mov_a_a', 'injury_gmsc_h', 'injury_gmsc_a', 'injury_mins_h', 'injury_mins_a']].values

# use the model to predict the probability of the binary value being 1 for the new data points
y_proba = model.predict(X_new)

df_new['ml_prob'] = y_proba

df_new.to_excel("./ml_spread_probs.xlsx")

print(y_proba)