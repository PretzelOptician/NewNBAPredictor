import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

pd.set_option('display.max_rows', None)

def get_2k_ratings(year): 
    api_url = f"https://hoopshype.com/nba2k/teams/{str(year-1)}-{str(year)}/"
    response = requests.get(api_url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    df = pd.read_html(str(table))[0]

    df = df.reset_index(drop=True)

    return df

years = range(2008, 2024)

for year in years:
    # Construct the file path for the game log file
    file_path = f'../historic_data/ratings/{year}.xlsx'

    # Check if the file already exists
    if not os.path.exists(file_path):
        # Generate the game log dataframe
        game_log = get_2k_ratings(year)

        # Create the directory for the ratings if it doesn't exist
        rsw_dir = f'../ratings'
        if not os.path.exists(rsw_dir):
            os.makedirs(rsw_dir)

        # Save the game log dataframe to a .xlsx file
        game_log.to_excel(file_path)