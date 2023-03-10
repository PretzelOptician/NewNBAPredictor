import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
from datetime import datetime
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
        time.sleep(3)
    roster['bbref url'] = urls
    return roster

def get_roster_excel(team, year): 
    df = pd.read_excel(f"./rosters/{year}/{team}/{team}.xlsx")
    return df


# dob: date of birth, should be date object
# name: player name, should be decoded
def get_player_profile_url(name, dob): 
    print(("Getting URL for player " + name).encode('utf-8'))
    name = name.replace(".", "").replace("'", "")
    i = 1
    names_list = name.split(' ')
    if name == "Clint Capela": base_string = "capelca"
    elif name == "Edy Tavares": base_string = "tavarwa"
    elif unidecode(name) == "Vitor Luiz Faverani": base_string = "favervi"
    elif name == "Gigi Datome": base_string = "datomlu"
    elif name == "Enes Freedom": base_string = "kanteen"
    elif name == "Michael Kidd-Gilchrist": base_string = "kiddgmi"
    elif name == "Mo Williams": base_string = "willima"
    elif name == "Cedi Osman": base_string = "osmande"
    elif name == "JJ Barea": base_string = "bareajo"
    elif name == "Maxi Kleber": base_string = "klebima"
    elif name == "Frank Ntilikina": base_string = "ntilila"
    elif name == "James Michael McAdoo": base_string = "mcadoja"
    elif unidecode(name) == "Nene": base_string = "hilarne"
    elif name == "Luc Mbah a Moute": base_string = "mbahalu"
    elif name == "Jeff Ayres": base_string = "pendeje"
    elif name == "Metta World Peace": base_string = "artesro"
    elif name == "Henry Walker": base_string = "walkebi"
    elif name == "Didi Louzada": base_string = "louzama"
    elif name == "Nando De Colo": base_string = "decolna"
    elif unidecode(name) == "Tibor Pleiss": base_string = "pleisti"
    elif name == "Sheldon Mac": base_string = "mcclesh"
    elif unidecode(name) == "Sasha Pavlovic": base_string = "pavloal"
    elif name == "Juan Carlos Navarro": base_string = "navarju"
    elif name == "Marcus Vinicius": base_string = "vincima"
    elif name == "Mouhamed Sene": base_string = "senesa"
    else: base_string = (unidecode(names_list[1][0:5]) + unidecode(names_list[0][0:2])).lower()
    if name == "PJ Hairston" or name == "Markus Howard" or name == "Xavier Munford" or name == "Killian Tillie" or name == "Bobby Jones": 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}02.html"
    elif name == "George King" or name == "Brandon Williams": 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}03.html"
    elif name == "Jalen Jones" or name == "Jalen Smith": 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}04.html"
    elif name == "Jalen Green" or name == "Jabari Smith Jr": 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}05.html"
    elif name == "Johnny Davis": 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}06.html"
    elif name == "Jaylin Williams": 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}07.html"
    elif name == "David Johnson": 
        url = f"https://www.basketball-reference.com/players/{base_string[0]}/{base_string}08.html"
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
    time.sleep(3)
    game_log_url = bbref_url[:-5] + f"/gamelog/{season}"
    response = requests.get(game_log_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', id='pgl_basic')
    df = pd.read_html(str(table))[0]
    df['Rk_num'] = pd.to_numeric(df['Rk'], errors='coerce')
    df = df[df['Rk_num'].notnull()]
    df = df.reset_index(drop=True)
    #check which teams this player played for this season ('Tm' column in dataframe). put game logs in all the appropriate folders. 
    return df

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
    elif team == 'NewJersey' or team == 'New Jersey': return 'NJN'
    elif team == 'Washington': return 'WAS'
    elif team == 'Miami': return 'MIA'
    elif team == 'NewYork' or team == 'New York': return 'NYK'
    elif team == 'Indiana': return 'IND'
    elif team == 'Detroit': return 'DET'
    elif team == 'OklahomaCity' or team == 'Oklahoma City': return 'OKC'
    elif team == 'Seattle': return 'SEA'
    elif team == 'Sacramento': return 'SAC'
    elif team == 'Minnesota': return 'MIN'
    elif team == 'Phoenix': return 'PHO'
    elif team == 'SanAntonio' or team == 'San Antonio': return 'SAS'
    elif team == 'Memphis': return 'MEM'
    elif team == 'Denver': return 'DEN'
    elif team == 'Houston': return 'HOU'
    elif team == 'Utah': return 'UTA'
    elif team == 'NewOrleans' or team == 'New Orleans': 
        if year < 2014: return 'NOH'
        else: return 'NOP'
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
        name = unidecode(roster.at[row, 'Player'])
        player_game_log = get_player_game_log_excel(name, team, season)
        injured = False
        for row2 in range(player_game_log.shape[0]): 
            date_string = str(player_game_log.at[row2, 'Date'])
            date_list = date_string.split(' ')[0].split('-')
            date_of_game = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
            # print(date_of_game)
            if date_of_game == date: 
                # if 'inactive', set injured to True
                # print(df.at[row2, 'GS'])
                if player_game_log .at[row2, 'GS'] == "Inactive" or player_game_log .at[row2, 'GS'] == "Not With Team" or player_game_log .at[row2, 'GS'] == "Did Not Dress": 
                    injured = True
                break
        if injured: 
            injured_list.append(name)
    return injured_list

def abrv_to_city(team_code, season): 
    team_names = { 'pre2009': ["Atlanta", "Boston", "New Jersey", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Seattle", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'pre2013': ["Atlanta", "Boston", "New Jersey", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'pre2014': ["Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'pre2015': ["Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'post2015': ["Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]}
    team_abbrvs = { 'pre2009': ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'SEA', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'], 'pre2013': ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'], 'pre2014': ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'], 'pre2015': ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'], 'post2015': ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']}
    if season < 2009: category = 'pre2009'
    elif season < 2013: category = 'pre2013'
    elif season < 2014: category = 'pre2014'
    elif season < 2015: category = 'pre2015'
    else: category = 'post2015'
    index = 31
    for abbr in range(len(team_abbrvs[category])): 
        if team_code == team_abbrvs[category][abbr]: 
            index = abbr
            break
    return team_names[category][index]

def get_total_gmsc_during_date(team, date_beg, date_end): 
    if date_beg.month > 9 or date_beg.month == 9 and date_beg.day > 14: 
        season = date_beg.year+1
    else: 
        season = date_beg.year 
    total_gmsc = 0 
    roster = get_roster_excel(team, season)
    for row in range(roster.shape[0]): 
        player = unidecode(roster.at[row, 'Player'])
        player_game_log = get_player_game_log_excel(player, team, season)
        #all the following for loop does is check that a) the player is on the team during a game and b) the game is between the given dates and if those two are true it adds the game score to the running total
        for row2 in range(player_game_log.shape[0]):
            if abrv_to_city(player_game_log.at[row2, 'Tm'], season) == team: 
                date_string = str(player_game_log.at[row2, 'Date'])
                date_list = date_string.split(' ')[0].split('-')
                date_of_game = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
                if date_of_game < date_end and date_of_game >= date_beg: 
                    try: 
                        gamescore = float(player_game_log.at[row2, 'GmSc'])
                        if gamescore < 0 or gamescore > 0: 
                            total_gmsc += gamescore
                    except ValueError:
                        gamescore = 0
                else: 
                    break
    return total_gmsc

def get_gmsc_injured(team, date): 
    if date.month > 9 or date.month == 9 and date.day > 14: 
        season = date.year+1
    else: 
        season = date.year 
    injured_players = get_injuries_for_team(team, date)
    # print("Injuries for team: ")
    # print(injured_players)
    total_ratio = 0
    for player in injured_players: 
        player_game_log = get_player_game_log_excel(player, team, season)
        time_on_team = {}
        on_team = False
        gmsc_on_team = 0
        for row in range(player_game_log.shape[0]): 
            date_string = str(player_game_log.at[row, 'Date'])
            date_list = date_string.split(' ')[0].split('-')
            date_of_game = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
            if date_of_game < date: 
                if abrv_to_city(player_game_log.at[row, 'Tm'], season) == team: 
                    if not on_team: 
                        on_team = True
                        time_on_team[len(time_on_team)] = {'start': date_of_game, 'end': None}
                    try: 
                        gamescore = float(player_game_log.at[row, 'GmSc'])
                        if gamescore < 0 or gamescore > 0: 
                            gmsc_on_team += gamescore
                    except ValueError:
                        gamescore = 0
                elif abrv_to_city(player_game_log.at[row, 'Tm'], season) != team and on_team: 
                    on_team = False
                    time_on_team[len(time_on_team)-1]['end'] = date_of_game
            else: 
                break
        # print("Time on team for player " + player + " during " + str(season) + " for team " + team)
        # print(time_on_team)
        total_gmsc_while_on_team = 0
        for stretch in range(len(time_on_team)): 
            start_date = time_on_team[stretch]['start']
            end_date = time_on_team[stretch]['end']
            if end_date == None: end_date = date
            total_gmsc_while_on_team += get_total_gmsc_during_date(team, start_date, end_date)
        if total_gmsc_while_on_team > 0: 
            ratio = gmsc_on_team/total_gmsc_while_on_team
        else: ratio = 0
        total_ratio += ratio
    return total_ratio

def get_mins_injured(team, date): 
    if date.month > 9 or date.month == 9 and date.day > 14: 
        season = date.year+1
    else: 
        season = date.year 
    injured_players = get_injuries_for_team(team, date)
    # print("Injuries for team: ")
    # print(injured_players)
    total_ratio = 0
    for player in injured_players: 
        player_game_log = get_player_game_log_excel(player, team, season)
        time_on_team = {}
        on_team = False
        mins_on_team = 0
        gp_on_team = 0
        for row in range(player_game_log.shape[0]): 
            date_string = str(player_game_log.at[row, 'Date'])
            date_list = date_string.split(' ')[0].split('-')
            date_of_game = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2])) 
            if date_of_game < date: 
                if abrv_to_city(player_game_log.at[row, 'Tm'], season) == team: 
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
                elif abrv_to_city(player_game_log.at[row, 'Tm'], season) != team and on_team: 
                    on_team = False
                    time_on_team[len(time_on_team)-1]['end'] = date_of_game
            else: 
                break
        # print("Time on team for player " + player + " during " + str(season) + " for team " + team)
        # print(time_on_team)
        # print(mins_on_team)
        total_mins_while_on_team = gp_on_team * 240
        if total_mins_while_on_team > 0: 
            ratio = mins_on_team/total_mins_while_on_team
        else: ratio = 0
        total_ratio += ratio
    return total_ratio

