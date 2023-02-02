import pandas as pd
from random import random

all_data = pd.read_excel('./spread_data.xlsx')
test_data = pd.DataFrame({'year': [], 'home_spread_hit': [], 'total': [], 'spread': [], 'home_team': [], 'away_team': [], 'pct_spreads_hit_h': [], 'pct_spreads_hit_a': [], 'ppg_h': [], 'ppg_a': [], 'pace_h': [], 'pace_a': [], 'ortg_h': [], 'ortg_a': [], 'drtg_h': [], 'drtg_a': [], 'drb_h': [], 'drb_a': [], 'threePAR_h': [], 'threePAR_a': [], 'ts_h': [], 'ts_a': [], 'ftr_h': [], 'ftr_a': [], 'd_tov_h': [], 'd_tov_a': [], 'o_tov_h': [], 'o_tov_a': [], 'ftperfga_h': [], 'ftperfga_a': [], 'points_over_average_ratio_h': [], 'points_over_average_ratio_a': [], 'hotness_ratio_h': [], 'hotness_ratio_a': [], 'std_dev_h': [], 'std_dev_a': [], 'win_pct_h': [], 'win_pct_a': [], 'rsw_h': [], 'rsw_a': [], 'ratings_2k_h': [], 'ratings_2k_a': [], 'win_pct_close_h': [], 'win_pct_close_a': [], 'sos_h': [], 'sos_a': [], 'mov_a_h': [], 'mov_a_a': [], 'injury_gmsc_h': [], 'injury_gmsc_a': [], 'injury_mins_h': [], 'injury_mins_a': []})
train_data = pd.DataFrame({'year': [], 'home_spread_hit': [], 'total': [], 'spread': [], 'home_team': [], 'away_team': [], 'pct_spreads_hit_h': [], 'pct_spreads_hit_a': [], 'ppg_h': [], 'ppg_a': [], 'pace_h': [], 'pace_a': [], 'ortg_h': [], 'ortg_a': [], 'drtg_h': [], 'drtg_a': [], 'drb_h': [], 'drb_a': [], 'threePAR_h': [], 'threePAR_a': [], 'ts_h': [], 'ts_a': [], 'ftr_h': [], 'ftr_a': [], 'd_tov_h': [], 'd_tov_a': [], 'o_tov_h': [], 'o_tov_a': [], 'ftperfga_h': [], 'ftperfga_a': [], 'points_over_average_ratio_h': [], 'points_over_average_ratio_a': [], 'hotness_ratio_h': [], 'hotness_ratio_a': [], 'std_dev_h': [], 'std_dev_a': [], 'win_pct_h': [], 'win_pct_a': [], 'rsw_h': [], 'rsw_a': [], 'ratings_2k_h': [], 'ratings_2k_a': [], 'win_pct_close_h': [], 'win_pct_close_a': [], 'sos_h': [], 'sos_a': [], 'mov_a_h': [], 'mov_a_a': [], 'injury_gmsc_h': [], 'injury_gmsc_a': [], 'injury_mins_h': [], 'injury_mins_a': []})
for row in range(all_data.shape[0]): 
    randy = random()
    if randy < 0.05: #testing data
        print(f"Adding row {str(row)} to testing data!")
        entry = all_data.iloc[row]
        test_data = test_data.append( [entry] )
    else: 
        print(f"Adding row {str(row)} to training data!")
        entry = all_data.iloc[row]
        train_data = train_data.append( [entry] )
test_data.to_excel('./spread_test_data.xlsx')
train_data.to_excel('./spread_train_data.xlsx')
