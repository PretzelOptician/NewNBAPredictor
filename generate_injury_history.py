import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date

def get_injury_data_raw(): 
    i = 0
    url = "https://www.prosportstransactions.com/basketball/Search/SearchResults.php?Player=&Team=&BeginDate=2013-06-01&EndDate=2023-01-10&ILChkBx=yes&Submit=Search&start=0"
    response = requests.get(url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    injuryData = pd.read_html(str(table))[0]
    injuryData = injuryData.drop([0])
    injuryData = injuryData.reset_index(drop=True)
    i += 1
    total_data = pd.DataFrame()

    while (not injuryData.empty): 

        #add stuff to overall dataframe
        total_data = pd.concat([total_data, injuryData], ignore_index=True)

        url = f"https://www.prosportstransactions.com/basketball/Search/SearchResults.php?Player=&Team=&BeginDate=2013-06-01&EndDate=2023-01-10&ILChkBx=yes&Submit=Search&start={str(i*25)}"
        response = requests.get(url) 
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        injuryData = pd.read_html(str(table))[0]
        injuryData = injuryData.drop([0])
        injuryData = injuryData.reset_index(drop=True)
        # injuryData.rename(columns={'0': 'Date', '1': 'Team', '2': 'Acquired', '3': 'Relinquished', '4': 'Notes'})
        # print(injuryData)
        i += 1

    total_data.columns = ['Date', 'Team', 'Acquired', 'Relinquished', 'Notes']

    print(total_data)
    return total_data
    # total_data.to_excel('raw_injury_data.xlsx')

def process_injury_data(injury_data): 
    dict_list = {}
    injury_data['Acquired'] = injury_data['Acquired'].fillna("")
    injury_data['Relinquished'] = injury_data['Relinquished'].fillna("")
    for row in range(injury_data.shape[0]): 
        if injury_data.at[row, 'Acquired'] is not "": ##player comes off IR
            player_name = ' '.join(injury_data.at[row, 'Acquired'].split(' ')[1:])
            if player_name in dict_list: 
                dict_list[player_name][len(dict_list[player_name])-1]['Return Date'] = injury_data.at[row, 'Date']
            # print(player_name)
        elif injury_data.at[row, 'Relinquished'] is not "": ##player injured
            player_name = ' '.join(injury_data.at[row, 'Relinquished'].split(' ')[1:])
            # print(player_name)
            if player_name not in dict_list:
                dict_list[player_name] = {}
                dict_list[player_name][0] = {'Injury Date': injury_data.at[row, 'Date'], 'Return Date': None, 'Notes': injury_data.at[row, 'Notes']}
            elif dict_list[player_name][len(dict_list[player_name])-1]['Return Date'] is not None: 
                dict_list[player_name][len(dict_list[player_name])] = {'Injury Date': injury_data.at[row, 'Date'], 'Return Date': None, 'Notes': injury_data.at[row, 'Notes']}
            else: 
                dict_list[player_name][len(dict_list[player_name])-1]['Notes'] = dict_list[player_name][len(dict_list[player_name])-1]['Notes'] + "; " + injury_data.at[row, 'Notes']
    return dict_list

#date must be date object
#only players that played a game earlier in the season are included here
def get_injuries_by_date(inj_dict, date): 
    # uses the date supplied to figure out the season year
    if date.month > 9 or date.month == 9 and date.day > 14: 
        season = date.year+1
    else: 
        season = date.year
    players_injured = []
    for player in inj_dict: 
        player_injured = False
        for injury in inj_dict[player]: 
            injury_date_list = inj_dict[player][injury]['Injury Date'].split('-')
            injury_date = datetime.date(int(injury_date_list[0]), int(injury_date_list[1]), int(injury_date_list[2]))
            season_start = datetime.date(season-1, 9, 14)
            injured_this_season = injury_date > season_start
            if inj_dict[player][injury]['Return Date'] is not None: 
                return_date_list = inj_dict[player][injury]['Return Date'].split('-')
            # if a player was injured this season before the current date and has not yet returned from IR, then they are currently injured
            if injury_date <= date and injured_this_season and (inj_dict[player][injury]['Return Date'] is None or datetime.date(int(return_date_list[0]), int(return_date_list[1]), int(return_date_list[2])) > date): 
                player_injured = True
        if player_injured: 
            players_injured.append(player)
    return players_injured

# df = get_injury_data_raw()
# df.to_excel('raw_injury_data.xlsx')

df = pd.read_excel('./raw_injury_data.xlsx')
injury_dict = process_injury_data(df)
print(get_injuries_by_date(injury_dict, date.today()))