def get_current_injuries(team): 
    print(f"Now generating injuries for {team}")
    injured_players = []
    team_names = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"]
    team_abbrvs = ['ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    index = 31
    for x in range(len(team_names)): 
        if team_names[x] == team: 
            index = x
    abrv = team_abbrvs[index]
    url = f"https://www.rotowire.com/basketball/tables/injury-report.php?team={abrv}&pos=ALL"
    response = requests.get(url) 
    json = response.json()
    for x in range(len(json)): 
        if json[x]['status'] == 'Out': 
            injured_players.append(json[x]['player'])
    print("Injured players: ", injured_players)
    return injured_players

team_names = { 'pre2009': ["Atlanta", "Boston", "New Jersey", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Seattle", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'pre2013': ["Atlanta", "Boston", "New Jersey", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'pre2014': ["Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'pre2015': ["Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"], 'post2015': ["Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]}
team_abbrvs = { 'pre2009': ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'SEA', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'], 'pre2013': ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'], 'pre2014': ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'], 'pre2015': ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'], 'post2015': ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']}
years = range(2008, 2024)

def generate_player_game_logs(): 
    for year in years: 
        if year < 2009: 
            category = 'pre2009'
        elif year < 2013: 
            category = 'pre2013'
        elif year < 2014: 
            category = 'pre2014'
        elif year < 2015: 
            category = 'pre2015'
        else: category = 'post2015'
        for team_name in team_names[category]: 
            roster = pd.read_excel(f'./rosters/{year}/{team_name}/{team_name}.xlsx')
            # Construct the file path for the game log file
            for row in range(roster.shape[0]): 

                name = unidecode(roster.at[row, 'Player'])
                bbref_url = roster.at[row, 'bbref url']

                file_path = f'./rosters/{year}/{team_name}/{name}.xlsx'

                # Check if the file already exists
                if not os.path.exists(file_path) and not (name == "Ty Lawson" and team_name == "Washington"):
                    # Generate the game log dataframe
                    print("Generating game log for " + name + " in year " + str(year) + " for team " + team_name)
                    game_log = get_player_game_log(bbref_url, year)
                    time.sleep(3.5)
                    print("Generated game log for " + name + " in year " + str(year) + " for team " + team_name)
                    
                    teams_played_for = []
                    for row2 in range(game_log.shape[0]): 
                        team = game_log.at[row2, 'Tm']
                        if team not in teams_played_for: 
                            teams_played_for.append(team)

                    for team in teams_played_for: 
                        print(team)
                        index = 31
                        for abbr in range(len(team_abbrvs[category])): 
                            if team == team_abbrvs[category][abbr]: 
                                index = abbr
                                break
                        file_path = f'./rosters/{year}/{team_names[category][index]}/{name}.xlsx'
                        if not os.path.exists(file_path):
                            game_log.to_excel(file_path)

def generate_rosters(): 
    for year in years: 
        if year < 2009: 
            category = 'pre2009'
        elif year < 2013: 
            category = 'pre2013'
        elif year < 2014: 
            category = 'pre2014'
        elif year < 2015: 
            category = 'pre2015'
        else: category = 'post2015'
        for team_name in team_names[category]: 
            file_path = f"./rosters/{str(year)}/{team_name}/{team_name}.xlsx"
            team_dir = f"./rosters/{str(year)}/{team_name}"
            if not os.path.exists(team_dir):
                os.makedirs(team_dir)
            if not os.path.exists(file_path): 
                roster = get_roster(team_name, year)
                roster.to_excel(file_path)

# generate_player_game_logs()
# for team_name in team_names:
#     for year in years:
#         roster = pd.read_excel(f'./rosters/{year}/{team_name}/{team_name}.xlsx')
#         # Construct the file path for the game log file
#         for row in range(roster.shape[0]): 

#             name = unidecode(roster.at[row, 'Player'])
#             bbref_url = roster.at[row, 'bbref url']

#             file_path = f'./rosters/{year}/{team_name}/{name}.xlsx'

#             # Check if the file already exists
#             if not os.path.exists(file_path) and not (name == "Ty Lawson" and team_name == "Washington"):
#                 # Generate the game log dataframe
#                 print("Generating game log for " + name + " in year " + str(year) + " for team " + team_name)
#                 game_log = get_player_game_log(bbref_url, year)
#                 time.sleep(2)
#                 print("Generated game log for " + name + " in year " + str(year) + " for team " + team_name)
                
#                 teams_played_for = []
#                 for row2 in range(game_log.shape[0]): 
#                     team = game_log.at[row2, 'Tm']
#                     if team not in teams_played_for: 
#                         teams_played_for.append(team)

#                 for team in teams_played_for: 
#                     print(team)
#                     if year < 2015: 
#                         index = 31
#                         for abbr in range(len(team_abbrvs['pre2015'])): 
#                             if team == team_abbrvs['pre2015'][abbr]: 
#                                 index = abbr
#                                 break
#                     else: 
#                         index = 31
#                         for abbr in range(len(team_abbrvs['post2015'])): 
#                             if team == team_abbrvs['post2015'][abbr]: 
#                                 index = abbr
#                                 break
#                     file_path = f'./rosters/{year}/{team_names[index]}/{name}.xlsx'
#                     if not os.path.exists(file_path):
#                             game_log.to_excel(file_path)