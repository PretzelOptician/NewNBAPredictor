import datetime
import pandas as pd
from consensus_tracker import *
import pickle

def days_since_start(date): 
    target_date = datetime.date(2022, 10, 18)
    difference = date - target_date
    return difference.days

picks_dict = {'date': [], 'dict_string': []}
with open("consensus_data_spread.txt") as file: 
    f = file.readlines()

cur_date = None
file_string = ''
for line in f: 
    line = line.rstrip('\n')
    if len(line.split('-')) == 3 and line.split('-')[0].isnumeric() and line.split('-')[1].isnumeric() and line.split('-')[2].isnumeric():
        if cur_date is not None:
            with open(f'./spread_consensus_strings/{cur_date.isoformat()}', 'wb') as f:
                pickle.dump(json.loads(file_string), file=f)
            file_string = ''
            picks_dict['date'].append(cur_date)
        cur_date = datetime.date(int(line.split('-')[0]),int(line.split('-')[1]),int(line.split('-')[2])) if int(line.split('-')[0]) > 2000 else datetime.date(int(line.split('-')[2])+2000, int(line.split('-')[0]), int(line.split('-')[1]))
    else: 
        file_string += line.strip() 
file_string = ''
games_dict = []
for date in picks_dict['date']: 
    days_value = days_since_start(date)
    ids = get_game_ids(days_value)
    games_dict.append(ids)
    with open(f'./spread_game_ids/{date.isoformat()}', 'wb') as f:
        pickle.dump(games_dict, file=f)
