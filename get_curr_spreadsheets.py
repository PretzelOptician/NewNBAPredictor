import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import math
import numpy as np
from datetime import datetime
import datetime as dt
from tweet_generator import *
from injuryv2 import *
from unidecode import unidecode

CURR_YEAR = 2023
CLOSE_GAME_THRESHOLD = 6

pd.set_option('display.max_rows', None)

def get_city(team): 
    if team == 'Golden State Warriors' or team == 'GoldenState' or team == 'Golden State': return 'GoldenState'
    elif team == 'Los Angeles Clippers' or team == 'LAClippers' or team == 'LA Clippers': return 'LAClippers'
    elif team == 'Los Angeles Lakers' or team == 'LALakers' or team == 'LA Lakers': return 'LALakers'
    elif team == 'New Orleans Pelicans' or team == 'NewOrleans' or team == 'New Orleans': return 'NewOrleans'
    elif team == 'New York Knicks' or team == 'NewYork' or team == 'New York': return 'NewYork'
    elif team == 'Oklahoma City Thunder' or team == 'OklahomaCity' or team == 'OklaCity' or team == 'Oklahoma City': return 'OklahomaCity'
    elif team == 'San Antonio Spurs' or team == 'SanAntonio' or team == 'San Antonio': return 'SanAntonio'
    else: return team.split(' ')[0]

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

def get_ratings(year, team): 
    filepath = f'./ratings/{year}.xlsx'
    df = pd.read_excel(filepath)
    col_name = f"{str(year-1)}/{str(year)[2:4]}"
    for row in range(df.shape[0]): 
        if df.at[row, 'Team'] == team: 
            rating1 = df.at[row, col_name]
    return rating1

def convert_team_name(team): 
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
    elif team == 'Charlotte': return 'Charlotte Hornets'
    elif team == 'Dallas': return 'Dallas Mavericks'

def get_abbrv(team, year): 
    if team == 'LALakers' or team == 'Los Angeles Lakers' or team == 'LA Lakers': return 'LAL'
    elif team == 'Cleveland' or team == 'Cleveland Cavaliers': return 'CLE'
    elif team == 'Boston' or team == 'Boston Celtics': return 'BOS'
    elif team == 'Milwaukee' or team == 'Milwaukee Bucks': return 'MIL'
    elif team == 'Chicago' or team == 'Chicago Bulls': return 'CHI'
    elif team == 'Portland' or team == 'Portland Trail Blazers': return 'POR'
    elif team == 'Toronto' or team == 'Toronto Raptors': return 'TOR'
    elif team == 'Philadelphia' or team == 'Philadelphia 76ers': return 'PHI'
    elif team == 'Atlanta' or team == 'Atlanta Hawks': return 'ATL'
    elif team == 'Orlando' or team == 'Orlando Magic': return 'ORL'
    elif team == 'Brooklyn' or team == 'Brooklyn Nets': return 'BRK'
    elif team == 'Washington' or team == 'Washington Wizards': return 'WAS'
    elif team == 'Miami' or team == 'Miami Heat': return 'MIA'
    elif team == 'NewYork' or team == 'New York' or team == 'New York Knicks': return 'NYK'
    elif team == 'Indiana' or team == 'Indiana Pacers': return 'IND'
    elif team == 'Detroit' or team == 'Detroit Pistons': return 'DET'
    elif team == 'OklahomaCity' or team == 'Oklahoma City' or team == 'Oklahoma City Thunder': return 'OKC'
    elif team == 'Sacramento' or team == 'Sacramento Kings': return 'SAC'
    elif team == 'Minnesota' or team == 'Minnesota Timberwolves': return 'MIN'
    elif team == 'Phoenix' or team == 'Phoenix Suns': return 'PHO'
    elif team == 'SanAntonio' or team == 'San Antonio' or team == 'San Antonio Spurs': return 'SAS'
    elif team == 'Memphis' or team == 'Memphis Grizzlies': return 'MEM'
    elif team == 'Denver' or team == 'Denver Nuggets': return 'DEN'
    elif team == 'Houston' or team == 'Houston Rockets': return 'HOU'
    elif team == 'Utah' or team == 'Utah Jazz': return 'UTA'
    elif team == 'NewOrleans' or team == 'New Orleans' or team == 'New Orleans Pelicans': return 'NOP'
    elif team == 'GoldenState' or team == 'Golden State' or team == 'Golden State Warriors': return 'GSW'
    elif team == 'LAClippers' or team == 'LA Clippers' or team == 'Los Angeles Clippers': return 'LAC'
    elif team == 'Charlotte' or team == 'Charlotte Hornets': 
        if year < 2015: return 'CHA'
        else: return 'CHO'
    elif team == 'Dallas' or team == 'Dallas Mavericks': return 'DAL'

