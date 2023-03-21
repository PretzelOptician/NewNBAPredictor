import pandas as pd
import numpy as np
from tweet_generator import *
# from injuryv2 import *

def logit_total(df):     
    #chatGPT code:: 
    # Extract the relevant columns from the dataframe
    X = df[['total', 'size_of_spread', 'pct_overs_hit', 'ortg', 'drtg', 'drb', 'threePAR', 'ts', 'ftr', 'points_over_average_ratio', 'hotness_ratio', 'std_dev']]
    # Add a column of consts to the dataframe to represent the intercept term
    X['intercept'] = 4.644535
    coefs = [0.0040295, 0.0120225, -0.392392, 0.028596,  -0.0214184, -0.0128709, 0.8110862, -6.346099, -0.7018032, -2.42325, 0.5000966, 0.0161823, 1]
    z = np.dot(X, coefs)
    prob = 1 / (1 + np.exp(-z))
    # Calculate the probability using the sigmoid function
    df['calc_over_prob'] = prob
    return df

def average(numbers): 
    sum = 0
    for x in numbers: 
        sum += x
    if sum == 0: 
        return 0
    else: 
        return float(sum/len(numbers))

def logit_spread(df): 
    X = df[['spread', 'pace_h', 'pace_a', 'ortg_h', 'ortg_a', 'drb_h', 'drb_a', 'threePAR_h', 'threePAR_a', 'ts_h', 'ts_a', 'ftr_h', 'ftr_a', 'd_tov_h', 'd_tov_a', 'o_tov_h', 'o_tov_a', 'ftperfga_h', 'ftperfga_a', 'points_over_average_ratio_h', 'points_over_average_ratio_a', 'hotness_ratio_h', 'hotness_ratio_a', 'std_dev_h', 'std_dev_a', 'win_pct_h', 'win_pct_a', 'rsw_h', 'rsw_a', 'ratings_2k_h', 'ratings_2k_a', 'win_pct_close_h', 'win_pct_close_a', 'sos_h', 'sos_a', 'mov_a_h', 'mov_a_a', 'injury_mins_h', 'injury_mins_a', 'drtg_h', 'drtg_a']]
    X['intercept'] = -0.1662377
    coefs = [0.004023, 0.0360045, -0.0269394, 0.0630027, -0.0104669, 0.0110417, -0.0077624, 0.9284867, -1.350638, -7.07015, 0.9263744, -2.08019, 0.1163992, 0.0513194, 0.0351266, 0.0091355, -0.0273747, 2.851526, 0.2861693, -4.865999, 1.248197, -0.4978895, 0.0724876, 0.0134026, 0.0150962, 0.2478499, 0.6733762, 0.0046755, 0.0079782, 0.0256954, -0.0318087, 0.1798136, -0.74373, -0.1768355, -0.1041935, -0.010406, -0.0071341, -0.5646092, 0.0187997, 0.0012492, -0.0062607, 1]
    z = np.dot(X, coefs)
    prob = 1 / (1 + np.exp(-z))
    df['calc_home_prob'] = prob
    return df

