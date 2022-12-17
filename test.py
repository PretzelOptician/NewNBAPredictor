import pandas as pd
from bs4 import BeautifulSoup
import requests

# year = 2022
# api_url = "https://www.basketball-reference.com/teams/BRK/2022/gamelog/?sr&amp;utm_source=direct&amp;utm_medium=Share&amp;utm_campaign=ShareTool#tgl_basic"
# response = requests.get(api_url) 
# soup = BeautifulSoup(response.content, 'html.parser')
# table = soup.find('table')
# leagueData = pd.read_html(str(table))[0]
# leagueData.columns = leagueData.columns.droplevel(level=0)
# # print(leagueData)
# # Convert the 'G' column to a numeric type and store in a new column 'G_num'
# leagueData['G_num'] = pd.to_numeric(leagueData['G'], errors='coerce')

# # Filter the rows where 'G_num' is not null
# df = leagueData[leagueData['G_num'].notnull()]
# df = df.reset_index(drop=True)
# pd.set_option('display.max_rows', None)
# print(df)

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
    elif team == 'NewYork': return 'NYK'
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
    print(team_str)
    print(year_str)

    api_url = f"https://www.basketball-reference.com/teams/{team_str}/{year_str}/gamelog-advanced/?sr&utm_source=direct&utm_medium=Share&utm_campaign=ShareTool#tgl_advanced"
    print(api_url)
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

print(get_game_log("Cleveland", 2017))

# Iterate over the list of teams and the range of years
for team in team_names:
    for year in range(2014, 2022):
        # Use the get_game_log function to retrieve the dataframe for the current team and year
        df = get_game_log(team, year)
        # Add the dataframe to the dictionary with the key (team, year)
        game_logs[(team, year)] = df
        print("Generated game log for " + team + " in " + str(year) + "...")

team1 = "New York"
print(game_logs[(team_name_mapping.get(team1, team1), year)])
team1 = "SanAntonio"
print(game_logs[(team_name_mapping.get(team1, team1), year)])
team1 = "Minnesota"
print(game_logs[(team_name_mapping.get(team1, team1), year)])

