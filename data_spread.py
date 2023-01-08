import pandas as pd
from bs4 import BeautifulSoup
import requests
import math

ROW_START = 150
ROW_PLAYOFFS = 0

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

# convert team name to the name used in the league stats sheet. note that it only returns the first word as this is the name used to parse the spreadsheet
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
    elif team == 'Washington': return 'Washington Wizards'
    elif team == 'Miami': return 'Miami Heat'
    elif team == 'NewYork': return 'New York Knicks'
    elif team == 'Indiana': return 'Indiana Pacers'
    elif team == 'Detroit': return 'Detroit Pistons'
    elif team == 'OklahomaCity' or team == 'Oklahoma City': return 'Oklahoma City Thunder'
    elif team == 'Sacramento': return 'Sacramento Kings'
    elif team == 'Minnesota': return 'Minnesota Timberwolves'
    elif team == 'Phoenix': return 'Phoenix Suns'
    elif team == 'SanAntonio' or team == 'San Antonio': return 'San Antonio Spurs'
    elif team == 'Memphis': return 'Memphis Grizzlies'
    elif team == 'Denver': return 'Denver Nuggets'
    elif team == 'Houston': return 'Houston Rockets'
    elif team == 'Utah': return 'Utah Jazz'
    elif team == 'NewOrleans' or team == 'New Orleans': return 'New Orleans Pelicans'
    elif team == 'GoldenState' or team == 'Golden State': return 'Golden State Warriors'
    elif team == 'LAClippers' or team == 'LA Clippers': return 'Los Angeles Clippers'
    elif team == 'Charlotte': 
        if year < 2015: return 'Charlotte Bobcats'
        else: return 'Charlotte Hornets'
    elif team == 'Dallas': return 'Dallas Mavericks'

def get_abbrv(team, year): 
    if team == 'LALakers' or team == 'LA Lakers': return 'LAL'
    elif team == 'Cleveland': return 'CLE'
    elif team == 'Boston': return 'BOS'
    elif team == 'Milwaukee': return 'MIL'
    elif team == 'Chicago': return 'CHI'
    elif team == 'Portland': return 'POR'
    elif team == 'Toronto': return 'TOR'
    elif team == 'Philadelphia': return 'PHI'
    elif team == 'Atlanta': return 'ATL'
    elif team == 'Orlando': return 'ORL'
    elif team == 'Brooklyn': return 'BRK'
    elif team == 'Washington': return 'WAS'
    elif team == 'Miami': return 'MIA'
    elif team == 'NewYork' or team == 'New York': return 'NYK'
    elif team == 'Indiana': return 'IND'
    elif team == 'Detroit': return 'DET'
    elif team == 'OklahomaCity' or team == 'Oklahoma City': return 'OKC'
    elif team == 'Sacramento': return 'SAC'
    elif team == 'Minnesota': return 'MIN'
    elif team == 'Phoenix': return 'PHO'
    elif team == 'SanAntonio' or team == 'San Antonio': return 'SAS'
    elif team == 'Memphis': return 'MEM'
    elif team == 'Denver': return 'DEN'
    elif team == 'Houston': return 'HOU'
    elif team == 'Utah': return 'UTA'
    elif team == 'NewOrleans' or team == 'New Orleans': return 'NOP'
    elif team == 'GoldenState' or team == 'Golden State': return 'GSW'
    elif team == 'LAClippers' or team == 'LA Clippers': return 'LAC'
    elif team == 'Charlotte': 
        if year < 2015: return 'CHA'
        else: return 'CHO'
    elif team == 'Dallas': return 'DAL'