def get_mov_excel(year): 
    filepath = f'./movRatings/{year}.xlsx'
    df = pd.read_excel(filepath)
    return df

def get_game_log(team, year): 
    print("Getting game log for " + team + " in year " + str(year))
    team_str = get_abbrv(team, year)
    year_str = str(year)

    api_url = f"https://www.basketball-reference.com/teams/{team_str}/{year_str}/gamelog-advanced/?sr&utm_source=direct&utm_medium=Share&utm_campaign=ShareTool#tgl_advanced"
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
    
    cols = ['Rk', 'G', 'Date', 'H/A', 'Opp_team', 'W/L', 'Tm', 'Opp', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'TS%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'Ofr', 'eFG%_1', 'TOV%_1', 'ORB%', 'FT/FGA_1', 'Dfr', 'eFG%_2', 'TOV%_2', 'DRB%', 'FT/FGA_2', 'G_num']
    df.columns = cols

    return df

def get_2k_ratings(year): 
    api_url = f"https://hoopshype.com/nba2k/teams/{str(year-1)}-{str(year)}/"
    response = requests.get(api_url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]

    df = df.reset_index(drop=True)

    return df

def get_odds(): 
    url = "https://odds.p.rapidapi.com/v4/sports/basketball_nba/odds"
    querystring = {"regions":"us","oddsFormat":"decimal","markets":"spreads,totals","dateFormat":"iso"}
    headers = {
        "X-RapidAPI-Key": "12777cbd21mshe5e3f8c4932bb27p163af3jsndff8ebab5ee4",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response

def get_rsw_odds_excel(year): 
    filepath = f'./rswOdds/{year}.xlsx'
    df = pd.read_excel(filepath)
    return df

def get_pct_overs_hit(team1, team2): 
    if team1 == 'Golden State Warriors': team1 = 'Golden State'
    elif team1 == 'Los Angeles Clippers': team1 = 'LA Clippers'
    elif team1 == 'Los Angeles Lakers': team1 = 'LA Lakers'
    elif team1 == 'New Orleans Pelicans': team1 = 'New Orleans'
    elif team1 == 'New York Knicks': team1 = 'New York'
    elif team1 == 'Oklahoma City Thunder': team1 = 'Okla City'
    elif team1 == 'San Antonio Spurs': team1 = 'San Antonio'
    else: team1 = team1.split(' ')[0]

    if team2 == 'Golden State Warriors': team2 = 'Golden State'
    elif team2 == 'Los Angeles Clippers': team2 = 'LA Clippers'
    elif team2 == 'Los Angeles Lakers': team2 = 'LA Lakers'
    elif team2 == 'New Orleans Pelicans': team2 = 'New Orleans'
    elif team2 == 'New York Knicks': team2 = 'New York'
    elif team2 == 'Oklahoma City Thunder': team2 = 'Okla City'
    elif team2 == 'San Antonio Spurs': team2 = 'San Antonio'
    else: team2 = team2.split(' ')[0]

    url = "https://www.teamrankings.com/nba/trends/ou_trends/"
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]

    df = df.reset_index(drop=True)
    for x in range(df.shape[0]): 
        if df.at[x, 'Team'] == team1: 
            home_over = float((df.at[x, 'Over Record']).split("-")[0])
            home_under = float((df.at[x, 'Over Record']).split("-")[1])
        elif df.at[x, 'Team'] == team2: 
            away_over = float((df.at[x, 'Over Record']).split("-")[0])
            away_under = float((df.at[x, 'Over Record']).split("-")[1])
    home_pct = home_over/(home_over+home_under)
    away_pct = away_over/(away_over+away_under)
    pct = (home_pct + away_pct)/2
    return pct

def get_pct_spreads_hit(team): 
    if team == 'Golden State Warriors': team = 'Golden State'
    elif team == 'Los Angeles Clippers': team = 'LA Clippers'
    elif team == 'Los Angeles Lakers': team = 'LA Lakers'
    elif team == 'New Orleans Pelicans': team = 'New Orleans'
    elif team == 'New York Knicks': team = 'New York'
    elif team == 'Oklahoma City Thunder': team = 'Okla City'
    elif team == 'San Antonio Spurs': team = 'San Antonio'
    else: team = team.split(' ')[0]

    url = "https://www.teamrankings.com/nba/trends/ats_trends/"
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]

    df = df.reset_index(drop=True)
    for x in range(df.shape[0]): 
        if df.at[x, 'Team'] == team: 
            wins = float((df.at[x, 'ATS Record']).split("-")[0])
            losses = float((df.at[x, 'ATS Record']).split("-")[1])
    pct = wins/(wins+losses)
    return pct

