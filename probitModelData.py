import pandas as pd
from bs4 import BeautifulSoup
import requests

ROW_START = 100
ROW_PLAYOFFS = 0

def get_avg_followers(team): 
    if team == 'LALakers' or team == 'LA Lakers': return 52321433
    elif team == 'Cleveland': return 23853389
    elif team == 'Boston': return 19952367
    elif team == 'Milwaukee': return 10288717
    elif team == 'Chicago': return 30435628
    elif team == 'Portland': return 7117111
    elif team == 'Toronto': return 8798856
    elif team == 'Philadelphia': return 7925637
    elif team == 'Atlanta': return 5635700
    elif team == 'Orlando': return 6161629
    elif team == 'Brooklyn': return 9902212
    elif team == 'Washington': return 8209114
    elif team == 'Miami': return 25825318
    elif team == 'NewYork': return 11755482
    elif team == 'Indiana': return 6768683
    elif team == 'Detroit': return 4443090
    elif team == 'OklahomaCity' or team == 'Oklahoma City': return 14379492
    elif team == 'Sacramento': return 10624663
    elif team == 'Minnesota': return 5790088
    elif team == 'Phoenix': return 6479573
    elif team == 'SanAntonio' or team == 'San Antonio': return 14554210
    elif team == 'Memphis': return 5430199
    elif team == 'Denver': return 5618580
    elif team == 'Houston': return 25544036
    elif team == 'Utah': return 8164010
    elif team == 'NewOrleans' or team == 'New Orleans': return 6016902
    elif team == 'GoldenState' or team == 'Golden State': return 48149619
    elif team == 'LAClippers' or team == 'LA Clippers': return 10709842
    elif team == 'Charlotte': return 5802049
    elif team == 'Dallas': return 10535695

# convert team name to the name used in the league stats sheet. note that it only returns the first word as this is the name used to parse the spreadsheet
def convert_team_name(team): 
    if team == 'LALakers' or team == 'LA Lakers': return 'Los Angeles Lakers'
    elif team == 'Cleveland': return 'Cleveland Cavaliers'
    elif team == 'Boston': return 'Boston Celtics'
    elif team == 'Milwaukee': return 'Milwaukee Bucks'
    elif team == 'Chicago': return 'Chicago Bulls'
    elif team == 'Portland': return 'Portland Trail Blazers'
    elif team == 'Toronto': return 'Toronto Raptors'
    elif team == 'Philadelphia': return 'Philadelphia 76ers'
    elif team == 'Atlanta': return 'Atlanta Hawks'
    elif team == 'Orlando': return 'Orlando Magic'
    elif team == 'Brooklyn': return 'Brooklyn Nets'
    elif team == 'Washington': return 'Washington Wizards'
    elif team == 'Miami': return 'Miami Heat'
    elif team == 'NewYork': return 'New York Knicks'
    elif team == 'Indiana': return 'Indiana Pacers'
    elif team == 'Detroit': return 'Detroit Pistons'
    elif team == 'OklahomaCity' or team == 'Oklahoma City': return 'Oklahoma City Thunder'
    elif team == 'Sacramento': return 'Sacramento Kings'
    elif team == 'Minnesota': return 'Minnesota Timberwolves'
    elif team == 'Phoenix': return 'Phoenix Suns'
    elif team == 'SanAntonio' or team == 'San Antonio': return 'San Antonio Spurs'
    elif team == 'Memphis': return 'Memphis Grizzlies'
    elif team == 'Denver': return 'Denver Nuggets'
    elif team == 'Houston': return 'Houston Rockets'
    elif team == 'Utah': return 'Utah Jazz'
    elif team == 'NewOrleans' or team == 'New Orleans': return 'New Orleans Pelicans'
    elif team == 'GoldenState' or team == 'Golden State': return 'Golden State Warriors'
    elif team == 'LAClippers' or team == 'LA Clippers': return 'Los Angeles Clippers'
    elif team == 'Charlotte': return 'Charlotte Hornets'
    elif team == 'Dallas': return 'Dallas Mavericks'