def get_game_log(team, year): 
    team_str = get_abbrv(team, year)
    year_str = str(year)

    api_url = f"https://www.basketball-reference.com/teams/{team_str}/{year_str}/gamelog/?sr&amp;utm_source=direct&amp;utm_medium=Share&amp;utm_campaign=ShareTool#tgl_basic"
    response = requests.get(api_url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    leagueData = pd.read_html(str(table))[0]
    leagueData.columns = leagueData.columns.droplevel(level=0)

    ## ChatGPT code: filtering data set
    # Convert the 'G' column to a numeric type and store in a new column 'G_num'
    leagueData['G_num'] = pd.to_numeric(leagueData['G'], errors='coerce')

    # Filter the rows where 'G_num' is not null
    df = leagueData[leagueData['G_num'].notnull()]

    df = df.reset_index(drop=True)
    return df

def get_game_log_excel(team, year): 
    filepath = f'./gameLogs/{year}/{team}.xlsx'
    df = pd.read_excel(filepath)
    return df

def get_rsw_odds_excel(year): 
    filepath = f'./rswOdds/{year}.xlsx'
    df = pd.read_excel(filepath)
    return df

def get_ratings(year): 
    filepath = f'./ratings/{year}.xlsx'
    df = pd.read_excel(filepath)
    return df

pd.set_option('display.max_rows', None)
total_data = pd.DataFrame({'year': [], 'home_spread_hit': [], 'total': [], 'spread': [], 'home_team': [], 'away_team': [], 'pct_spreads_hit_h': [], 'pct_spreads_hit_a': [], 'ppg_h': [], 'ppg_a': [], 'pace_h': [], 'pace_a': [], 'ortg_h': [], 'ortg_a': [], 'drtg_h': [], 'drtg_a': [], 'drb_h': [], 'drb_a': [], 'threePAR_h': [], 'threePAR_a': [], 'ts_h': [], 'ts_a': [], 'ftr_h': [], 'ftr_a': [], 'd_tov_h': [], 'd_tov_a': [], 'o_tov_h': [], 'o_tov_a': [], 'ftperfga_h': [], 'ftperfga_a': [], 'points_over_average_ratio_h': [], 'points_over_average_ratio_a': [], 'hotness_ratio_h': [], 'hotness_ratio_a': [], 'std_dev_h': [], 'std_dev_a': [], 'win_pct_h': [], 'win_pct_a': [], 'rsw_h': [], 'rsw_a': [], 'ratings_2k_h': [], 'ratings_2k_a': []})

team_names = [ "Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]

team_name_mapping = {
    "LALakers": "LA Lakers",
    "GoldenState": "Golden State",
    "LAClippers": "LA Clippers", 
    "NewOrleans": "New Orleans", 
    "SanAntonio": "San Antonio", 
    "OklahomaCity": "Oklahoma City", 
    "NewYork": "New York"
}

# Initialize an empty dictionary to store the dataframes
game_logs = {}

# Iterate over the list of teams and the range of years
for team in team_names:
    for year in range(2014, 2024):
        # Use the get_game_log function to retrieve the dataframe for the current team and year
        df = get_game_log_excel(team, year)
        # Add the dataframe to the dictionary with the key (team, year)
        game_logs[(team, year)] = df
        print("Generated game log for " + team + " in " + str(year) + "...")

rsw_odds = {}
for year in range(2014, 2024): 
    df = get_rsw_odds_excel(year)
    rsw_odds[year] = df
    print("Generated pre-season odds for year " + str(year) + "...")

ratings = {}
for year in range(2014, 2024): 
    df = get_ratings(year)
    ratings[year] = df
    print("Generated ratings for year " + str(year) + "...")

for yearOffset in range(10):
    year = 2014+yearOffset

    # api_url = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_" + str(year-1) + ".html&div=div_advanced-team"
    # response = requests.get(api_url) 
    # soup = BeautifulSoup(response.content, 'html.parser')
    # table = soup.find('table')
    # leagueData = pd.read_html(str(table))[0]
    # leagueData = leagueData.drop(['Unnamed: 0_level_0'], axis=1)

    data = pd.read_excel('../NBA-Spreadsheets/' + str(year) + '/oddsStats.xlsx')
    new_data = pd.DataFrame({'year': [], 'home_spread_hit': [], 'total': [], 'spread': [], 'home_team': [], 'away_team': [], 'pct_spreads_hit_h': [], 'pct_spreads_hit_a': [], 'ppg_h': [], 'ppg_a': [], 'pace_h': [], 'pace_a': [], 'ortg_h': [], 'ortg_a': [], 'drtg_h': [], 'drtg_a': [], 'drb_h': [], 'drb_a': [], 'threePAR_h': [], 'threePAR_a': [], 'ts_h': [], 'ts_a': [], 'ftr_h': [], 'ftr_a': [], 'd_tov_h': [], 'd_tov_a': [], 'o_tov_h': [], 'o_tov_a': [], 'ftperfga_h': [], 'ftperfga_a': [], 'points_over_average_ratio_h': [], 'points_over_average_ratio_a': [], 'hotness_ratio_h': [], 'hotness_ratio_a': [], 'std_dev_h': [], 'std_dev_a': [], 'win_pct_h': [], 'win_pct_a': [], 'rsw_h': [], 'rsw_a': [], 'ratings_2k_h': [], 'ratings_2k_a': []})
    for row in range(data.shape[0]): 
        if row%2==1: 

            # phase 1 factors: basic numbers

            #home is negative
            team1 = data.at[row, 'Team']
            team2 = data.at[row-1, 'Team']
            # print('for: ' + team1 + ' vs ' + team2)
            if data.at[row, 'Close']!='pk' and data.at[row, 'Close']>=100: #this means away is favored, spread is +
                #is the total
                total = data.at[row, 'Close']
                if data.at[row-1, 'Close'] != 'pk' and data.at[row-1, 'Close'] != 'PK': 
                    spread = data.at[row-1, 'Close']
                else: 
                    spread = 0
            else: #home is favored, spread is -
                total = data.at[row-1, 'Close']
                if data.at[row, 'Close'] != 'pk' and data.at[row, 'Close'] != 'PK': 
                    spread = -(data.at[row, 'Close'])
                else: 
                    spread = 0
            final_spread = data.at[row-1, 'Final'] - data.at[row, 'Final']
            home_spread_hit = final_spread < spread
            push = final_spread == spread
            
            # phase 2 factors: advanced stats

            game_log_1 = game_logs[(team_name_mapping.get(team1, team1), year)]
            game_log_2 = game_logs[(team_name_mapping.get(team2, team2), year)]

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

            game_log_1 = game_logs[(team_name_mapping.get(team1, team1), year)]
            game_log_2 = game_logs[(team_name_mapping.get(team2, team2), year)]
            games_played_team_one = 0
            games_played_team_two = 0
            for row2 in range(row-1): 
                if data.at[row2, 'Team'] == team1: 
                    games_played_team_one += 1
                elif data.at[row2, 'Team'] == team2: 
                    games_played_team_two += 1
            if not (((games_played_team_one > 81 or games_played_team_two > 81)) or (year == 2020 and (games_played_team_one > 63 or games_played_team_two > 63)) or (year == 2021 and (games_played_team_one > 71 or games_played_team_two > 71))): 
                
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

                pace = (pace2 - pace1)
                ortg = (ortg2 - ortg1)
                drtg = (drtg2 - drtg1)
                drb = (drb2 - drb1)
                threePAR = (threePAR2 - threePAR1)
                ts = (ts2 - ts1)
                ftr = (ftr2 - ftr1)
                d_tov = (d_tov2 - d_tov1)
                o_tov = (o_tov2 - o_tov1)
                ftperfga = (ftperfga2 - ftperfga1)
                totalppg = (ppg2 - ppg1)

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
                points_over_average_ratio1 = 0
                points_over_average_ratio2 = 0
                if total_league_scoring > 0: 
                    league_scoring_average = total_league_scoring / games_played
                    points_over_average_ratio = totalppg / league_scoring_average
                    points_over_average_ratio1 = (ppg1/league_scoring_average)
                    points_over_average_ratio2 = (ppg2/league_scoring_average)
                    points_over_average_ratio = (ppg2/league_scoring_average) - (ppg1/league_scoring_average)

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
                hotness_ratio = (hotness_ratio2 - hotness_ratio1)

                #standard deviation of points
                std_dev1 = calc_std_dev(points1)
                std_dev2 = calc_std_dev(points2)
                std_dev = (std_dev2 - std_dev1)

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
                win_pct = (win_pct2 - win_pct1)

                #rsw
                preseason_odds = rsw_odds[year]
                rsw1 = 0
                rsw2 = 0
                for team in range(preseason_odds.shape[0]): 
                    if preseason_odds.at[team, 'Team'] == convert_team_name(team1, year): 
                        rsw1 = preseason_odds.at[team, 'W-L O/U']
                    elif preseason_odds.at[team, 'Team'] == convert_team_name(team2, year): 
                        rsw2 = preseason_odds.at[team, 'W-L O/U']
                rsw = (rsw2-rsw1)

                #2k ratings
                ratings_for_year = ratings[year]
                rating1 = 0
                rating2 = 0
                col_name = f"{str(year-1)}/{str(year)[2:4]}"
                team1name = convert_team_name(team1, year)
                team2name = convert_team_name(team2, year)
                if team1name == 'Charlotte Bobcats':
                    team1name = 'Charlotte Hornets'
                elif team2name == 'Charlotte Bobcats': 
                    team2name = 'Charlotte Hornets'
                for team in range(ratings_for_year.shape[0]): 
                    if ratings_for_year.at[team, 'Team'] == team1name: 
                        rating1 = ratings_for_year.at[team, col_name]
                    elif ratings_for_year.at[team, 'Team'] == team2name: 
                        rating2 = ratings_for_year.at[team, col_name]
                rating = (rating2 - rating1)

                # debugging
                outlier = (team1 == "Brooklyn" and team2 == "Oklahoma City" and year == 2016) or (team1 == "Toronto" and team2 == "LA Clippers" and year == 2016)

                #push
                if not push and not outlier: 
                    new_data.loc[len(new_data.index)] = [year, (1 if home_spread_hit else 0), total, spread, team1, team2, None, None, ppg1, ppg2, pace1, pace2, ortg1, ortg2, drtg1, drtg2, drb1, drb2, threePAR1, threePAR2, ts1, ts2, ftr1, ftr2, d_tov1, d_tov2, o_tov1, o_tov2, ftperfga1, ftperfga2, points_over_average_ratio1, points_over_average_ratio2, hotness_ratio1, hotness_ratio2, std_dev1, std_dev2, win_pct1, win_pct2, rsw1, rsw2, rating1, rating2]

                # print("Data for " + team1 + " vs " + team2 + " in " + str(year))
    print("gathering spread percentage data for year " + str(year))
    for row in range(new_data.shape[0]): 
        if row > ROW_START: 
            totalGames1 = 0
            spreadsCovered1 = 0
            totalGames2 = 0
            spreadsCovered2 = 0
            for row2 in range(row-1): 
                if (new_data.at[row2, 'home_team'] == new_data.at[row, 'home_team'] or new_data.at[row2, 'away_team'] == new_data.at[row, 'home_team']): 
                    totalGames1 += 1
                    spreadsCovered1 += new_data.at[row2, 'home_spread_hit']
            for row2 in range(row-1): 
                if (new_data.at[row2, 'home_team'] == new_data.at[row, 'away_team'] or new_data.at[row2, 'away_team'] == new_data.at[row, 'away_team']): 
                    totalGames2 += 1
                    spreadsCovered2 += new_data.at[row2, 'home_spread_hit']
            pct_spreads_covered1 = float(spreadsCovered1)/float(totalGames1)
            pct_spreads_covered2 = float(spreadsCovered2)/float(totalGames2)
            new_data.at[row, 'pct_spreads_hit_h'] = pct_spreads_covered1
            new_data.at[row, 'pct_spreads_hit_a'] = pct_spreads_covered2
    total_data = pd.concat([total_data, new_data.iloc[(ROW_START+1):]], ignore_index=True)
    
print(total_data)
total_data.to_excel("spread_data.xlsx")