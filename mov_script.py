import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_rsw_odds(year): 
    api_url = f"https://www.basketball-reference.com/leagues/NBA_{str(year)}_ratings.html"
    response = requests.get(api_url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    leagueData = pd.read_html(str(table))[0]
    leagueData.columns = leagueData.columns.droplevel(level=0)

    ## ChatGPT code: filtering data set
    # Convert the 'W' column to a numeric type and store in a new column 'W-num'
    leagueData['W-num'] = pd.to_numeric(leagueData['W'], errors='coerce')

    # Filter the rows where 'W-num' is not null
    df = leagueData[leagueData['W-num'].notnull()]

    df = df.reset_index(drop=True)

    return df

years = range(2007, 2024)

for year in years:
    # Construct the file path for the game log file
    file_path = f'./movRatings/{year}.xlsx'

    # Check if the file already exists
    if not os.path.exists(file_path):
        # Generate the game log dataframe
        game_log = get_rsw_odds(year)

        # Create the directory for the rswOdds if it doesn't exist
        rsw_dir = f'./movRatings'
        if not os.path.exists(rsw_dir):
            os.makedirs(rsw_dir)

        # Save the game log dataframe to a .xlsx file
        game_log.to_excel(file_path)