def get_player_game_log_current(player, team, season):
    # print("team in get_player_game_log: ", team) 
    roster = get_roster_excel(team_name_mapping.get(get_city(team), get_city(team)), season)
    bbref_url = None
    for row in range(roster.shape[0]): 
        if unidecode(roster.at[row, 'Player']) == player or unidecode(roster.at[row, 'Player']) == f'{player} Jr.' or unidecode(roster.at[row, 'Player']) == f'{player} (TW)' or unidecode(roster.at[row, 'Player']) == f'{player} Jr. (TW)' or unidecode(roster.at[row, 'Player']) == f'{player} Sr.' or unidecode(roster.at[row, 'Player']) == f'{player} Sr. (TW)': 
            bbref_url = roster.at[row, 'bbref url']
    if bbref_url == None: 
        raise Exception(f"Failed to find player game log for {player}!")
        return pd.DataFrame()
    return get_player_game_log(bbref_url, season)

def get_game_log_excel(team, year): 
    filepath = f'./gameLogs/{year}/{team}.xlsx'
    df = pd.read_excel(filepath)
    return df

def get_total_gmsc_current(team, date_beg, date_end, season): 
    total_gmsc = 0 
    roster = get_roster_excel(team, season)
    for row in range(roster.shape[0]): 
        player = unidecode(roster.at[row, 'Player'])
        player_game_log = get_player_game_log_current(player, team, season)
        #all the following for loop does is check that a) the player is on the team during a game and b) the game is between the given dates and if those two are true it adds the game score to the running total
        for row2 in range(player_game_log.shape[0]):
            if abrv_to_city(player_game_log.at[row2, 'Tm'], season) == team_name_mapping.get(get_city(team), get_city(team)): 
                date_string = str(player_game_log.at[row2, 'Date'])
                date_list = date_string.split(' ')[0].split('-')
                date_of_game = dt.date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
                # print("Date of game for checked player: ", date_of_game)
                if date_of_game < date_end and date_of_game >= date_beg: 
                    # print("Date was within time injured player was on team!")
                    try: 
                        gamescore = float(player_game_log.at[row2, 'GmSc'])
                        if gamescore < 0 or gamescore > 0: 
                            total_gmsc += gamescore
                    except ValueError:
                        gamescore = 0
                else: 
                    continue
    return total_gmsc

