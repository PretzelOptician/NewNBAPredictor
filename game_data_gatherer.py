import requests
import pickle

overall_data = []
for i in range(14): 
    url = f"https://free-nba.p.rapidapi.com/games?seasons[]=2022&per_page=100&page={str(i+1)}"
    headers = {
        "X-RapidAPI-Key": "12777cbd21mshe5e3f8c4932bb27p163af3jsndff8ebab5ee4",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()["data"]
    for game in data: 
        overall_data.append(game)

with open("season_data_2023", 'wb') as file: 
    pickle.dump(overall_data, file=file)