def get_abbrv(team, year): 
    if team == 'LALakers' or team == 'LA Lakers': return 'LAL'
    elif team == 'Cleveland': return 'CLE'
    elif team == 'Boston': return 'BOS'
    elif team == 'Milwaukee': return 'MIL'
    elif team == 'Chicago': return 'CHI'
    elif team == 'Portland': return 'POR'
    elif team == 'Toronto': return 'TOR'
    elif team == 'Philadelphia': return 'PHI'
    elif team == 'Atlanta': return 'ATL'
    elif team == 'Orlando': return 'ORL'
    elif team == 'Brooklyn': return 'BRK'
    elif team == 'Washington': return 'WAS'
    elif team == 'Miami': return 'MIA'
    elif team == 'NewYork' or team == 'New York': return 'NYK'
    elif team == 'Indiana': return 'IND'
    elif team == 'Detroit': return 'DET'
    elif team == 'OklahomaCity' or team == 'Oklahoma City': return 'OKC'
    elif team == 'Sacramento': return 'SAC'
    elif team == 'Minnesota': return 'MIN'
    elif team == 'Phoenix': return 'PHO'
    elif team == 'SanAntonio' or team == 'San Antonio': return 'SAS'
    elif team == 'Memphis': return 'MEM'
    elif team == 'Denver': return 'DEN'
    elif team == 'Houston': return 'HOU'
    elif team == 'Utah': return 'UTA'
    elif team == 'NewOrleans' or team == 'New Orleans': return 'NOP'
    elif team == 'GoldenState' or team == 'Golden State': return 'GSW'
    elif team == 'LAClippers' or team == 'LA Clippers': return 'LAC'
    elif team == 'Charlotte': 
        if year < 2015: return 'CHA'
        else: return 'CHO'
    elif team == 'Dallas': return 'DAL'