def get_mins_injured_current(team, season):  
    injured_players = get_current_injuries(team)
    total_ratio = 0
    for player in injured_players: 
        player_game_log = get_player_game_log_current(player, team, season)
        time_on_team = {}
        on_team = False
        mins_on_team = 0
        gp_on_team = 0
        for row in range(player_game_log.shape[0]): 
            date_string = str(player_game_log.at[row, 'Date'])
            date_list = date_string.split(' ')[0].split('-')
            date_of_game = dt.date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
            if abrv_to_city(player_game_log.at[row, 'Tm'], season) == team_name_mapping.get(get_city(team), get_city(team)): 
                gp_on_team += 1
                if not on_team: 
                    on_team = True
                    time_on_team[len(time_on_team)] = {'start': date_of_game, 'end': None}
                try: 
                    minutes_list = player_game_log.at[row, 'MP'].split(':')
                    minutes = float(minutes_list[0]) + (float(minutes_list[1])/60)
                    mins_on_team += minutes
                except ValueError:
                    minutes = 0
            elif abrv_to_city(player_game_log.at[row, 'Tm'], season) != team_name_mapping.get(get_city(team), get_city(team)) and on_team: 
                on_team = False
                time_on_team[len(time_on_team)-1]['end'] = date_of_game
        total_mins_while_on_team = gp_on_team * 240
        if total_mins_while_on_team > 0: 
            ratio = mins_on_team/total_mins_while_on_team
        else: ratio = 0
        total_ratio += ratio
    return total_ratio

def get_gmsc_injured_current(team, season): 
    injured_players = get_current_injuries(team)
    total_ratio = 0
    for player in injured_players: 
        player_game_log = get_player_game_log_current(player, team, season)
        time_on_team = {}
        on_team = False
        gmsc_on_team = 0
        for row in range(player_game_log.shape[0]): 
            date_string = str(player_game_log.at[row, 'Date'])
            date_list = date_string.split(' ')[0].split('-')
            date_of_game = dt.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
            if abrv_to_city(player_game_log.at[row, 'Tm'], season) == team_name_mapping.get(get_city(team), get_city(team)): 
                if not on_team: 
                    on_team = True
                    time_on_team[len(time_on_team)] = {'start': date_of_game, 'end': None}
                try: 
                    gamescore = float(player_game_log.at[row, 'GmSc'])
                    if gamescore < 0 or gamescore > 0: 
                        gmsc_on_team += gamescore
                except ValueError:
                    gamescore = 0
            elif abrv_to_city(player_game_log.at[row, 'Tm'], season) != team_name_mapping.get(get_city(team), get_city(team)) and on_team: 
                on_team = False
                time_on_team[len(time_on_team)-1]['end'] = date_of_game
            else: 
                continue
        # print("Time on team for player " + player + " during " + str(season) + " for team " + team)
        # print(time_on_team)
        total_gmsc_while_on_team = 0
        for stretch in range(len(time_on_team)): 
            start_date = time_on_team[stretch]['start']
            end_date = time_on_team[stretch]['end']
            if end_date == None: end_date = dt.date.today()
            total_gmsc_while_on_team += get_total_gmsc_current(team_name_mapping.get(get_city(team), get_city(team)), start_date, end_date, season)
        print("total gamescore while on team: ", total_gmsc_while_on_team)
        print("total gamescore for player: ", gmsc_on_team)
        if total_gmsc_while_on_team > 0: 
            ratio = gmsc_on_team/total_gmsc_while_on_team
        else: ratio = 0
        total_ratio += ratio
    return total_ratio

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