def get_regression_probs(notweet=False): 

    team_names = [ "Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]
    total_data = pd.read_excel('./current_games_total.xlsx')
    spread_data = pd.read_excel('./current_games_spread.xlsx')
    team_name_mapping = {
        "LALakers": "LA Lakers",
        "GoldenState": "Golden State",
        "LAClippers": "LA Clippers", 
        "NewOrleans": "New Orleans", 
        "SanAntonio": "San Antonio", 
        "OklahomaCity": "Oklahoma City", 
        "NewYork": "New York"
    }
    df_total = logit_total(total_data)
    df_spread = logit_spread(spread_data)
    for x in range(df_total.shape[0]):
        total = df_total.at[x, 'total'] 
        over_prob = df_total.at[x, 'calc_over_prob']
        letter = 'o' if over_prob > 0.5 else 'u'
        away_team = team_name_mapping.get(df_total.at[x, 'away_team'], df_total.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_total.at[x, 'home_team'], df_total.at[x, 'home_team'])
        pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
        print(f'{away_team} at {home_team}: {letter}{str(total)} with probability {pct}%')
    # print(df_spread)
    #SPREAD
    for x in range(df_spread.shape[0]): 
        spread = df_spread.at[x, 'spread']
        home_prob = df_spread.at[x, 'calc_home_prob']
        away_team = team_name_mapping.get(df_spread.at[x, 'away_team'], df_spread.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_spread.at[x, 'home_team'], df_spread.at[x, 'home_team'])
        cover = home_team if home_prob > 0.5 else away_team
        pct = str(home_prob*100) if cover == home_team else str(100-home_prob*100)
        pm = '-' if (spread < 0 and cover == home_team) or (spread > 0 and cover==away_team) else '+'
        spread_string = str(abs(spread)) if (spread*2)%2==1 else str(abs(int(spread)))
        print(f'{away_team} at {home_team}: {cover} {pm}{spread_string} with probability {pct}%')
    print("\n   Bets greater than 53%: ")
    for x in range(df_total.shape[0]): 
        total = df_total.at[x, 'total'] 
        over_prob = df_total.at[x, 'calc_over_prob']
        letter = 'o' if over_prob > 0.5 else 'u'
        away_team = team_name_mapping.get(df_total.at[x, 'away_team'], df_total.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_total.at[x, 'home_team'], df_total.at[x, 'home_team'])
        pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
        if float(pct) > 53: 
            print(f'{away_team} at {home_team}: {letter}{str(total)} with probability {pct}%')
    for x in range(df_spread.shape[0]): 
        spread = df_spread.at[x, 'spread']
        home_prob = df_spread.at[x, 'calc_home_prob']
        away_team = team_name_mapping.get(df_spread.at[x, 'away_team'], df_spread.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_spread.at[x, 'home_team'], df_spread.at[x, 'home_team'])
        cover = home_team if home_prob > 0.5 else away_team
        pct = str(home_prob*100) if cover == home_team else str(100-home_prob*100)
        pm = '-' if (spread < 0 and cover == home_team) or (spread > 0 and cover==away_team) else '+'
        spread_string = str(abs(spread)) if (spread*2)%2==1 else str(abs(int(spread)))
        if float(pct) > 53: 
            print(f'{away_team} at {home_team}: {cover} {pm}{spread_string} with probability {pct}%')


    top_bet_index = 0
    top_bet_pct = 0.0
    top_bet_ou = True
    for x in range(df_total.shape[0]): 
        total = df_total.at[x, 'total'] 
        over_prob = df_total.at[x, 'calc_over_prob']
        letter = 'o' if over_prob > 0.5 else 'u'
        away_team = team_name_mapping.get(df_total.at[x, 'away_team'], df_total.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_total.at[x, 'home_team'], df_total.at[x, 'home_team'])
        pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
        if float(pct) > top_bet_pct: 
            top_bet_pct = float(pct)
            top_bet_index = x
            top_bet_ou = True
    for x in range(df_spread.shape[0]): 
        # spread = df_spread.at[x, 'spread']
        home_prob = df_spread.at[x, 'calc_home_prob']
        away_team = team_name_mapping.get(df_spread.at[x, 'away_team'], df_spread.at[x, 'away_team'])
        home_team = team_name_mapping.get(df_spread.at[x, 'home_team'], df_spread.at[x, 'home_team'])
        cover = home_team if home_prob > 0.5 else away_team
        pct = str(home_prob*100) if cover == home_team else str(100-home_prob*100)
        # pm = '-' if (spread < 0 and cover == home_team) or (spread > 0 and cover==away_team) else '+'
        if float(pct) > top_bet_pct: 
            top_bet_pct = float(pct)
            top_bet_index = x
            top_bet_ou = False
    if top_bet_ou: 
        x = top_bet_index
        total = df_total.at[x, 'total'] 
        over_prob = df_total.at[x, 'calc_over_prob']
        letter = 'o' if over_prob > 0.5 else 'u'
        away_team = df_total.at[x, 'away_team']
        home_team = df_total.at[x, 'home_team']
        pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
        pick_string = f"{away_team}@{home_team} {letter}{total}"
    else: 
        x = top_bet_index
        spread = df_spread.at[x, 'spread']
        home_prob = df_spread.at[x, 'calc_home_prob']
        away_team = df_spread.at[x, 'away_team']
        home_team = df_spread.at[x, 'home_team']
        cover = home_team if home_prob > 0.5 else away_team
        pct = str(home_prob*100) if cover == home_team else str(100-home_prob*100)
        pm = '-' if (spread < 0 and cover == home_team) or (spread > 0 and cover==away_team) else '+'
        spread_string = str(abs(spread)) if (spread*2)%2==1 else str(abs(int(spread)))
        pick_string = f"{away_team}@{home_team} {cover} {pm}{spread_string}"
    if not notweet: 
        print("\n")
        print("Generating tweet... \n")
        run_tweet_gen(pick_string, round(float(pct), 2), 'regression')