import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_rsw_odds(year): 
    api_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_preseason_odds.html#NBA_preseason_odds"
    response = requests.get(api_url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    leagueData = pd.read_html(str(table))[0]

    ## ChatGPT code: filtering data set
    # Convert the 'W-L O/U' column to a numeric type and store in a new column 'O-U-num'
    leagueData['O-U-num'] = pd.to_numeric(leagueData['W-L O/U'], errors='coerce')

    # Filter the rows where 'O-U-num' is not null
    df = leagueData[leagueData['O-U-num'].notnull()]

    df = df.reset_index(drop=True)
    
    cols = ['Team', 'Odds', 'blank', 'W-L O/U', 'Result', 'O-U-num']
    df.columns = cols

    return df

years = range(2008, 2024)

for year in years:
    # Construct the file path for the game log file
    file_path = f'./rswOdds/{year}.xlsx'

    # Check if the file already exists
    if not os.path.exists(file_path):
        # Generate the game log dataframe
        game_log = get_rsw_odds(year)

        # Create the directory for the rswOdds if it doesn't exist
        rsw_dir = f'./rswOdds'
        if not os.path.exists(rsw_dir):
            os.makedirs(rsw_dir)

        # Save the game log dataframe to a .xlsx file
        game_log.to_excel(file_path)