def get_league_scoring_average(year): 
    api_url = f"https://www.basketball-reference.com/leagues/NBA_{str(year)}.html#per_game-team"
    response = requests.get(api_url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', id='per_game-team')
    df = pd.read_html(str(table))[0]

    df = df.reset_index(drop=True)

    return df.at[30, 'PTS']

game_logs = {}
# Iterate over the list of teams and the range of years
for team in team_names:
    # Use the get_game_log function to retrieve the dataframe for the current team and year
    df = get_game_log(team, CURR_YEAR)
    # Add the dataframe to the dictionary with the key (team, year)
    game_logs[(team, CURR_YEAR)] = df
    # print("Generated game log for " + team + " in " + str(CURR_YEAR) + "...")
    time.sleep(4)
for team in team_names: 
    team_str = get_abbrv(team, CURR_YEAR)
    url = f"https://www.basketball-reference.com/teams/{team_str}/{str(CURR_YEAR)}.html"
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    roster = pd.read_html(str(table))[0]
    time.sleep(4)
    saved_roster = pd.read_excel(f"./rosters/{str(CURR_YEAR)}/{team}/{team}.xlsx")
    if not roster['Player'].equals(saved_roster['Player']):
        roster = get_roster(team, CURR_YEAR)
        time.sleep(4)
        roster.to_excel(f"./rosters/{str(CURR_YEAR)}/{team}/{team}.xlsx")
print("\n\n")
year = CURR_YEAR
ratings = get_2k_ratings(CURR_YEAR)
league_scoring_average = get_league_scoring_average(CURR_YEAR)
# print(league_scoring_average)
odds = get_odds().json()
# print(odds)
total_data = pd.DataFrame({'year': [], 'hitOver': [], 'total': [], 'avg_popularity': [], 'totalppg': [], 'size_of_spread': [], 'home_team': [], 'away_team': [], 'pct_overs_hit': [], 'pace': [], 'ortg': [], 'drtg': [], 'drb': [], 'threePAR': [], 'ts': [], 'ftr': [], 'd_tov': [], 'o_tov': [], 'ftperfga': [], 'points_over_average_ratio': [], 'hotness_ratio': [], 'std_dev': [], 'win_pct': [], 'rsw': [], 'ratings_2k': [], 'win_pct_close': [], 'mov_a': [], 'sos': [], 'injury_gmsc': [], 'injury_mins': []})
spread_data = pd.DataFrame({'year': [], 'home_spread_hit': [], 'total': [], 'spread': [], 'home_team': [], 'away_team': [], 'pct_spreads_hit_h': [], 'pct_spreads_hit_a': [], 'ppg_h': [], 'ppg_a': [], 'pace_h': [], 'pace_a': [], 'ortg_h': [], 'ortg_a': [], 'drtg_h': [], 'drtg_a': [], 'drb_h': [], 'drb_a': [], 'threePAR_h': [], 'threePAR_a': [], 'ts_h': [], 'ts_a': [], 'ftr_h': [], 'ftr_a': [], 'd_tov_h': [], 'd_tov_a': [], 'o_tov_h': [], 'o_tov_a': [], 'ftperfga_h': [], 'ftperfga_a': [], 'points_over_average_ratio_h': [], 'points_over_average_ratio_a': [], 'hotness_ratio_h': [], 'hotness_ratio_a': [], 'std_dev_h': [], 'std_dev_a': [], 'win_pct_h': [], 'win_pct_a': [], 'rsw_h': [], 'rsw_a': [], 'ratings_2k_h': [], 'ratings_2k_a': [], 'win_pct_close_h': [], 'win_pct_close_a': [], 'sos_h': [], 'sos_a': [], 'mov_a_h': [], 'mov_a_a': [], 'injury_gmsc_h': [], 'injury_gmsc_a': [], 'injury_mins_h': [], 'injury_mins_a': []})
for game in odds: 
    # print(game)
    bookmaker_id = 0
    while(len(game['bookmakers']) < bookmaker_id and len(game['bookmakers'][bookmaker_id]['markets']) != 2): 
        bookmaker_id += 1
    if len(game['bookmakers'][bookmaker_id]['markets'])>1: 
        # print("Size of spread: " + str(size_of_spread))
        total = float(game['bookmakers'][bookmaker_id]['markets'][1]['outcomes'][0]['point'])
        # print("Total: " + str(total))
        team1 = game['home_team']
        team2 = game['away_team']
        if game['bookmakers'][bookmaker_id]['markets'][0]['outcomes'][0]['name'] == team1: 
            spread = float(game['bookmakers'][bookmaker_id]['markets'][0]['outcomes'][0]['point'])
        else: 
            spread = float(game['bookmakers'][bookmaker_id]['markets'][0]['outcomes'][1]['point'])
        if spread < 0: size_of_spread = -1*spread
        else: size_of_spread = spread
        game_log_1 = game_logs[(team_name_mapping.get(get_city(team1), get_city(team1)), year)]
        game_log_2 = game_logs[(team_name_mapping.get(get_city(team2), get_city(team2)), year)] 

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
        for game_number in range(game_log_1.shape[0]): 
            pace1 += float(game_log_1.at[game_number, 'Pace'])
            ortg1 += float(game_log_1.at[game_number, 'ORtg'])
            drtg1 += float(game_log_1.at[game_number, 'DRtg'])
            drb1 += float(game_log_1.at[game_number, 'DRB%'])
            threePAR1 += float(game_log_1.at[game_number, '3PAr'])
            ts1 += float(game_log_1.at[game_number, 'TS%'])
            ftr1 += float(game_log_1.at[game_number, 'FTr'])
            d_tov1 += float(game_log_1.at[game_number, 'TOV%_1'])
            o_tov1 += float(game_log_1.at[game_number, 'TOV%_2'])
            ftperfga1 += ((float(game_log_1.at[game_number, 'FT/FGA_1'])) + float(game_log_1.at[game_number, 'FT/FGA_2']))/2
            points1.append(float(game_log_1.at[game_number, 'Tm']))
        for game in points1: 
            ppg1 += game

        if game_log_1.shape[0] > 0: 
            pace1 /= game_log_1.shape[0]
            ortg1 /= game_log_1.shape[0]
            drtg1 /= game_log_1.shape[0]
            drb1 /= game_log_1.shape[0]
            threePAR1 /= game_log_1.shape[0]
            ts1 /= game_log_1.shape[0]
            ftr1 /= game_log_1.shape[0]
            d_tov1 /= game_log_1.shape[0]
            o_tov1 /= game_log_1.shape[0]
            ftperfga1 /= game_log_1.shape[0]
            ppg1 /= game_log_1.shape[0]

        points2 = []
        for game_number in range(game_log_2.shape[0]): 
            pace2 += float(game_log_2.at[game_number, 'Pace'])
            ortg2 += float(game_log_2.at[game_number, 'ORtg'])
            drtg2 += float(game_log_2.at[game_number, 'DRtg'])
            drb2 += float(game_log_2.at[game_number, 'DRB%'])
            threePAR2 += float(game_log_2.at[game_number, '3PAr'])
            ts2 += float(game_log_2.at[game_number, 'TS%'])
            ftr2 += float(game_log_2.at[game_number, 'FTr'])
            d_tov2 += float(game_log_2.at[game_number, 'TOV%_1'])
            o_tov2 += float(game_log_2.at[game_number, 'TOV%_2'])
            ftperfga2 += ((float(game_log_2.at[game_number, 'FT/FGA_1'])) + float(game_log_2.at[game_number, 'FT/FGA_2']))/2
            points2.append(float(game_log_2.at[game_number, 'Tm']))
        for game in points2: 
            ppg2 += game
        
        if game_log_2.shape[0] > 0: 
            ftperfga2 /= game_log_2.shape[0]
            o_tov2 /= game_log_2.shape[0]
            d_tov2 /= game_log_2.shape[0]
            ftr2 /= game_log_2.shape[0]
            ts2 /= game_log_2.shape[0]
            threePAR2 /= game_log_2.shape[0]
            drb2 /= game_log_2.shape[0]
            drtg2 /= game_log_2.shape[0]
            ortg2 /= game_log_2.shape[0]
            pace2 /= game_log_2.shape[0]
            ppg2 /= game_log_2.shape[0]

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

        points_over_average_ratio1 = ppg1/league_scoring_average
        points_over_average_ratio2 = ppg2/league_scoring_average
        points_over_average_ratio = totalppg / league_scoring_average

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

        std_dev1 = calc_std_dev(points1)
        std_dev2 = calc_std_dev(points2)
        std_dev = (std_dev1 + std_dev2)/2

        rating1 = get_ratings(CURR_YEAR, team1)
        rating2 = get_ratings(CURR_YEAR, team2)
        rating = (rating1 + rating2)/2

        wins1 = 0
        games1 = 0
        wins1close = 0
        games1close = 0
        wins2 = 0
        games2 = 0
        wins2close = 0
        games2close = 0
        for row in range(game_log_1.shape[0]): 
            if game_log_1.at[row, 'W/L'] == 'W': 
                wins1 += 1
            games1 += 1
            if abs(int(game_log_1.at[row, 'Tm']) - int(game_log_1.at[row, 'Opp'])) < CLOSE_GAME_THRESHOLD: 
                if game_log_1.at[row, 'W/L'] == 'W': 
                    wins1close += 1
                games1close += 1
        for row in range(game_log_2.shape[0]): 
            if game_log_2.at[row, 'W/L'] == 'W': 
                wins2 += 1
            games2 += 1
            if abs(int(game_log_2.at[row, 'Tm']) - int(game_log_2.at[row, 'Opp'])) < CLOSE_GAME_THRESHOLD: 
                if game_log_2.at[row, 'W/L'] == 'W': 
                    wins2close += 1
                games2close += 1
        win_pct1 = wins1/games1
        win_pct2 = wins2/games2
        win_pct = (win_pct1 + win_pct2)/2
        win_pct_close1 = wins1close/games1close
        win_pct_close2 = wins2close/games2close
        win_pct_close = (win_pct_close1 + win_pct_close2)/2

        #rsw
        preseason_odds = get_rsw_odds_excel(CURR_YEAR)
        rsw1 = 0
        rsw2 = 0
        for team in range(preseason_odds.shape[0]): 
            if preseason_odds.at[team, 'Team'] == team1: 
                rsw1 = preseason_odds.at[team, 'W-L O/U']
            elif preseason_odds.at[team, 'Team'] == team2: 
                rsw2 = preseason_odds.at[team, 'W-L O/U']
        rsw = (rsw1+rsw2)/2

        # adjusted MOV 
        mov_ratings_for_year = get_mov_excel(CURR_YEAR-1)
        mov_a_h = 0
        mov_a_a = 0
        for team in range(mov_ratings_for_year.shape[0]): 
            if mov_ratings_for_year.at[team, 'Team'] == team1: 
                mov_a_h = mov_ratings_for_year.at[team, 'MOV/A']
            elif mov_ratings_for_year.at[team, 'Team'] == team2: 
                mov_a_a = mov_ratings_for_year.at[team, 'MOV/A']
        mov_a = (mov_a_h + mov_a_a)/2

        #injuries
        injury_mins1 = get_mins_injured_current(team1, CURR_YEAR)
        injury_mins2 = get_mins_injured_current(team2, CURR_YEAR)
        injury_gmsc1 = get_gmsc_injured_current(team1, CURR_YEAR)
        injury_gmsc2 = get_gmsc_injured_current(team2, CURR_YEAR)
        # injury_gmsc1 = 0
        # injury_gmsc2 = 0
        injury_mins = (injury_mins1 + injury_mins2)/2
        injury_gmsc = (injury_gmsc1 + injury_gmsc2)/2

        #strength of schedule
        home_sos_array = []
        away_sos_array = []
        team_names_spreadsheet = [ "Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "GoldenState", "Houston", "Indiana", "LAClippers", "LALakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "NewOrleans", "NewYork", "OklahomaCity", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "SanAntonio", "Toronto", "Utah", "Washington"]
        team_abbrvs = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
        index = 31
        for row in range(game_log_1.shape[0]): 
            opp_abrv = game_log_1.at[row, 'Opp_team']
            date_string = str(game_log_1.at[row, 'Date'])
            date_list = date_string.split(' ')[0].split('-')
            date_of_game = dt.date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
            for x in range(len(team_abbrvs)): 
                if team_abbrvs[x] == opp_abrv: 
                    index = x
            opp_team = team_names_spreadsheet[index]
            opp_game_log = game_logs[(team_name_mapping.get(opp_team, opp_team), CURR_YEAR)]
            wins = 0
            losses = 0
            for row2 in range(opp_game_log.shape[0]): 
                date_string2 = str(opp_game_log.at[row2, 'Date'])
                date_list2 = date_string2.split(' ')[0].split('-')
                date_of_game2 = dt.date(int(date_list2[0]), int(date_list2[1]), int(date_list2[2])) 
                if date_of_game2 < date_of_game: 
                    if opp_game_log.at[row2, 'W/L'] == 'W': 
                        wins += 1
                    else: 
                        losses += 1
                else: 
                    break
            if wins+losses > 0: 
                winpct = wins/(wins+losses)
            else: winpct = 0
            home_sos_array.append(winpct)
        index = 31
        for row in range(game_log_2.shape[0]): 
            opp_abrv = game_log_2.at[row, 'Opp_team']
            date_string = str(game_log_2.at[row, 'Date'])
            date_list = date_string.split(' ')[0].split('-')
            date_of_game = dt.date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
            for x in range(len(team_abbrvs)): 
                if team_abbrvs[x] == opp_abrv: 
                    index = x
            opp_team = team_names_spreadsheet[index]
            opp_game_log = game_logs[(team_name_mapping.get(opp_team, opp_team), CURR_YEAR)]
            wins = 0
            losses = 0
            for row2 in range(opp_game_log.shape[0]): 
                date_string2 = str(opp_game_log.at[row2, 'Date'])
                date_list2 = date_string2.split(' ')[0].split('-')
                date_of_game2 = dt.date(int(date_list2[0]), int(date_list2[1]), int(date_list2[2])) 
                if date_of_game2 < date_of_game: 
                    if opp_game_log.at[row2, 'W/L'] == 'W': 
                        wins += 1
                    else: 
                        losses += 1
                else: 
                    break
            if wins+losses > 0:
                winpct = wins/(wins+losses)
            else: winpct = 0
            away_sos_array.append(winpct)
        sos1 = average(home_sos_array)
        sos2 = average(away_sos_array)
        sos = (sos1 + sos2)/2

        total_data.loc[len(total_data.index)] = [year, None, total, None, totalppg, size_of_spread, get_city(team1), get_city(team2), get_pct_overs_hit(team1, team2), pace, ortg, drtg, drb, threePAR, ts, ftr, d_tov, o_tov, ftperfga, points_over_average_ratio, hotness_ratio, std_dev, win_pct, rsw, rating, win_pct_close, sos, mov_a, injury_gmsc, injury_mins]
        spread_data.loc[len(spread_data.index)] = [year, None, total, spread, get_city(team1), get_city(team2), get_pct_spreads_hit(team1), get_pct_spreads_hit(team2), ppg1, ppg2, pace1, pace2, ortg1, ortg2, drtg1, drtg2, drb1, drb2, threePAR1, threePAR2, ts1, ts2, ftr1, ftr2, d_tov1, d_tov2, o_tov1, o_tov2, ftperfga1, ftperfga2, points_over_average_ratio1, points_over_average_ratio2, hotness_ratio1, hotness_ratio2, std_dev1, std_dev2, win_pct1, win_pct2, rsw1, rsw2, rating1, rating2, win_pct_close1, win_pct_close2, sos1, sos2, mov_a_h, mov_a_a, injury_gmsc1, injury_gmsc2, injury_mins1, injury_mins2]
    else: 
        team1 = game['home_team']
        team2 = game['away_team']
        print(f"NOTE: missing odds for game {team2} at {team1}")


df_total = logit_total(total_data)
df_total.to_excel("current_games_total.xlsx")
df_spread = logit_spread(spread_data)
df_spread.to_excel("current_games_spread.xlsx")
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
print("\n")
print("Generating tweet... \n")
run_tweet_gen(pick_string, round(float(pct), 2))