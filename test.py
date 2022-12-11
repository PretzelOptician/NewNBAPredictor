import pandas as pd
from bs4 import BeautifulSoup
import requests

api_url = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_" + str(2014) + ".html&div=div_advanced-team"
response = requests.get(api_url) 
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table')
leagueData = pd.read_html(str(table))[0]
leagueData = leagueData.drop(['Unnamed: 0_level_0'], axis=1)
for row2 in range(leagueData.shape[0]): 
    if leagueData.iat[row2, 0].startswith("San Antonio Spurs") or leagueData.iat[row2, 0].startswith("San Antonio Spurs"): 
        print(leagueData.iat[row2, 21])