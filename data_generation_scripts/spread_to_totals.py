## this script takes spread data and converts it to total data 

import pandas as pd
import math
import os
from injuryv2 import *

ROW_START = 125
CLOSE_GAME_THRESHOLD = 6

team_names = { 'pre2009': ["Atlanta", "Boston", "New Jersey", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Seattle", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'pre2013': ["Atlanta", "Boston", "New Jersey", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'post2013': ["Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]}

team_name_mapping = {
    "LALakers": "LA Lakers",
    "GoldenState": "Golden State",
    "LAClippers": "LA Clippers", 
    "NewOrleans": "New Orleans", 
    "SanAntonio": "San Antonio", 
    "OklahomaCity": "Oklahoma City", 
    "NewYork": "New York",
    "NewJersey": "New Jersey"
}

#chatGPT generated function
def calc_std_dev(numbers):
  # Return 0 if the input list is empty
  if not numbers:
    return 0

  # Calculate the mean of the numbers
  mean = sum(numbers) / len(numbers)

  # Calculate the variance of the numbers
  variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)

  # Calculate the standard deviation from the variance
  std_dev = math.sqrt(variance)

  return std_dev

def convert_date(date_string, season): 
    date_string = str(date_string)
    day = int(date_string[-2:])
    month = int(date_string[:-2])
    if month <= 9:
        year = season
    else: 
        year = season-1
    return datetime.date(year, month, day)

def convert_team_name_mov(team, year): 
    if team == 'LALakers' or team == 'LA Lakers': return 'Los Angeles Lakers'
    elif team == 'Cleveland': return 'Cleveland Cavaliers'
    elif team == 'Boston': return 'Boston Celtics'
    elif team == 'Milwaukee': return 'Milwaukee Bucks'
    elif team == 'Chicago': return 'Chicago Bulls'
    elif team == 'Portland': return 'Portland Trail Blazers'
    elif team == 'Toronto': return 'Toronto Raptors'
    elif team == 'Philadelphia': return 'Philadelphia 76ers'
    elif team == 'Atlanta': return 'Atlanta Hawks'
    elif team == 'Orlando': return 'Orlando Magic'
    elif team == 'Brooklyn': 
        if year == 2012: return 'New Jersey Nets'
        else: return 'Brooklyn Nets'
    elif team == 'New Jersey' or team == 'NewJersey': return 'New Jersey Nets'
    elif team == 'Washington': return 'Washington Wizards'
    elif team == 'Miami': return 'Miami Heat'
    elif team == 'NewYork': return 'New York Knicks'
    elif team == 'Indiana': return 'Indiana Pacers'
    elif team == 'Detroit': return 'Detroit Pistons'
    elif team == 'OklahomaCity' or team == 'Oklahoma City': 
        if year == 2008: return 'Seattle SuperSonics'
        else: return 'Oklahoma City Thunder'
    elif team == 'Seattle': return 'Seattle SuperSonics'
    elif team == 'Sacramento': return 'Sacramento Kings'
    elif team == 'Minnesota': return 'Minnesota Timberwolves'
    elif team == 'Phoenix': return 'Phoenix Suns'
    elif team == 'SanAntonio' or team == 'San Antonio': return 'San Antonio Spurs'
    elif team == 'Memphis': return 'Memphis Grizzlies'
    elif team == 'Denver': return 'Denver Nuggets'
    elif team == 'Houston': return 'Houston Rockets'
    elif team == 'Utah': return 'Utah Jazz'
    elif team == 'NewOrleans' or team == 'New Orleans': 
        if year < 2014: return 'New Orleans Hornets'
        else: return 'New Orleans Pelicans'
    elif team == 'GoldenState' or team == 'Golden State': return 'Golden State Warriors'
    elif team == 'LAClippers' or team == 'LA Clippers': return 'Los Angeles Clippers'
    elif team == 'Charlotte': 
        if year < 2015: return 'Charlotte Bobcats'
        else: return 'Charlotte Hornets'
    elif team == 'Dallas': return 'Dallas Mavericks'
    else: raise Exception

