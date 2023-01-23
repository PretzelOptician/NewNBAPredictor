import requests
import datetime
from datetime import date

def get_city(team): 
    if team == 'Golden State Warriors': return 'GoldenState'
    elif team == 'Los Angeles Clippers': return 'LAClippers'
    elif team == 'Los Angeles Lakers': return 'LALakers'
    elif team == 'New Orleans Pelicans': return 'NewOrleans'
    elif team == 'New York Knicks': return 'NewYork'
    elif team == 'Oklahoma City Thunder': return 'OklahomaCity'
    elif team == 'San Antonio Spurs': return 'SanAntonio'
    else: return team.split(' ')[0]

def predict_correct_o_u(home_team, away_team, picked_over, ou):
    # get scores from prev night
    url = "https://odds.p.rapidapi.com/v4/sports/basketball_nba/scores"

    querystring = {"daysFrom":"1"}

    headers = {
        "X-RapidAPI-Key": "12777cbd21mshe5e3f8c4932bb27p163af3jsndff8ebab5ee4",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    games = response.json()
    for game in range(len(games)): 
        if get_city(games[game]['home_team']) == home_team and get_city(games[game]['away_team']) and games[game]['completed']: 
            total = int(games[game]['scores'][0]['score']) + int(games[game]['scores'][1]['score'])
    # check if prediction was correct
    if total > ou: #over hit
        if picked_over: 
            return "W"
        else: 
            return "L"
    elif total < ou: 
        if not picked_over: 
            return "W"
        else: 
            return "L"
    else: 
        return "T"

def predict_correct_spread(home_team, away_team, picked_home, home_spread): 
    # get scores from prev night
    url = "https://odds.p.rapidapi.com/v4/sports/basketball_nba/scores"

    querystring = {"daysFrom":"1"}

    headers = {
        "X-RapidAPI-Key": "12777cbd21mshe5e3f8c4932bb27p163af3jsndff8ebab5ee4",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    games = response.json()
    for game in range(len(games)): 
        if get_city(games[game]['home_team']) == home_team and get_city(games[game]['away_team']) and games[game]['completed']: 
            actual_spread_home = int(games[game]['scores'][1]['score']) - int(games[game]['scores'][0]['score'])
    # check if prediction was correct
    if actual_spread_home < home_spread: #home covered
        if picked_home: 
            return "W"
        else: 
            return "L"
    elif actual_spread_home > home_spread: 
        if not picked_home: 
            return "W"
        else: 
            return "L"
    else: 
        return "T"

def read_and_update_file(pick_string): 
    with open('record.txt', 'r') as file: 
        file_list = file.readlines()
        old_record = file_list[0].split('-')
        wins = int(old_record[0])
        loss = int(old_record[1])
        pushes = int(old_record[2])
        prev_predict = file_list[1].split(' ')
        teams = prev_predict[0].split('@')
        prediction = prev_predict[1:]
        home_team = teams[1]
        away_team = teams[0]
        if len(prediction) == 2: 
            team_picked = prediction[0]
            spread = prediction[1]
            if team_picked == home_team: 
                picked_home = True
                result = predict_correct_spread(home_team, away_team, picked_home, float(spread))
            else: #picked away 
                picked_home = False
                home_spread = -1*float(spread)
                result = predict_correct_spread(home_team, away_team, picked_home, home_spread)
            if result == "W": 
                wins += 1
            elif result == "L": 
                loss += 1
            elif result == "T": 
                pushes += 1
            new_record = f"{str(wins)}-{str(loss)}-{str(pushes)}"
            print(new_record)
        else: 
            prediction = prediction[0]
            picked_over = prediction[0] == 'o'
            print(picked_over)
            result = predict_correct_o_u(home_team, away_team, picked_over, float(prediction[1:]))
            if result == "W": 
                wins += 1
            elif result == "L": 
                loss += 1
            elif result == "T": 
                pushes += 1
            new_record = f"{str(wins)}-{str(loss)}-{str(pushes)}"
            print(new_record)
    with open('record.txt', 'w') as file: 
        file.write(new_record + "\n" + pick_string)

def generate_tweet(pick_string, pct): 
    pick_string = pick_string.replace(' ', ': ').replace('@', ' @ ')
    pick_string = pick_string + " with a probability of " + str(pct) + "%."
    today = date.today()
    line1 = f"NBA Pick of the Day ({today.month}/{today.day}/{today.year}) for SportsNinja Stat Model v1.2: "
    line2 = pick_string
    with open('record.txt', 'r') as file: 
        file_list = file.readlines()
        record = file_list[0].split('-')
        wins = int(record[0])
        loss = int(record[1])
        pushes = int(record[2])
        if pushes > 0: 
            line3 = f"Current Season Record for v1.1/1.2: {str(wins)}-{str(loss)}-{str(pushes)}"
        else: 
            line3 = f"Current Season Record for v1.1/1.2: {str(wins)}-{str(loss)}"
    tweet_text = line1 + "\n\n" + line2 + "\n\n" + line3
    return tweet_text

def run_tweet_gen(pick_string, pct): 
    read_and_update_file(pick_string)
    print(generate_tweet(pick_string, pct))