def get_game_log(team, year): 
    team_str = get_abbrv(team, year)
    year_str = str(year)

    api_url = f"https://www.basketball-reference.com/teams/{team_str}/{year_str}/gamelog/?sr&amp;utm_source=direct&amp;utm_medium=Share&amp;utm_campaign=ShareTool#tgl_basic"
    response = requests.get(api_url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    leagueData = pd.read_html(str(table))[0]
    leagueData.columns = leagueData.columns.droplevel(level=0)

    ## ChatGPT code: filtering data set
    # Convert the 'G' column to a numeric type and store in a new column 'G_num'
    leagueData['G_num'] = pd.to_numeric(leagueData['G'], errors='coerce')

    # Filter the rows where 'G_num' is not null
    df = leagueData[leagueData['G_num'].notnull()]

    df = df.reset_index(drop=True)
    return df

def get_game_log_excel(team, year): 
    filepath = f'./gameLogs/{year}/{team}.xlsx'
    df = pd.read_excel(filepath)
    return df

pd.set_option('display.max_rows', None)
total_data = pd.DataFrame({'year': [], 'hitOver': [], 'total': [], 'avg_popularity': [], 'totalppg': [], 'size_of_spread': [], 'home_team': [], 'away_team': [], 'pct_overs_hit': [], 'pace': [], 'ortg': [], 'drtg': [], 'drb': [], 'threePAR': [], 'ts': [], 'ftr': [], 'd_tov': [], 'o_tov': [], 'ftperfga': []})

team_names = [ "Atlanta", "Boston", "Brooklyn", "Charlotte", "Chicago", "Cleveland", "Dallas", "Denver", "Detroit", "Golden State", "Houston", "Indiana", "LA Clippers", "LA Lakers", "Memphis", "Miami", "Milwaukee", "Minnesota", "New Orleans", "New York", "Oklahoma City", "Orlando", "Philadelphia", "Phoenix", "Portland", "Sacramento", "San Antonio", "Toronto", "Utah", "Washington"]

team_name_mapping = {
    "LALakers": "LA Lakers",
    "GoldenState": "Golden State",
    "LAClippers": "LA Clippers", 
    "NewOrleans": "New Orleans", 
    "SanAntonio": "San Antonio", 
    "OklahomaCity": "Oklahoma City", 
    "NewYork": "New York"
}

# Initialize an empty dictionary to store the dataframes
game_logs = {}

# Iterate over the list of teams and the range of years
for team in team_names:
    for year in range(2014, 2023):
        # Use the get_game_log function to retrieve the dataframe for the current team and year
        df = get_game_log_excel(team, year)
        # Add the dataframe to the dictionary with the key (team, year)
        game_logs[(team, year)] = df
        print("Generated game log for " + team + " in " + str(year) + "...")

for yearOffset in range(9):
    year = 2014+yearOffset

    api_url = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_" + str(year-1) + ".html&div=div_advanced-team"
    response = requests.get(api_url) 
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    leagueData = pd.read_html(str(table))[0]
    leagueData = leagueData.drop(['Unnamed: 0_level_0'], axis=1)

    data = pd.read_excel('../NBA-Spreadsheets/' + str(year) + '/oddsStats.xlsx')
    new_data = pd.DataFrame({'year': [], 'hitOver': [], 'total': [], 'avg_popularity': [], 'totalppg': [], 'size_of_spread': [], 'home_team': [], 'away_team': [], 'pct_overs_hit': [], 'pace': [], 'ortg': [], 'drtg': [], 'drb': [], 'threePAR': [], 'ts': [], 'ftr': [], 'd_tov': [], 'o_tov': [], 'ftperfga': []})
    for row in range(data.shape[0]): 
        if row%2==1: 
            team1 = data.at[row, 'Team']
            team2 = data.at[row-1, 'Team']
            print('for: ' + team1 + ' vs ' + team2)
            if data.at[row, 'Close']!='pk' and data.at[row, 'Close']>=100:
                #is the total
                total = data.at[row, 'Close']
                if data.at[row-1, 'Close'] != 'pk': 
                    size_of_spread = data.at[row-1, 'Close']
                else: 
                    size_of_spread = 0
            else: 
                total = data.at[row-1, 'Close']
                if data.at[row, 'Close'] != 'pk': 
                    size_of_spread = data.at[row, 'Close']
                else: 
                    size_of_spread = 0
            final_score = data.at[row, 'Final'] + data.at[row-1, 'Final']
            hitOver = final_score > total
            push = final_score == total
            # homeppg = 0
            # gamesPlayed = 0
            # for row2 in range(row-1): 
            #     if data.at[row2, 'Team'] == team1: 
            #         homeppg+= data.at[row2, 'Final']
            #         gamesPlayed += 1
            # homeppg /= (gamesPlayed if gamesPlayed>0 else 1)
            # awayppg = 0
            # gamesPlayed = 0
            # for row2 in range(row-1): 
            #     if data.at[row2, 'Team'] == team2: 
            #         awayppg+= data.at[row2, 'Final']
            #         gamesPlayed += 1
            # awayppg /= (gamesPlayed if gamesPlayed>0 else 1)
            # totalppg = homeppg + awayppg
            avg_followers = (get_avg_followers(team2) + get_avg_followers(team1))/2
            
            # advanced stats

            game_log_1 = game_logs[(team_name_mapping.get(team1, team1), year)]
            game_log_2 = game_logs[(team_name_mapping.get(team2, team2), year)]

            o_tov1 = 0
            o_tov2 = 0
            d_tov1 = 0
            d_tov2 = 0
            ftr1 = 0
            ftr2 = 0
            ts1 = 0
            ts2 = 0
            threePAR1 = 0
            threePAR2 = 0
            drb1 = 0
            drb2 = 0
            ortg1 = 0
            ortg2 = 0
            drtg1 = 0
            drtg2 = 0
            pace1 = 0
            pace2 = 0
            ftperfga1 = 0
            ftperfga2 = 0
            ppg1 = 0
            ppg2 = 0

            game_log_1 = game_logs[(team_name_mapping.get(team1, team1), year)]
            game_log_2 = game_logs[(team_name_mapping.get(team2, team2), year)]
            games_played_team_one = 0
            games_played_team_two = 0
            for row2 in range(row-1): 
                if data.at[row2, 'Team'] == team1: 
                    games_played_team_one += 1
                elif data.at[row2, 'Team'] == team2: 
                    games_played_team_two += 1
            if not (((games_played_team_one > 81 or games_played_team_two > 81)) or (year == 2020 and (games_played_team_one > 63 or games_played_team_two > 63)) or (year == 2021 and (games_played_team_one > 71 or games_played_team_two > 71))): 
                for game_number in range(games_played_team_one): 
                    pace1 += game_log_1.at[game_number, 'Pace']
                    ortg1 += game_log_1.at[game_number, 'ORtg']
                    drtg1 += game_log_1.at[game_number, 'DRtg']
                    drb1 += game_log_1.at[game_number, 'DRB%']
                    threePAR1 += game_log_1.at[game_number, '3PAr']
                    ts1 += game_log_1.at[game_number, 'TS%']
                    ftr1 += game_log_1.at[game_number, 'FTr']
                    d_tov1 += game_log_1.at[game_number, 'TOV%_1']
                    o_tov1 += game_log_1.at[game_number, 'TOV%_2']
                    ftperfga1 += (game_log_1.at[game_number, 'FT/FGA_1'] + game_log_1.at[game_number, 'FT/FGA_2'])/2
                    ppg1 += game_log_1.at[game_number, 'Tm']

                if games_played_team_one > 0: 
                    pace1 /= games_played_team_one
                    ortg1 /= games_played_team_one
                    drtg1 /= games_played_team_one
                    drb1 /= games_played_team_one
                    threePAR1 /= games_played_team_one
                    ts1 /= games_played_team_one
                    ftr1 /= games_played_team_one
                    d_tov1 /= games_played_team_one
                    o_tov1 /= games_played_team_one
                    ftperfga1 /= games_played_team_one
                    ppg1 /= games_played_team_one

                for game_number in range(games_played_team_two): 
                    pace2 += game_log_2.at[game_number, 'Pace']
                    ortg2 += game_log_2.at[game_number, 'ORtg']
                    drtg2 += game_log_2.at[game_number, 'DRtg']
                    drb2 += game_log_2.at[game_number, 'DRB%']
                    threePAR2 += game_log_2.at[game_number, '3PAr']
                    ts2 += game_log_2.at[game_number, 'TS%']
                    ftr2 += game_log_2.at[game_number, 'FTr']
                    d_tov2 += game_log_2.at[game_number, 'TOV%_1']
                    o_tov2 += game_log_2.at[game_number, 'TOV%_2']
                    ftperfga2 += (game_log_2.at[game_number, 'FT/FGA_1'] + game_log_1.at[game_number, 'FT/FGA_2'])/2
                    ppg2 += game_log_2.at[game_number, 'Tm']
                
                if games_played_team_two > 0: 
                    ftperfga2 /= games_played_team_two
                    o_tov2 /= games_played_team_two
                    d_tov2 /= games_played_team_two
                    ftr2 /= games_played_team_two
                    ts2 /= games_played_team_two
                    threePAR2 /= games_played_team_two
                    drb2 /= games_played_team_two
                    drtg2 /= games_played_team_two
                    ortg2 /= games_played_team_two
                    pace2 /= games_played_team_two
                    ppg2 /= games_played_team_two

                pace = (pace1 + pace2)/2
                ortg = (ortg1 + ortg2)/2
                drtg = (drtg1 + drtg2)/2
                drb = (drb1 + drb2)/2
                threePAR = (threePAR1 + threePAR2)/2
                ts = (ts1 + ts2)/2
                ftr = (ftr1 + ftr2)/2
                d_tov = (d_tov1 + d_tov2)/2
                o_tov = (o_tov1 + o_tov2)/2
                ftperfga = (ftperfga1 + ftperfga2)/2
                totalppg = (ppg1 + ppg2)/2

                # pace /= (games_played_team_one + games_played_team_two)
                # ortg /= (games_played_team_one + games_played_team_two)
                # drtg /= (games_played_team_one + games_played_team_two)
                # drb /= (games_played_team_one + games_played_team_two)
                # threePAR /= (games_played_team_one + games_played_team_two)
                # ts /= (games_played_team_one + games_played_team_two)
                # ftr /= (games_played_team_one + games_played_team_two)
                # d_tov /= (games_played_team_one + games_played_team_two)
                # o_tov /= (games_played_team_one + games_played_team_two)
                # ftperfga /= (games_played_team_one + games_played_team_two)

                if not push: 
                    new_data.loc[len(new_data.index)] = [year, (1 if hitOver else 0), total, avg_followers, totalppg, size_of_spread, team1, team2, None, pace, ortg, drtg, drb, threePAR, ts, ftr, d_tov, o_tov, ftperfga]

                print("Data for " + team1 + " vs " + team2 + " in " + str(year))
    print("gathering over percentage data for year " + str(year))
    for row in range(new_data.shape[0]): 
        if row > ROW_START: 
            totalGames = 0
            oversHit = 0
            for row2 in range(row-1): 
                if (new_data.at[row2, 'home_team'] == new_data.at[row, 'home_team'] or new_data.at[row2, 'away_team'] == new_data.at[row, 'home_team']): 
                    totalGames += 1
                    oversHit += new_data.at[row2, 'hitOver']
            for row2 in range(row-1): 
                if (new_data.at[row2, 'home_team'] == new_data.at[row, 'away_team'] or new_data.at[row2, 'away_team'] == new_data.at[row, 'away_team']): 
                    totalGames += 1
                    oversHit += new_data.at[row2, 'hitOver']
            pct_overs_hit = float(oversHit)/float(totalGames)
            new_data.at[row, 'pct_overs_hit'] = pct_overs_hit
    #new_test_data = new_data.iloc[(ROW_START+1):-ROW_PLAYOFFS]
    total_data = pd.concat([total_data, new_data.iloc[(ROW_START+1):]], ignore_index=True)
    
print(total_data)
total_data.to_excel("probit_data.xlsx")