from consensus_tracker import *
import pickle

import os
directory_picks = 'spread_consensus_strings'
directory_ids = 'spread_game_ids'

with open('spread_game_ids/2022-10-21', 'rb') as file: 
    ids = pickle.load(file)

for i, filename in enumerate(os.listdir(directory_picks)): 
    f_picks = os.path.join(directory_picks, filename)
    # print(f_picks)
    # f_ids = os.path.join(directory_ids, filename)
    # print(f_ids)
    with open(f_picks, 'rb') as file:
        picks = pickle.load(file)
    # with open(f_ids, 'rb') as file: 
    #     ids = pickle.load(file)
    #     print(ids)
    get_spread_picks(ids[i+1], picks)
    # quit()