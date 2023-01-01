import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

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

team_names = [ "Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]
years = range(2014, 2024)


for team in team_names:
    for year in years:
        # Construct the file path for the game log file
        file_path = f'./gameLogs/{year}/{team}.xlsx'

        # Check if the file already exists
        if not os.path.exists(file_path):
            # Generate the game log dataframe
            game_log = get_game_log(team, year)

            # Create the directory for the year if it doesn't exist
            year_dir = f'./gameLogs/{year}'
            if not os.path.exists(year_dir):
                os.makedirs(year_dir)

            # Save the game log dataframe to a .xlsx file
            game_log.to_excel(file_path)