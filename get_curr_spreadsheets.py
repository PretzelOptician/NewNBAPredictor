import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import math
import numpy as np

CURR_YEAR = 2023

pd.set_option('display.max_rows', None)

def get_city(team): 
    if team == 'Golden State Warriors': return 'GoldenState'
    elif team == 'Los Angeles Clippers': return 'LAClippers'
    elif team == 'Los Angeles Lakers': return 'LALakers'
    elif team == 'New Orleans Pelicans': return 'NewOrleans'
    elif team == 'New York Knicks': return 'NewYork'
    elif team == 'Oklahoma City Thunder': return 'OklahomaCity'
    elif team == 'San Antonio Spurs': return 'SanAntonio'
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

def logit(df): 
    # home_dummy = {
    #     'Atlanta': 0.0,
    #     'Boston': -0.0049771,
    #     'Brooklyn': -0.0976231,
    #     'Charlotte': -0.1616863,
    #     'Chicago': -0.1792073,
    #     'Cleveland': -0.09652,
    #     'Dallas': -0.1852565, 
    #     'Denver': 0.1810079, 
    #     'Detroit': 0.1986823,
    #     'GoldenState': -0.255966,
    #     'Houston': 0.0367426, 
    #     'Indiana': -0.0293679, 
    #     'LAClippers': -0.065803, 
    #     'LALakers': -0.2043106, 
    #     'Memphis': -0.1364876, 
    #     'Miami': 0.0986813, 
    #     'Milwaukee': 0.0950917, 
    #     'Minnesota': 0.1531429,
    #     'NewOrleans': 0.3482693, 
    #     'NewYork': -0.1498722, 
    #     'OklahomaCity': -0.0853131, 
    #     'Orlando': 0.0034486, 
    #     'Philadelphia': 0.0431477, 
    #     'Phoenix': 0.1017284, 
    #     'Portland': 0.045715, 
    #     'Sacramento': 0.1420166, 
    #     'SanAntonio': 0.0354622, 
    #     'Toronto': 0.0958902, 
    #     'Utah': -0.2651519, 
    #     'Washington': 0.1219588, 
    # }
    # away_dummy = {
    #     'Atlanta': 0.0,
    #     'Boston': 0.082884,
    #     'Brooklyn': 0.0886438,
    #     'Charlotte': 0.1817,
    #     'Chicago': -0.0423023,
    #     'Cleveland': 0.1211452,
    #     'Dallas': -0.0623778, 
    #     'Denver': 0.1134192, 
    #     'Detroit': -0.133122,
    #     'GoldenState': -0.2301149,
    #     'Houston': -0.0220769, 
    #     'Indiana': 0.0618522, 
    #     'LAClippers': 0.0357576, 
    #     'LALakers': 0.1241524, 
    #     'Memphis': 0.0785158, 
    #     'Miami': -0.1313578, 
    #     'Milwaukee': 0.1319199, 
    #     'Minnesota': 0.3885524,
    #     'NewOrleans': 0.0353463, 
    #     'NewYork': 0.042184, 
    #     'OklahomaCity': -0.0733661, 
    #     'Orlando': -0.1777448, 
    #     'Philadelphia': -0.1730964, 
    #     'Phoenix': 0.0218554, 
    #     'Portland': 0.2001103, 
    #     'Sacramento': 0.0612493, 
    #     'SanAntonio': 0.1352708, 
    #     'Toronto': 0.1909384, 
    #     'Utah': -0.1020129, 
    #     'Washington': 0.2796706,
    # }
    
    #chatGPT code:: 
    # Extract the relevant columns from the dataframe
    X = df[['total', 'size_of_spread', 'pct_overs_hit', 'ortg', 'drtg', 'drb', 'threePAR', 'ts', 'ftr', 'points_over_average_ratio', 'hotness_ratio', 'std_dev']]
    # Add a column of consts to the dataframe to represent the intercept term
    X['intercept'] = 4.644535
    coefs = [0.0040295, 0.0120225, -0.392392, 0.028596,  -0.0214184, -0.0128709, 0.8110862, -6.346099, -0.7018032, -2.42325, 0.5000966, 0.0161823, 1]
    z = np.dot(X, coefs)
    # for game in range(len(z)): 
    #     home_dummy_val = home_dummy.get(df.at[game, 'home_team'])
    #     away_dummy_val = away_dummy.get(df.at[game, 'away_team'])
    #     z[game] += (home_dummy_val + away_dummy_val)
    prob = 1 / (1 + np.exp(-z))
    # Calculate the probability using the sigmoid function
    #THIS ALL WORKS LMAO
    df['calc_over_prob'] = prob
    return df

