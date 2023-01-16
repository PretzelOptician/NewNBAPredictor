import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import datetime
from datetime import date

team_names = [ "Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]

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

def get_league_scoring_average(year): 
    points = 0
    games_played = 0
    for team in team_names: 
        game_log = get_game_log(team, year)
        for game in range(game_log.shape[0]): 
            points += int(game_log.at[game, 'Tm'])
            games_played += 1
    return (points/games_played)

def get_pct_overs_hit(team1, team2): 
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

df = pd.read_excel('./test.xlsx')
# print(df.at[1, 'GS'])
date = datetime.date(2022, 10, 25)
injured = False
# print(df.shape[0])
for row2 in range(df.shape[0]): 
    # print("what")
    #get date of the row and turn it to variable "date_of_game"
    date_string = str(df.at[row2, 'Date'])
    date_list = date_string.split(' ')[0].split('-')
    date_of_game = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    # print(date_of_game)
    if date_of_game == date: 
        # if 'inactive', set injured to True
        # print(df.at[row2, 'GS'])
        if df.at[row2, 'GS'] == "Inactive": 
            injured = True
        break
gmsc_sum = 0
for row2 in range(df.shape[0]): 
    gamescore = df.at[row2, 'GmSc']
    if gamescore < 0 or gamescore > 0: 
        gmsc_sum += gamescore
    print(gmsc_sum)