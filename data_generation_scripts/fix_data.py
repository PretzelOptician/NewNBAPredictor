## THIS SCRIPT IS FOR EDITING THE LARGE SAMPLE SIZE DATA (SOME STUFF IS MISSING)

import pandas as pd

def get_rsw_odds_excel(year): 
    filepath = f'../rsw_odds/{year}.xlsx'
    df = pd.read_excel(filepath)
    return df

def get_mov_excel(year): 
    filepath = f'../mov_ratings/{year}.xlsx'
    df = pd.read_excel(filepath)
    return df

rsw_odds = {}
for year in range(2008, 2024): 
    df = get_rsw_odds_excel(year)
    rsw_odds[year] = df
    print("Generated pre-season odds for year " + str(year) + "...")

movs = {}
for year in range(2007, 2023): 
    df = get_mov_excel(year)
    movs[year] = df
    print("Generated MOV ratings for year " + str(year) + "...")

spread_data = pd.read_excel('../historic_data/spread_data.xlsx')

#exclude ratings_2k because the data doesn't exist before 2013
spread_data = spread_data[['year', 'home_spread_hit', 'total', 'spread', 'home_team', 'away_team', 'pct_spreads_hit_h', 'pct_spreads_hit_a', 'ppg_h', 'ppg_a', 'pace_h', 'pace_a', 'ortg_h', 'ortg_a', 'drtg_h', 'drtg_a', 'drb_h', 'drb_a', 'threePAR_h', 'threePAR_a', 'ts_h', 'ts_a', 'ftr_h', 'ftr_a', 'd_tov_h', 'd_tov_a', 'o_tov_h', 'o_tov_a', 'ftperfga_h', 'ftperfga_a', 'points_over_average_ratio_h', 'points_over_average_ratio_a', 'hotness_ratio_h', 'hotness_ratio_a', 'std_dev_h', 'std_dev_a', 'win_pct_h', 'win_pct_a', 'rsw_h', 'rsw_a', 'win_pct_close_h', 'win_pct_close_a', 'sos_h', 'sos_a', 'mov_a_h', 'mov_a_a', 'injury_gmsc_h', 'injury_gmsc_a', 'injury_mins_h', 'injury_mins_a']]

for row in range(spread_data.shape[0]): 
    home_team = spread_data.at[row, 'home_team']
    away_team = spread_data.at[row, 'away_team']
    year = spread_data.at[row, 'year']
    if spread_data.at[row, 'rsw_h'] == 0: 
        preseason_odds = rsw_odds[year]
        if home_team == "NewJersey": 
            for team in range(preseason_odds.shape[0]): 
                if preseason_odds.at[team, 'Team'] == "New Jersey Nets": 
                    spread_data.at[row, 'rsw_h'] = preseason_odds.at[team, 'W-L O/U']
        elif home_team == "Seattle": 
            for team in range(preseason_odds.shape[0]): 
                if preseason_odds.at[team, 'Team'] == "Seattle SuperSonics": 
                    spread_data.at[row, 'rsw_h'] = preseason_odds.at[team, 'W-L O/U']
        elif home_team == "NewOrleans": 
            for team in range(preseason_odds.shape[0]): 
                if preseason_odds.at[team, 'Team'] == "New Orleans Hornets": 
                    spread_data.at[row, 'rsw_h'] = preseason_odds.at[team, 'W-L O/U']
    if spread_data.at[row, 'rsw_a'] == 0: 
        preseason_odds = rsw_odds[year]
        if away_team == "NewJersey": 
            for team in range(preseason_odds.shape[0]): 
                if preseason_odds.at[team, 'Team'] == "New Jersey Nets": 
                    spread_data.at[row, 'rsw_a'] = preseason_odds.at[team, 'W-L O/U']
        elif away_team == "Seattle": 
            for team in range(preseason_odds.shape[0]): 
                if preseason_odds.at[team, 'Team'] == "Seattle SuperSonics": 
                    spread_data.at[row, 'rsw_a'] = preseason_odds.at[team, 'W-L O/U']
        elif away_team == "NewOrleans": 
            for team in range(preseason_odds.shape[0]): 
                if preseason_odds.at[team, 'Team'] == "New Orleans Hornets": 
                    spread_data.at[row, 'rsw_a'] = preseason_odds.at[team, 'W-L O/U']
    if spread_data.at[row, 'mov_a_h'] == 0: 
        mov_ratings_for_year = movs[year-1]
        if home_team == "NewJersey": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "New Jersey Nets": 
                    mov_a_h = mov_ratings_for_year.at[team, 'MOV/A']
        elif home_team == "Seattle": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "Seattle SuperSonics": 
                    mov_a_h = mov_ratings_for_year.at[team, 'MOV/A']
        elif home_team == "NewOrleans": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "New Orleans Hornets": 
                    mov_a_h = mov_ratings_for_year.at[team, 'MOV/A']
        elif home_team == "Brooklyn": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "New Jersey Nets": 
                    mov_a_h = mov_ratings_for_year.at[team, 'MOV/A']
        elif home_team == "OklahomaCity": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "Seattle SuperSonics": 
                    mov_a_h = mov_ratings_for_year.at[team, 'MOV/A']
        spread_data.at[row, 'mov_a_h'] = mov_a_h
    if spread_data.at[row, 'mov_a_a'] == 0: 
        mov_ratings_for_year = movs[year-1]
        if away_team == "NewJersey": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "New Jersey Nets": 
                    mov_a_a = mov_ratings_for_year.at[team, 'MOV/A']
        elif away_team == "Seattle": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "Seattle SuperSonics": 
                    mov_a_a = mov_ratings_for_year.at[team, 'MOV/A']
        elif away_team == "NewOrleans": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "New Orleans Hornets": 
                    mov_a_a = mov_ratings_for_year.at[team, 'MOV/A']
        elif away_team == "Brooklyn": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "New Jersey Nets": 
                    mov_a_a = mov_ratings_for_year.at[team, 'MOV/A']
        elif away_team == "OklahomaCity": 
            for team in range(mov_ratings_for_year.shape[0]): 
                if mov_ratings_for_year.at[team, 'Team'] == "Seattle SuperSonics": 
                    mov_a_a = mov_ratings_for_year.at[team, 'MOV/A']
        spread_data.at[row, 'mov_a_a'] = mov_a_a

spread_data.to_excel("../historic_data/spread_data_large_fixed.xlsx")