def convert_team_name(team, year): 
    if team == 'LALakers' or team == 'LA Lakers': return 'Los Angeles Lakers'
    elif team == 'Cleveland': return 'Cleveland Cavaliers'
    elif team == 'Boston': return 'Boston Celtics'
    elif team == 'Milwaukee': return 'Milwaukee Bucks'
    elif team == 'Chicago': return 'Chicago Bulls'
    elif team == 'Portland': return 'Portland Trail Blazers'
    elif team == 'Toronto': return 'Toronto Raptors'
    elif team == 'Philadelphia': return 'Philadelphia 76ers'
    elif team == 'Atlanta': return 'Atlanta Hawks'
    elif team == 'Orlando': return 'Orlando Magic'
    elif team == 'Brooklyn': return 'Brooklyn Nets'
    elif team == 'New Jersey' or team == 'NewJersey': return 'New Jersey Nets'
    elif team == 'Washington': return 'Washington Wizards'
    elif team == 'Miami': return 'Miami Heat'
    elif team == 'NewYork': return 'New York Knicks'
    elif team == 'Indiana': return 'Indiana Pacers'
    elif team == 'Detroit': return 'Detroit Pistons'
    elif team == 'OklahomaCity' or team == 'Oklahoma City': return 'Oklahoma City Thunder'
    elif team == 'Seattle': return 'Seattle SuperSonics'
    elif team == 'Sacramento': return 'Sacramento Kings'
    elif team == 'Minnesota': return 'Minnesota Timberwolves'
    elif team == 'Phoenix': return 'Phoenix Suns'
    elif team == 'SanAntonio' or team == 'San Antonio': return 'San Antonio Spurs'
    elif team == 'Memphis': return 'Memphis Grizzlies'
    elif team == 'Denver': return 'Denver Nuggets'
    elif team == 'Houston': return 'Houston Rockets'
    elif team == 'Utah': return 'Utah Jazz'
    elif team == 'NewOrleans' or team == 'New Orleans': 
        if year < 2014: return 'New Orleans Hornets'
        else: return 'New Orleans Pelicans'
    elif team == 'GoldenState' or team == 'Golden State': return 'Golden State Warriors'
    elif team == 'LAClippers' or team == 'LA Clippers': return 'Los Angeles Clippers'
    elif team == 'Charlotte': 
        if year < 2015: return 'Charlotte Bobcats'
        else: return 'Charlotte Hornets'
    elif team == 'Dallas': return 'Dallas Mavericks'
    else: 
        raise Exception

# Initialize an empty dictionary to store the dataframes
game_logs = {}

def get_rsw_odds_excel(year): 
    filepath = f'../rsw_odds/{year}.xlsx'
    df = pd.read_excel(filepath)
    return df

def get_game_log_excel(team, year): 
    filepath = f'../game_logs/{year}/{team}.xlsx'
    df = pd.read_excel(filepath)
    return df

def get_mov_excel(year): 
    filepath = f'../mov_ratings/{year}.xlsx'
    df = pd.read_excel(filepath)
    return df

# Iterate over the list of teams and the range of years
for year in range(2008, 2024):
    if year < 2009: 
        for team in team_names['pre2009']: 
            # Use the get_game_log function to retrieve the dataframe for the current team and year
            df = get_game_log_excel(team, year)
            # Add the dataframe to the dictionary with the key (team, year)
            game_logs[(team, year)] = df
            print("Generated game log for " + team + " in " + str(year) + "...")
    elif year < 2013: 
        for team in team_names['pre2013']: 
            # Use the get_game_log function to retrieve the dataframe for the current team and year
            df = get_game_log_excel(team, year)
            # Add the dataframe to the dictionary with the key (team, year)
            game_logs[(team, year)] = df
            print("Generated game log for " + team + " in " + str(year) + "...")
    else: 
        for team in team_names['post2013']:
            # Use the get_game_log function to retrieve the dataframe for the current team and year
            df = get_game_log_excel(team, year)
            # Add the dataframe to the dictionary with the key (team, year)
            game_logs[(team, year)] = df
            print("Generated game log for " + team + " in " + str(year) + "...")

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

