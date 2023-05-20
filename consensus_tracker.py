import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import math
import datetime
import urllib3

PCT_THRESHOLD = 50

def days_since_jan_2(): 
    ##chatGPT generated
    # Get current date
    current_date = datetime.datetime.now()
    # Set target date
    target_date = datetime.datetime(2023, 1, 2)
    # Calculate difference between dates
    difference = current_date - target_date
    # Print number of days
    return difference.days

def get_z_score(user): 
    sample_percent = user['season_win_pct']
    sample_size = user['season_wins'] + user['season_losses']
    z = (sample_percent/100 - PCT_THRESHOLD/100)/math.sqrt(((PCT_THRESHOLD/100) * (1-(PCT_THRESHOLD/100)))/sample_size)
    return z

def get_total_picks(game_ids, days):
    # print(days)
    total_picks_url = f"https://api.nflpickwatch.com/v1/picks/nba/2022/{str(77+days)}/ou/combined/true/25/0"
    response = requests.get(total_picks_url) 
    data = response.content
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    picks = data['picks']
    dict_list = []
    print("Generating consensus scores for total bets: ")
    for game in game_ids: 
        dict1 = {'id': game['id'], 'home_team': game['home_team_id'], 'away_team': game['road_team_id'], 'z_total': 0.0, 'count': 0, 'over': True, 'z_total_volume': 0.0}
        dict_list.append(dict1)
    z_total_ou = 0
    for user in picks: 
        if user['season_pick_pct'] > 60 and user['season_win_pct'] > 50: 
            # print(user['username'])
            z = get_z_score(user)
            # print(z)
            # for bruh in user['picks']: 
            #     print(bruh)
            z_total_ou += z
            for dict_ in dict_list: 
                id = str(dict_['id'])
                if(id in user['picks']): 
                    if(user['picks'][id]['ou_type'] == 'under'): 
                        z_to_add = -z
                    else: 
                        z_to_add = z
                    dict_['z_total_volume'] += z
                    dict_['z_total'] += z_to_add
                    dict_['count'] += 1
    for dict_ in dict_list: 
        if dict_['z_total'] < 0: 
            dict_['z_total'] = -dict_['z_total']
            dict_['over'] = False
        total_string = "over" if dict_['over'] else "under"
        awcs = (dict_['z_total']/dict_['z_total_volume'])*math.sqrt(dict_['z_total'])
        print(f"For game {dict_['away_team']} at {dict_['home_team']}, the average AWCS score is {awcs} for the {total_string} (total: {dict_['z_total']}, percent of Z with pick made: {100*dict_['z_total_volume']/z_total_ou}%)")
    return dict_list, picks

def get_spread_picks(game_ids, days): 
    print("\nGenerating consensus scores for spread bets: ")
    spread_picks_url = f"https://api.nflpickwatch.com/v1/picks/nba/2022/{str(77+days)}/ats/combined/true/25/0"
    response = requests.get(spread_picks_url) 
    data = response.content
    my_json = data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    picks = data['picks']
    dict_list = []
    for game in game_ids: 
        ## HOME IS POSITIVE Z
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
                    # print(user['picks'])
                    if(user['picks'][id]['team_id'] == dict_['away_team']): 
                        z_to_add = -z
                    else: 
                        z_to_add = z
                    dict_['z_total_volume'] += z
                    dict_['z_total'] += z_to_add
                    dict_['count'] += 1
    for dict_ in dict_list: 
        # print("raw z score: " + str(dict_['z_total']/dict_['count']))
        if dict_['z_total'] < 0: 
            dict_['z_total'] = -dict_['z_total']
            dict_['home'] = False
            # print("z val is negative, so dict_['home'] is " + str(dict_['home']))
        awcs = (dict_['z_total']/dict_['z_total_volume'])*math.sqrt(dict_['z_total'])
        total_string = dict_['home_team'] if dict_['home'] else dict_['away_team']
        print(f"For game {dict_['away_team']} at {dict_['home_team']}, the average AWCS score is {awcs} for {total_string} (total: {dict_['z_total']}, percent of Z with pick made: {100*dict_['z_total_volume']/z_total_spread}%)")
    return dict_list, picks

def get_game_ids(days): 
    game_id_url = f"https://api.nflpickwatch.com/v1/general/games/2022/{str(77+days)}/nba/REGULAR"
    game_ids = json.loads(requests.get(game_id_url).content.decode('utf8').replace("'", '"'))
    return game_ids

def run_consensus_model(days): 
    game_ids = get_game_ids(days)
    get_total_picks(game_ids, days)
    get_spread_picks(game_ids, days)

def test(): 
    url = 'https://api.nflpickwatch.com/v1/picks/nba/2022/46/ats/combined/true/25/0'

def test2(days): 
    print(f"https://api.nflpickwatch.com/v1/picks/nba/2022/{str(77+days)}/ats/combined/true/25/0")
    try: 
        response = requests.get(f"https://api.nflpickwatch.com/v1/picks/nba/2022/{str(77+days)}/ats/combined/true/25/0")
        data = response.content
        my_json = data.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        print(data)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print(f"Error: {e}. Skipping this request.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}.")
        return
    

days = days_since_jan_2()
# days = 60
run_consensus_model(days)
# test2(days_since_jan_2())
# for i in range(-77, days_since_jan_2()): 
#     test2(i)
