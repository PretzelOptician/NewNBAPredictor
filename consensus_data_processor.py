import pickle
import datetime
import pandas as pd
from consensus_tracker import get_z_score 
import math

def get_spread_picks(game_ids, data, scores, date): 
    picks = data['picks']
    dict_list = []
    for game in game_ids: 
        dict1 = {'id': game['id'], 'home_team': game['home_team_id'], 'away_team': game['road_team_id'], 'z_total': 0.0, 'count': 0, 'home': True, 'z_total_volume': 0.0}
        dict_list.append(dict1)
    z_total_spread = 0
    for user in picks: 
        if user['season_pick_pct'] > 60 and user['season_win_pct'] > 50:
            z = get_z_score(user)
            z_total_spread += z
            for dict_ in dict_list: 
                id = str(dict_['id'])
                if(id in user['picks']): 
                    if(user['picks'][id]['team_id'] == dict_['away_team']): 
                        z_to_add = -z
                    else: 
                        z_to_add = z
                    dict_['z_total_volume'] += z
                    dict_['z_total'] += z_to_add
                    dict_['count'] += 1
    for dict_ in dict_list: 
        if dict_['z_total'] < 0: 
            dict_['z_total'] = -dict_['z_total']
            dict_['home'] = False
        try: 
            awcs = (dict_['z_total']/dict_['z_total_volume'])*math.sqrt(dict_['z_total'])
        except ZeroDivisionError: 
            awcs = 0
        total_string = dict_['home_team'] if dict_['home'] else dict_['away_team']
        print(f"For game {dict_['away_team']} at {dict_['home_team']}, the average AWCS score is {awcs} for {total_string} (total: {dict_['z_total']}, percent of Z with pick made: {100*dict_['z_total_volume']/z_total_spread}%)")
        for game in data_2023:
            if game['home_team']['abbreviation'] == dict_['home_team'] and game['visitor_team']['abbreviation'] == dict_['away_team']: 
                date_days = game['date'].split('T')[0]
                date_of_game = datetime.date(int(date_days.split('-')[0]), int(date_days.split('-')[1]), int(date_days.split('-')[2])) 
                if abs(date_of_game - date) <= datetime.timedelta(days=1): #correct game found
                    print("Game outcome was discovered.")
    return dict_list, picks

import os
directory_picks = 'spread_consensus_strings'
directory_ids = 'spread_game_ids'

pick_list = []
with open('season_data_2023', 'rb') as file: 
    data_2023 = pickle.load(file)
list_of_files = os.listdir(directory_picks)
for i, filename in enumerate(list_of_files): 
    f_picks = os.path.join(directory_picks, filename)
    try: 
        f_ids = os.path.join(directory_ids, list_of_files[i+1])
    except IndexError: 
        continue
    with open(f_picks, 'rb') as file:
        picks = pickle.load(file)
    with open(f_ids, 'rb') as file: 
        ids = pickle.load(file)
    try: 
        example_id = list(picks['picks'][0]['picks'].keys())[0]
    except IndexError: 
        continue
    correct_day = None
    for id_day in ids: 
        for game in id_day: 
            # print(game['id'])
            if game['id'] == int(example_id): 
                correct_day = id_day
                break
        if correct_day is not None: 
            break
    if correct_day is None: 
        print("Correct day of games not found, skipping this file...")
        continue
    date = datetime.date(int(filename.split('-')[0]),int(filename.split('-')[1]),int(filename.split('-')[2]))
    dict_list = get_spread_picks(correct_day, picks, data_2023, date)[0]
    for x in dict_list: 
        pick_list.append(x)