spread_data = pd.read_excel('../historic_data/spread_data_large_fixed.xlsx')
total_data = pd.DataFrame({'year': [], 'hitOver': [], 'total': [], 'totalppg': [], 'size_of_spread': [], 'home_team': [], 'away_team': [], 'pct_overs_hit': [], 'pace': [], 'ortg': [], 'drtg': [], 'drb': [], 'threePAR': [], 'ts': [], 'ftr': [], 'd_tov': [], 'o_tov': [], 'ftperfga': [], 'points_over_average_ratio': [], 'hotness_ratio': [], 'std_dev': [], 'win_pct': [], 'rsw': [], 'win_pct_close': [], 'mov_a': [], 'injury_gmsc': [], 'injury_mins': []})
for year in range(2008, 2024): 
    if os.path.exists(f'../historic_data/{year}_total_data.xlsx'): 
        print("Found existing data for year " + str(year) + ", loading data now...")
        new_data = pd.read_excel(f'../historic_data/{year}_total_data.xlsx')
    else:  
        data = pd.read_excel('../../NBA-Spreadsheets/' + str(year) + '/oddsStats.xlsx')
        new_data = pd.DataFrame({'year': [], 'hitOver': [], 'total': [], 'totalppg': [], 'size_of_spread': [], 'home_team': [], 'away_team': [], 'pct_overs_hit': [], 'pace': [], 'ortg': [], 'drtg': [], 'drb': [], 'threePAR': [], 'ts': [], 'ftr': [], 'd_tov': [], 'o_tov': [], 'ftperfga': [], 'points_over_average_ratio': [], 'hotness_ratio': [], 'std_dev': [], 'win_pct': [], 'rsw': [], 'win_pct_close': [], 'mov_a': [], 'injury_gmsc': [], 'injury_mins': []})
        for row in range(data.shape[0]): 
            if row%2==1: 
                team1 = data.at[row, 'Team']
                team2 = data.at[row-1, 'Team']

                print(f"{str(100*float(row/data.shape[0]))}% through the {str(year)} season...")
                
                # phase 2 factors: advanced stats

                game_log_1 = game_logs[(team_name_mapping.get(team1, team1), year)]
                game_log_2 = game_logs[(team_name_mapping.get(team2, team2), year)]

                ppg1 = 0
                ppg2 = 0

                game_log_1 = game_logs[(team_name_mapping.get(team1, team1), year)]
                game_log_2 = game_logs[(team_name_mapping.get(team2, team2), year)]
                games_played_team_one = 0
                games_played_team_two = 0
                for row2 in range(row-1): 
                    if data.at[row2, 'Team'] == team1: 
                        games_played_team_one += 1
                    elif data.at[row2, 'Team'] == team2: 
                        games_played_team_two += 1
                if not (((games_played_team_one > 81 or games_played_team_two > 81)) or (year == 2020 and (games_played_team_one > 63 or games_played_team_two > 63)) or (year == 2021 and (games_played_team_one > 71 or games_played_team_two > 71)) or (year == 2012 and (games_played_team_one > 65 or games_played_team_two > 65))): 
                    
                    points1 = []
                    for game_number in range(games_played_team_one): 
                        points1.append(game_log_1.at[game_number, 'Tm'])
                    for game in points1: 
                        ppg1 += game

                    if games_played_team_one > 0: 
                        ppg1 /= games_played_team_one

                    points2 = []
                    for game_number in range(games_played_team_two): 
                        points2.append(game_log_2.at[game_number, 'Tm'])
                    for game in points2: 
                        ppg2 += game
                    
                    if games_played_team_two > 0: 
                        ppg2 /= games_played_team_two

                    for x in range(spread_data.shape[0]): 
                        if team1 == spread_data.at[x, 'home_team'] and team2 == spread_data.at[x, 'away_team'] and year == spread_data.at[x, 'year'] and abs(ppg1-spread_data.at[x, 'ppg_h'])<=0.01 and abs(ppg2-spread_data.at[x, 'ppg_a'])<=0.01:
                            spread_row = x
                            break
                        else: spread_row = -1
                    
                    if spread_row != -1:
                        # phase 1 factors: basic numbers
                        total = spread_data.at[spread_row, 'total']
                        size_of_spread = abs(spread_data.at[spread_row, 'spread'])
                        final_score = data.at[row, 'Final'] + data.at[row-1, 'Final']
                        hitOver = final_score > total
                        push = final_score == total

                        pace1 = spread_data.at[spread_row, 'pace_h']
                        pace2 = spread_data.at[spread_row, 'pace_a']
                        ortg1 = spread_data.at[spread_row, 'ortg_h']
                        ortg2 = spread_data.at[spread_row, 'ortg_a']
                        drtg1 = spread_data.at[spread_row, 'drtg_h']
                        drtg2 = spread_data.at[spread_row, 'drtg_a']
                        drb1 = spread_data.at[spread_row, 'drb_h']
                        drb2 = spread_data.at[spread_row, 'drb_a']
                        threePAR1 = spread_data.at[spread_row, 'threePAR_h']
                        threePAR2 = spread_data.at[spread_row, 'threePAR_a']
                        ts1 = spread_data.at[spread_row, 'ts_h']
                        ts2 = spread_data.at[spread_row, 'ts_a']
                        ftr1 = spread_data.at[spread_row, 'ftr_h']
                        ftr2 = spread_data.at[spread_row, 'ftr_a']
                        d_tov1 = spread_data.at[spread_row, 'd_tov_h']
                        d_tov2 = spread_data.at[spread_row, 'd_tov_a']
                        o_tov1 = spread_data.at[spread_row, 'o_tov_h']
                        o_tov2 = spread_data.at[spread_row, 'o_tov_a']
                        ftperfga1 = spread_data.at[spread_row, 'ftperfga_h']
                        ftperfga2 = spread_data.at[spread_row, 'ftperfga_a']

                        hotness_ratio1 = spread_data.at[spread_row, 'hotness_ratio_h']
                        hotness_ratio2 = spread_data.at[spread_row, 'hotness_ratio_a']
                        std_dev1 = spread_data.at[spread_row, 'std_dev_h']
                        std_dev2 = spread_data.at[spread_row, 'std_dev_a']
                        win_pct1 = spread_data.at[spread_row, 'win_pct_h']
                        win_pct2 = spread_data.at[spread_row, 'win_pct_a']
                        rsw1 = spread_data.at[spread_row, 'rsw_h']
                        rsw2 = spread_data.at[spread_row, 'rsw_a']
                        injury_gmsc1 = spread_data.at[spread_row, 'injury_gmsc_h']
                        injury_gmsc2 = spread_data.at[spread_row, 'injury_gmsc_a']
                        injury_mins1 = spread_data.at[spread_row, 'injury_mins_h']
                        injury_mins2 = spread_data.at[spread_row, 'injury_mins_a']
                        win_pct_close1 = spread_data.at[spread_row, 'win_pct_close_h']
                        win_pct_close2 = spread_data.at[spread_row, 'win_pct_close_a']
                        mov_a1 = spread_data.at[spread_row, 'mov_a_h']
                        mov_a2 = spread_data.at[spread_row, 'mov_a_a']

                        pace = (pace1 + pace2)/2
                        ortg = (ortg1 + ortg2)/2
                        drtg = (drtg1 + drtg2)/2
                        drb = (drb1 + drb2)/2
                        threePAR = (threePAR1 + threePAR2)/2
                        ts = (ts1 + ts2)/2
                        ftr = (ftr1 + ftr2)/2
                        d_tov = (d_tov1 + d_tov2)/2
                        o_tov = (o_tov1 + o_tov2)/2
                        ftperfga = (ftperfga1 + ftperfga2)/2
                        totalppg = (ppg1 + ppg2)/2
                        hotness_ratio = (hotness_ratio1 + hotness_ratio2)/2
                        std_dev = (std_dev1 + std_dev2)/2
                        win_pct = (win_pct1 + win_pct2)/2
                        rsw = (rsw1+rsw2)/2
                        injury_gmsc = (injury_gmsc1 + injury_gmsc2)/2
                        injury_mins = (injury_mins1 + injury_mins2)/2
                        win_pct_close = (win_pct_close1 + win_pct_close2)/2
                        mov_a = (mov_a1 + mov_a2)/2

                        ##phase 3 factors

                        #points over average
                        total_league_scoring = 0
                        games_played = 0
                        for row2 in range(row-1): 
                            if data.at[row2, 'Date'] != data.at[row, 'Date']: 
                                games_played += 1
                                total_league_scoring += data.at[row2, 'Final']
                        league_scoring_average = 0
                        points_over_average_ratio = 0
                        if total_league_scoring > 0: 
                            league_scoring_average = total_league_scoring / games_played
                            points_over_average_ratio = totalppg / league_scoring_average

                        new_data.loc[len(new_data.index)] = [year, (1 if hitOver else 0), total, totalppg, size_of_spread, team1, team2, None, pace, ortg, drtg, drb, threePAR, ts, ftr, d_tov, o_tov, ftperfga, points_over_average_ratio, hotness_ratio, std_dev, win_pct, rsw, win_pct_close, mov_a, injury_gmsc, injury_mins]
                    else: 
                        print("Data not found in spread table!")
                        if data.at[row, 'Close']!='pk' and data.at[row, 'Close']>=100:
                            #is the total
                            total = data.at[row, 'Close']
                            if data.at[row-1, 'Close'] != 'pk' and data.at[row-1, 'Close'] != 'PK': 
                                size_of_spread = data.at[row-1, 'Close']
                            else: 
                                size_of_spread = 0
                        else: 
                            total = data.at[row-1, 'Close']
                            if data.at[row, 'Close'] != 'pk' and data.at[row, 'Close'] != 'PK': 
                                size_of_spread = data.at[row, 'Close']
                            else: 
                                size_of_spread = 0
                        final_score = data.at[row, 'Final'] + data.at[row-1, 'Final']
                        hitOver = final_score > total
                        push = final_score == total
                        o_tov1 = 0
                        o_tov2 = 0
                        d_tov1 = 0
                        d_tov2 = 0
                        ftr1 = 0
                        ftr2 = 0
                        ts1 = 0
                        ts2 = 0
                        threePAR1 = 0
                        threePAR2 = 0
                        drb1 = 0
                        drb2 = 0
                        ortg1 = 0
                        ortg2 = 0
                        drtg1 = 0
                        drtg2 = 0
                        pace1 = 0
                        pace2 = 0
                        ftperfga1 = 0
                        ftperfga2 = 0
                        ppg1 = 0
                        ppg2 = 0
                        points1 = []
                        for game_number in range(games_played_team_one): 
                            pace1 += game_log_1.at[game_number, 'Pace']
                            ortg1 += game_log_1.at[game_number, 'ORtg']
                            drtg1 += game_log_1.at[game_number, 'DRtg']
                            drb1 += game_log_1.at[game_number, 'DRB%']
                            threePAR1 += game_log_1.at[game_number, '3PAr']
                            ts1 += game_log_1.at[game_number, 'TS%']
                            ftr1 += game_log_1.at[game_number, 'FTr']
                            d_tov1 += game_log_1.at[game_number, 'TOV%_1']
                            o_tov1 += game_log_1.at[game_number, 'TOV%_2']
                            ftperfga1 += (game_log_1.at[game_number, 'FT/FGA_1'] + game_log_1.at[game_number, 'FT/FGA_2'])/2
                            points1.append(game_log_1.at[game_number, 'Tm'])
                        for game in points1: 
                            ppg1 += game

                        if games_played_team_one > 0: 
                            pace1 /= games_played_team_one
                            ortg1 /= games_played_team_one
                            drtg1 /= games_played_team_one
                            drb1 /= games_played_team_one
                            threePAR1 /= games_played_team_one
                            ts1 /= games_played_team_one
                            ftr1 /= games_played_team_one
                            d_tov1 /= games_played_team_one
                            o_tov1 /= games_played_team_one
                            ftperfga1 /= games_played_team_one
                            ppg1 /= games_played_team_one

                        points2 = []
                        for game_number in range(games_played_team_two): 
                            pace2 += game_log_2.at[game_number, 'Pace']
                            ortg2 += game_log_2.at[game_number, 'ORtg']
                            drtg2 += game_log_2.at[game_number, 'DRtg']
                            drb2 += game_log_2.at[game_number, 'DRB%']
                            threePAR2 += game_log_2.at[game_number, '3PAr']
                            ts2 += game_log_2.at[game_number, 'TS%']
                            ftr2 += game_log_2.at[game_number, 'FTr']
                            d_tov2 += game_log_2.at[game_number, 'TOV%_1']
                            o_tov2 += game_log_2.at[game_number, 'TOV%_2']
                            ftperfga2 += (game_log_2.at[game_number, 'FT/FGA_1'] + game_log_2.at[game_number, 'FT/FGA_2'])/2
                            points2.append(game_log_2.at[game_number, 'Tm'])
                        for game in points2: 
                            ppg2 += game
                        
                        if games_played_team_two > 0: 
                            ftperfga2 /= games_played_team_two
                            o_tov2 /= games_played_team_two
                            d_tov2 /= games_played_team_two
                            ftr2 /= games_played_team_two
                            ts2 /= games_played_team_two
                            threePAR2 /= games_played_team_two
                            drb2 /= games_played_team_two
                            drtg2 /= games_played_team_two
                            ortg2 /= games_played_team_two
                            pace2 /= games_played_team_two
                            ppg2 /= games_played_team_two

                        pace = (pace1 + pace2)/2
                        ortg = (ortg1 + ortg2)/2
                        drtg = (drtg1 + drtg2)/2
                        drb = (drb1 + drb2)/2
                        threePAR = (threePAR1 + threePAR2)/2
                        ts = (ts1 + ts2)/2
                        ftr = (ftr1 + ftr2)/2
                        d_tov = (d_tov1 + d_tov2)/2
                        o_tov = (o_tov1 + o_tov2)/2
                        ftperfga = (ftperfga1 + ftperfga2)/2
                        totalppg = (ppg1 + ppg2)/2

                        ##phase 3 factors

                        #points over average
                        total_league_scoring = 0
                        games_played = 0
                        for row2 in range(row-1): 
                            if data.at[row2, 'Date'] != data.at[row, 'Date']: 
                                games_played += 1
                                total_league_scoring += data.at[row2, 'Final']
                        league_scoring_average = 0
                        points_over_average_ratio = 0
                        if total_league_scoring > 0: 
                            league_scoring_average = total_league_scoring / games_played
                            points_over_average_ratio = totalppg / league_scoring_average

                        #hotness factor
                        recent_ppg1 = 0
                        for game in range(len(points1)-3, len(points1)): #team 1
                            if game < 0: 
                                game = 0
                            if game < len(points1): 
                                recent_ppg1 += points1[game]
                        recent_ppg1 /= 3
                        recent_ppg2 = 0
                        for game in range(len(points2)-3, len(points2)): #team 2
                            if game < 0: 
                                game = 0
                            if game < len(points2): 
                                recent_ppg2 += points2[game]
                        recent_ppg2 /= 3
                        hotness_ratio1 = 1
                        if ppg1 > 0: 
                            hotness_ratio1 = recent_ppg1/ppg1
                        hotness_ratio2 = 1
                        if ppg2 > 0: 
                            hotness_ratio2 = recent_ppg2/ppg2
                        hotness_ratio = (hotness_ratio1 + hotness_ratio2)/2

                        #standard deviation of points
                        std_dev1 = calc_std_dev(points1)
                        std_dev2 = calc_std_dev(points2)
                        std_dev = (std_dev1 + std_dev2)/2

                        #phase 4 factors
                        
                        #winning percentage
                        wins1 = 0
                        wins2 = 0
                        games1 = 0
                        games2 = 0
                        for row2 in range(row-1): 
                            if data.at[row2, 'Team'] == team1: 
                                games1 += 1
                                if row2%2 == 1: #row-1 is the other team
                                    if data.at[row2, 'Final'] > data.at[row2-1, 'Final']: 
                                        wins1 += 1
                                else: #row+1 is the other team
                                    if data.at[row2, 'Final'] > data.at[row2+1, 'Final']: 
                                        wins1 += 1
                            elif data.at[row2, 'Team'] == team2: 
                                games2 += 1
                                if row2%2 == 1: #row-1 is the other team
                                    if data.at[row2, 'Final'] > data.at[row2-1, 'Final']: 
                                        wins2 += 1
                                else: #row+1 is the other team
                                    if data.at[row2, 'Final'] > data.at[row2+1, 'Final']: 
                                        wins2 += 1
                        if games1 == 0: 
                            win_pct1 = 0
                        else: 
                            win_pct1 = wins1/games1
                        if games2 == 0: 
                            win_pct2 = 0
                        else: 
                            win_pct2 = wins2/games2
                        win_pct = (win_pct1 + win_pct2)/2

                        #rsw
                        preseason_odds = rsw_odds[year]
                        rsw1 = 0
                        rsw2 = 0
                        for team in range(preseason_odds.shape[0]): 
                            if preseason_odds.at[team, 'Team'] == convert_team_name(team1, year): 
                                rsw1 = preseason_odds.at[team, 'W-L O/U']
                            elif preseason_odds.at[team, 'Team'] == convert_team_name(team2, year): 
                                rsw2 = preseason_odds.at[team, 'W-L O/U']
                        rsw = (rsw2+rsw1)/2

                        #mov/A
                        mov_ratings_for_year = movs[year-1]
                        mov_a_h = 0
                        mov_a_a = 0
                        for team in range(mov_ratings_for_year.shape[0]): 
                            if mov_ratings_for_year.at[team, 'Team'] == convert_team_name_mov(team1, year-1): 
                                mov_a_h = mov_ratings_for_year.at[team, 'MOV/A']
                            elif mov_ratings_for_year.at[team, 'Team'] == convert_team_name_mov(team2, year-1): 
                                mov_a_a = mov_ratings_for_year.at[team, 'MOV/A']
                        mov_a = (mov_a_h + mov_a_a)/2

                        # injuries (gmsc)
                        if row > 250: 
                            date_of_game = convert_date(data.at[row, 'Date'], year)
                            injury_gmsc1 = get_gmsc_injured(team_name_mapping.get(team1, team1), date_of_game)
                            injury_gmsc2 = get_gmsc_injured(team_name_mapping.get(team2, team2), date_of_game)
                            injury_gmsc = (injury_gmsc1 + injury_gmsc2)/2

                            # injuries (mins)
                            injury_mins1 = get_mins_injured(team_name_mapping.get(team1, team1), date_of_game)
                            injury_mins2 = get_mins_injured(team_name_mapping.get(team2, team2), date_of_game)
                            injury_mins = (injury_mins1 + injury_mins2)/2
                        else: 
                            injury_gmsc = 0
                            injury_mins = 0
                        
                        #win_pct_close
                        wins1_close = 0
                        wins2_close = 0
                        games1_close = 0
                        games2_close = 0
                        for row2 in range(row-1): 
                            if data.at[row2, 'Team'] == team1 and abs(data.at[row2, 'Final']-data.at[row2+1, 'Final'] < CLOSE_GAME_THRESHOLD): 
                                games1_close += 1
                                if row2%2 == 1: #row-1 is the other team
                                    if data.at[row2, 'Final'] > data.at[row2-1, 'Final']: 
                                        wins1_close += 1
                                else: #row+1 is the other team
                                    if data.at[row2, 'Final'] > data.at[row2+1, 'Final']: 
                                        wins1_close += 1
                            elif data.at[row2, 'Team'] == team2 and abs(data.at[row2, 'Final']-data.at[row2+1, 'Final'] < CLOSE_GAME_THRESHOLD): 
                                games2_close += 1
                                if row2%2 == 1: #row-1 is the other team
                                    if data.at[row2, 'Final'] > data.at[row2-1, 'Final']: 
                                        wins2_close += 1
                                else: #row+1 is the other team
                                    if data.at[row2, 'Final'] > data.at[row2+1, 'Final']: 
                                        wins2_close += 1
                        if games1_close == 0: 
                            win_pct_close1 = 0
                        else: 
                            win_pct_close1 = wins1_close/games1_close
                        if games2_close == 0: 
                            win_pct_close2 = 0
                        else: 
                            win_pct_close2 = wins2_close/games2_close
                        win_pct_close = (win_pct_close1 + win_pct_close2)/2

                        #FIND A WAY TO INCLUDE SOS

                        # debugging
                        outlier = (team1 == "Brooklyn" and team2 == "Oklahoma City" and year == 2016) or (team1 == "Toronto" and team2 == "LA Clippers" and year == 2016)

                        #push
                        if not push and not outlier: 
                            new_data.loc[len(new_data.index)] = [year, (1 if hitOver else 0), total, totalppg, size_of_spread, team1, team2, None, pace, ortg, drtg, drb, threePAR, ts, ftr, d_tov, o_tov, ftperfga, points_over_average_ratio, hotness_ratio, std_dev, win_pct, rsw, win_pct_close, mov_a, injury_gmsc, injury_mins]
        print("gathering over percentage data for year " + str(year))
        for row in range(new_data.shape[0]): 
            if row > ROW_START: 
                totalGames = 0
                oversHit = 0
                for row2 in range(row-1): 
                    if (new_data.at[row2, 'home_team'] == new_data.at[row, 'home_team'] or new_data.at[row2, 'away_team'] == new_data.at[row, 'home_team']): 
                        totalGames += 1
                        oversHit += new_data.at[row2, 'hitOver']
                for row2 in range(row-1): 
                    if (new_data.at[row2, 'home_team'] == new_data.at[row, 'away_team'] or new_data.at[row2, 'away_team'] == new_data.at[row, 'away_team']): 
                        totalGames += 1
                        oversHit += new_data.at[row2, 'hitOver']
                pct_overs_hit = float(oversHit)/float(totalGames)
                new_data.at[row, 'pct_overs_hit'] = pct_overs_hit
        new_data.to_excel(f"../historic_data/{year}_total_data.xlsx")
    total_data = pd.concat([total_data, new_data.iloc[(ROW_START+1):]], ignore_index=True)

print(total_data)
total_data.to_excel("../historic_data/total_data.xlsx")