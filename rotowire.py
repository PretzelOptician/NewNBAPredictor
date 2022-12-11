import requests
import json
import pandas as pd

api_url = "https://www.rotowire.com/basketball/tables/injury-report.php?team=ALL&pos=ALL"
response = requests.get(api_url) 
jsonString = response.json()
# a_json = json.loads(jsonString)
dataframe = pd.DataFrame(jsonString)
dataframe = dataframe.drop(['ID', 'firstname', 'lastname'], axis=1)
dataframe.to_excel("../NBA-Spreadsheets/injuryStats.xlsx", index=False)