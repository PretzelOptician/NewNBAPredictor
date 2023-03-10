import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import StandardScaler

TOTALS_MEAN = 0.4932219
TOTALS_STD_DEV = 0.026691532448322754
SPREAD_MEAN = None
SPREAD_STD_DEV = None

def apply_total_ml_model(df): 
    # load the model from the file
    model = load_model('totals_model.h5')
    X_new = df[['total', 'size_of_spread', 'pct_overs_hit', 'ortg', 'drb', 'threePAR', 'ts', 'ftr', 'ftperfga', 'points_over_average_ratio', 'hotness_ratio', 'std_dev', 'win_pct', 'rsw', 'win_pct_close', 'injury_gmsc', 'injury_mins']].values
    X_new = StandardScaler().fit_transform(X_new)
    print(X_new)
    # use the model to predict the probability of the binary value being 1 for the new data points
    y_proba = model.predict(X_new)
    print(y_proba)
    df['ml_prob'] = y_proba
    return df

def apply_spread_ml_model(df): 
    # load the model from the file
    model = load_model('model.h5')

    # extract input variables from the new dataframe
    X_new = df[['total', 'spread', 'pct_spreads_hit_h', 'pct_spreads_hit_a', 'ppg_h', 'ppg_a', 'pace_h', 'pace_a', 'ortg_h', 'ortg_a', 'drtg_h', 'drtg_a', 'drb_h', 'drb_a', 'threePAR_h', 'threePAR_a', 'ts_h', 'ts_a', 'ftr_h', 'ftr_a', 'd_tov_h', 'd_tov_a', 'o_tov_h', 'o_tov_a', 'ftperfga_h', 'ftperfga_a', 'points_over_average_ratio_h', 'points_over_average_ratio_a', 'hotness_ratio_h', 'hotness_ratio_a', 'std_dev_h', 'std_dev_a', 'win_pct_h', 'win_pct_a', 'rsw_h', 'rsw_a', 'win_pct_close_h', 'win_pct_close_a', 'sos_h', 'sos_a', 'mov_a_h', 'mov_a_a', 'injury_gmsc_h', 'injury_gmsc_a', 'injury_mins_h', 'injury_mins_a']].values
    X_new = StandardScaler().fit_transform(X_new)
    print(X_new)

    # use the model to predict the probability of the binary value being 1 for the new data points
    y_proba = model.predict(X_new)

    df['ml_prob'] = y_proba
    print(y_proba)
    return df