def get_avg_followers(team): 
    if team == 'LALakers' or team == 'LA Lakers' or team == 'Los Angeles Lakers': return 52321433
    elif team == 'Cleveland' or team == 'Cleveland Cavaliers': return 23853389
    elif team == 'Boston' or team == 'Boston Celtics': return 19952367
    elif team == 'Milwaukee' or team == 'Milwaukee Bucks': return 10288717
    elif team == 'Chicago' or team == 'Chicago Bulls': return 30435628
    elif team == 'Portland' or team == 'Portland Trail Blazers': return 7117111
    elif team == 'Toronto' or team == 'Toronto Raptors': return 8798856
    elif team == 'Philadelphia' or team == 'Philadelphia 76ers': return 7925637
    elif team == 'Atlanta' or team == 'Atlanta Hawks': return 5635700
    elif team == 'Orlando' or team == 'Orlando Magic': return 6161629
    elif team == 'Brooklyn' or team == 'Brooklyn Nets': return 9902212
    elif team == 'Washington' or team == 'Washington Wizards': return 8209114
    elif team == 'Miami' or team == 'Miami Heat': return 25825318
    elif team == 'NewYork' or team == 'New York Knicks': return 11755482
    elif team == 'Indiana' or team == 'Indiana Pacers': return 6768683
    elif team == 'Detroit' or team == 'Detroit Pistons': return 4443090
    elif team == 'OklahomaCity' or team == 'Oklahoma City' or team == 'Oklahoma City Thunder': return 14379492
    elif team == 'Sacramento' or team == 'Sacramento Kings': return 10624663
    elif team == 'Minnesota' or team == 'Minnesota Timberwolves': return 5790088
    elif team == 'Phoenix' or team == 'Phoenix Suns': return 6479573
    elif team == 'SanAntonio' or team == 'San Antonio' or team == 'San Antonio Spurs': return 14554210
    elif team == 'Memphis' or team == 'Memphis Grizzlies': return 5430199
    elif team == 'Denver' or team == 'Denver Nuggets': return 5618580
    elif team == 'Houston' or team == 'Houston Rockets': return 25544036
    elif team == 'Utah' or team == 'Utah Jazz': return 8164010
    elif team == 'NewOrleans' or team == 'New Orleans' or team == 'New Orleans Pelicans': return 6016902
    elif team == 'GoldenState' or team == 'Golden State' or team == 'Golden State Warriors': return 48149619
    elif team == 'LAClippers' or team == 'LA Clippers' or team == 'Los Angeles Clippers': return 10709842
    elif team == 'Charlotte' or team == 'Charlotte Hornets': return 5802049
    elif team == 'Dallas' or team == 'Dallas Mavericks': return 10535695

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

year = CURR_YEAR
ratings = get_2k_ratings(CURR_YEAR)
league_scoring_average = get_league_scoring_average(CURR_YEAR)
# print(league_scoring_average)
odds = get_odds().json()
# print(odds)
total_data = pd.DataFrame({'year': [], 'hitOver': [], 'total': [], 'avg_popularity': [], 'totalppg': [], 'size_of_spread': [], 'home_team': [], 'away_team': [], 'pct_overs_hit': [], 'pace': [], 'ortg': [], 'drtg': [], 'drb': [], 'threePAR': [], 'ts': [], 'ftr': [], 'd_tov': [], 'o_tov': [], 'ftperfga': [], 'points_over_average_ratio': [], 'hotness_ratio': [], 'std_dev': [], 'win_pct': [], 'rsw': [], 'ratings_2k': []})
for game in odds: 
    if len(game['bookmakers'][0]['markets'])>1: 
        size_of_spread = float(game['bookmakers'][0]['markets'][0]['outcomes'][0]['point'])
        if size_of_spread < 0: size_of_spread *= -1
        print("Size of spread: " + str(size_of_spread))
        total = float(game['bookmakers'][0]['markets'][1]['outcomes'][0]['point'])
        print("Total: " + str(total))
        team1 = game['home_team']
        team2 = game['away_team']
        game_log_1 = get_game_log(team1, CURR_YEAR)
        game_log_2 = get_game_log(team2, CURR_YEAR)   

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

        avg_followers = (get_avg_followers(team2) + get_avg_followers(team1))/2

        std_dev1 = calc_std_dev(points1)
        std_dev2 = calc_std_dev(points2)
        std_dev = (std_dev1 + std_dev2)/2

        total_data.loc[len(total_data.index)] = [year, None, total, avg_followers, totalppg, size_of_spread, get_city(team1), get_city(team2), get_pct_overs_hit(team1, team2), pace, ortg, drtg, drb, threePAR, ts, ftr, d_tov, o_tov, ftperfga, points_over_average_ratio, hotness_ratio, std_dev, None, None, None]
        #last 3 vars: win_pct, rsw, rating

print(total_data)
total_data.to_excel("current_games.xlsx")
df = logit(total_data)
for x in range(df.shape[0]):
    total = df.at[x, 'total'] 
    over_prob = df.at[x, 'calc_over_prob']
    letter = 'o' if over_prob > 0.5 else 'u'
    away_team = df.at[x, 'away_team']
    home_team = df.at[x, 'home_team']
    pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
    print(f'{away_team} at {home_team}: {letter}{str(total)} with probability {pct}%')
print("\n Bets greater than 53%: ")
for x in range(df.shape[0]): 
    total = df.at[x, 'total'] 
    over_prob = df.at[x, 'calc_over_prob']
    letter = 'o' if over_prob > 0.5 else 'u'
    away_team = df.at[x, 'away_team']
    home_team = df.at[x, 'home_team']
    pct = str(over_prob*100) if letter=='o' else str(100-over_prob*100)
    if float(pct) > 53: 
        print(f'{away_team} at {home_team}: {letter}{str(total)} with probability {pct}%')