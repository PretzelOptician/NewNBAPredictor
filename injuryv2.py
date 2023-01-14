import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
from datetime import datetime
import calendar
from unidecode import unidecode
import time

### second attempt at generating injury history

def string_to_datetime(date_string):
    return datetime.strptime(date_string, '%B %d, %Y')

def get_roster(team, year): 
    #team must be the abbreviation
    team = get_abbrv(team, year)
    url = f"https://www.basketball-reference.com/teams/{team}/{str(year)}.html"
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    roster = pd.read_html(str(table))[0]
    urls = []
    for row in range(roster.shape[0]): 
        name = roster.at[row, 'Player']
        dob = string_to_datetime(roster.at[row, 'Birth Date']).date()
        urls.append(get_player_profile_url(name, dob))
        time.sleep(2)
    roster['bbref url'] = urls
    return roster

def get_roster_excel(team, year): 
    df = pd.read_excel(f"./rosters/{year}/{team}.xlsx")
    return df

#not necessary
def get_rosters(team1, team2, date): 
    if date.month > 9 or date.month == 9 and date.day > 14: 
        season = date.year+1
    else: 
        season = date.year 
    unprocessed_roster_1 = get_roster_excel(team1, season)
    unprocessed_roster_2 = get_roster_excel(team2, season)


# dob: date of birth, should be date object
# name: player name, should be decoded
def get_player_profile_url(name, dob): 
    print(("Getting URL for player " + name).encode('utf-8'))
    name = name.replace(".", "").replace("'", "")
    i = 1
    names_list = name.split(' ')
    base_string = (unidecode(names_list[1][0:5]) + unidecode(names_list[0][0:2])).lower()
    if name == "Clint Capela": base_string = "capelca"
    elif name == "Edy Tavares": base_string = "tavarwa"
    elif unidecode(name) == "Vitor Luiz Faverani": base_string = "favervi"
    elif name == "Gigi Datome": base_string = "datomlu"
    elif name == "Enes Freedom": base_string = "kanteen"
    elif name == "Michael Kidd-Gilchrist": base_string = "kiddgmi"
    elif name == "Mo Williams": base_string = "willima"
    elif name == "Cedi Osman": base_string = "osmande"
    if name == "PJ Hairston": 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}02.html"
    else: 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}01.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(str(soup.find('div', id='info')).encode('utf-8'))
    # print(str(soup.find('span', id='necro-birth')).encode('utf-8'))
    print(base_string)
    # print(soup.encode('utf-8'))
    print(url)
    birth = str(soup.find('span', id='necro-birth')).split('"')[1]
    birth_list = birth.split('-')
    birth_date = date(int(birth_list[0]), int(birth_list[1]), int(birth_list[2]))
    print(birth_date == dob)
    while(birth_date != dob): 
        i += 1
        if name == "Chaundee Brown Jr": i = 5
        elif name == "Alondes Williams (TW)": i = 6
        elif name == "PJ Hairston" or name == "P.J. Hairston": i = 2
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}0{i}.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(str(soup.find('div', id='info')).encode('utf-8'))
        # print(str(soup.find('span', id='necro-birth')).encode('utf-8'))
        birth = str(soup.find('span', id='necro-birth')).split('"')[1]
        birth_list = birth.split('-')
        birth_date = date(int(birth_list[0]), int(birth_list[1]), int(birth_list[2]))
    print(url)
    return url

#STUB: get the bbref game log for a player. 
## REMEMBER TO ANGLICIZE FOREIGN NAMES (unidecode)
def get_player_game_log(bbref_url, season): 
    #in caller function, make sure that a game log doesn't already exist.
    #remove last 5 characters from bbref_url. 
    #add '/gamelog/{season}' to string
    #get table on page and convert to dataframe
    #check which teams this player played for this season ('Tm' column in dataframe). put game logs in all the appropriate folders. 
    return

#STUB: get the player game log for a player during that season from local files
def get_player_game_log_excel(player, team, season): 
    filepath = f'./rosters/{season}/{team}/{player}.xlsx'
    df = pd.read_excel(filepath)
    return df

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

## date must be a valid nba game date
## NOT DONE YET
def get_injuries_for_team(team, date): 
    if date.month > 9 or date.month == 9 and date.day > 14: 
        season = date.year+1
    else: 
        season = date.year 
    roster = get_roster_excel(team, season)
    injured_list = []
    for row in range(roster.shape[0]): 
        bbref_url = roster.at[row, 'bbref url']
        name = unidecode(roster.at[row, 'Player'])
        player_game_log = get_player_game_log_excel(name, team, season)
        injured = False
        for row2 in range(player_game_log.shape[0]): 
            #get date of the row and turn it to variable "date_of_game"
            if date_of_game == date: 
                # if 'inactive', set injured to True
                print(injured)
            else: 
                break
        if injured: 
            injured_list.append(name)
    return injured_list

def get_pcts_injured(team, date): 
    if date.month > 9 or date.month == 9 and date.day > 14: 
        season = date.year+1
    else: 
        season = date.year 
    injured_players = get_injuries_for_team(team, date)
    team_contribution_sum = 0
    for player in injured_players: 
        player_game_log = get_player_game_log_excel(player, team, season)
        # sum up all points, rebounds, assists, steals, and blocks up to that point from when player has been on the team. 
        # sum up all team's points, rebounds, assists, steals, and blocks during the time that the player has been on the team and playing. 
        # average all of these ratios to get a general team contribution score and add this to the running total. 
    return team_contribution_sum

team_names = [ "Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]
years = range(2014, 2024)

for team in team_names:
    for year in years:
        # Construct the file path for the game log file
        file_path = f'./rosters/{year}/{team}/{team}.xlsx'

        # Check if the file already exists
        if not os.path.exists(file_path):
            # Generate the game log dataframe
            roster = get_roster(team, year)

            # Create the directory for the year if it doesn't exist
            year_dir = f'./rosters/{year}'
            if not os.path.exists(year_dir):
                os.makedirs(year_dir)

            # Create the directory for the team if it doesn't exist
            team_dir = f'./rosters/{year}/{team}'
            if not os.path.exists(team_dir): 
                os.makedirs(team_dir)

            # Save the game log dataframe to a .xlsx file
            roster.to_excel(file_path)