def main(): 
    team_name_mapping = {
        "LALakers": "LA Lakers",
        "GoldenState": "Golden State",
        "LAClippers": "LA Clippers", 
        "NewOrleans": "New Orleans", 
        "SanAntonio": "San Antonio", 
        "OklahomaCity": "Oklahoma City", 
        "NewYork": "New York"
    }
    df_total = pd.read_excel('current_games_total.xlsx')
    df_total = apply_total_ml_model(df_total)
    # df_spread = pd.read_excel('current_games_spread.xlsx')
    # df_spread = apply_spread_ml_model(df_spread)
    for x in range(df_total.shape[0]):
        total = df_total.at[x, 'total'] 
        over_prob = df_total.at[x, 'ml_prob']
        letter = 'o' if over_prob > 0.5 else 'u'
        away_team = team_name_mapping.get(df_total.at[x, 'away_team'], df_total.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_total.at[x, 'home_team'], df_total.at[x, 'home_team'])
        pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
        print(f'{away_team} at {home_team}: {letter}{str(total)} with probability {pct}%')
    # print(df_spread)
    #SPREAD
    # for x in range(df_spread.shape[0]): 
    #     spread = df_spread.at[x, 'spread']
    #     home_prob = df_spread.at[x, 'ml_prob']
    #     away_team = team_name_mapping.get(df_spread.at[x, 'away_team'], df_spread.at[x, 'away_team'])
    #     home_team = team_name_mapping.get(df_spread.at[x, 'home_team'], df_spread.at[x, 'home_team'])
    #     cover = home_team if home_prob > 0.5 else away_team
    #     pct = str(home_prob*100) if cover == home_team else str(100-home_prob*100)
    #     pm = '-' if (spread < 0 and cover == home_team) or (spread > 0 and cover==away_team) else '+'
    #     spread_string = str(abs(spread)) if (spread*2)%2==1 else str(abs(int(spread)))
    #     print(f'{away_team} at {home_team}: {cover} {pm}{spread_string} with probability {pct}%')
    print("\n   Bets greater than the threshold: ")
    for x in range(df_total.shape[0]): 
        total = df_total.at[x, 'total'] 
        over_prob = df_total.at[x, 'ml_prob']
        letter = 'o' if over_prob > 0.5 else 'u'
        away_team = team_name_mapping.get(df_total.at[x, 'away_team'], df_total.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_total.at[x, 'home_team'], df_total.at[x, 'home_team'])
        dist_from_mean = abs(over_prob - TOTALS_MEAN)
        pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
        if float(dist_from_mean) > TOTALS_STD_DEV: 
            print(f'{away_team} at {home_team}: {letter}{str(total)} with probability {pct}%')
    # for x in range(df_spread.shape[0]): 
    #     spread = df_spread.at[x, 'spread']
    #     home_prob = df_spread.at[x, 'ml_prob']
    #     away_team = team_name_mapping.get(df_spread.at[x, 'away_team'], df_spread.at[x, 'away_team'])
    #     home_team = team_name_mapping.get(df_spread.at[x, 'home_team'], df_spread.at[x, 'home_team'])
    #     cover = home_team if home_prob > 0.5 else away_team
    #     pct = str(home_prob*100) if cover == home_team else str(100-home_prob*100)
    #     pm = '-' if (spread < 0 and cover == home_team) or (spread > 0 and cover==away_team) else '+'
    #     spread_string = str(abs(spread)) if (spread*2)%2==1 else str(abs(int(spread)))
    #     if float(pct) > 58: 
    #         print(f'{away_team} at {home_team}: {cover} {pm}{spread_string} with probability {pct}%')


    top_bet_index = 0
    top_bet_pct = 0.0
    top_bet_ou = True
    for x in range(df_total.shape[0]): 
        total = df_total.at[x, 'total'] 
        over_prob = df_total.at[x, 'ml_prob']
        letter = 'o' if over_prob > 0.5 else 'u'
        away_team = team_name_mapping.get(df_total.at[x, 'away_team'], df_total.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_total.at[x, 'home_team'], df_total.at[x, 'home_team'])
        pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
        if float(pct) > top_bet_pct: 
            top_bet_pct = float(pct)
            top_bet_index = x
            top_bet_ou = True
    # for x in range(df_spread.shape[0]): 
    #     # spread = df_spread.at[x, 'spread']
    #     home_prob = df_spread.at[x, 'ml_prob']
    #     away_team = team_name_mapping.get(df_spread.at[x, 'away_team'], df_spread.at[x, 'away_team'])
    #     home_team = team_name_mapping.get(df_spread.at[x, 'home_team'], df_spread.at[x, 'home_team'])
    #     cover = home_team if home_prob > 0.5 else away_team
    #     pct = str(home_prob*100) if cover == home_team else str(100-home_prob*100)
    #     # pm = '-' if (spread < 0 and cover == home_team) or (spread > 0 and cover==away_team) else '+'
    #     if float(pct) > top_bet_pct: 
    #         top_bet_pct = float(pct)
    #         top_bet_index = x
    #         top_bet_ou = False
    if top_bet_ou: 
        x = top_bet_index
        total = df_total.at[x, 'total'] 
        over_prob = df_total.at[x, 'ml_prob']
        letter = 'o' if over_prob > 0.5 else 'u'
        away_team = df_total.at[x, 'away_team']
        home_team = df_total.at[x, 'home_team']
        pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
        pick_string = f"{away_team}@{home_team} {letter}{total}"
    else: 
        x = top_bet_index
        # spread = df_spread.at[x, 'spread']
        # home_prob = df_spread.at[x, 'ml_prob']
        # away_team = df_spread.at[x, 'away_team']
        # home_team = df_spread.at[x, 'home_team']
        # cover = home_team if home_prob > 0.5 else away_team
        # pct = str(home_prob*100) if cover == home_team else str(100-home_prob*100)
        # pm = '-' if (spread < 0 and cover == home_team) or (spread > 0 and cover==away_team) else '+'
        # spread_string = str(abs(spread)) if (spread*2)%2==1 else str(abs(int(spread)))
        # pick_string = f"{away_team}@{home_team} {cover} {pm}{spread_string}"
    print("\n")
    # print("Generating tweet... \n")
    # run_tweet_gen(pick_string, round(float(pct), 2))

main()