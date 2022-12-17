import pandas as pd
from bs4 import BeautifulSoup
import requests

ROW_START = 100
ROW_PLAYOFFS = 100

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

def get_abbrv(team): 
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
    elif team == 'NewYork': return 'NYK'
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
    elif team == 'Charlotte': return 'CHA'
    elif team == 'Dallas': return 'DAL'

def get_game_log(team, year): 
    team_str = get_abbrv(team)
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

pd.set_option('display.max_rows', None)
total_data = pd.DataFrame({'year': [], 'hitOver': [], 'total': [], 'avg_popularity': [], 'totalppg': [], 'size_of_spread': [], 'home_team': [], 'away_team': [], 'pct_overs_hit': [], 'avg_prev_year_efg_pct_off': [], 'avg_prev_year_tov_pct_off': [], 'avg_prev_year_orb_pct': [], 'avg_prev_year_ft_per_fga_off': [], 'avg_prev_year_efg_pct_def': [], 'avg_prev_year_tov_pct_def': [], 'avg_prev_year_drb_pct': [], 'avg_prev_year_ft_per_fga_def': [], 'avg_prev_year_netrtg': [], 'avg_prev_year_pace': []})

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
    for year in range(2014, 2022):
        # Use the get_game_log function to retrieve the dataframe for the current team and year
        df = get_game_log(team, year)
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
    new_data = pd.DataFrame({'year': [], 'hitOver': [], 'total': [], 'avg_popularity': [], 'totalppg': [], 'size_of_spread': [], 'home_team': [], 'away_team': [], 'pct_overs_hit': [], 'avg_prev_year_efg_pct_off': [], 'avg_prev_year_tov_pct_off': [], 'avg_prev_year_orb_pct': [], 'avg_prev_year_ft_per_fga_off': [], 'avg_prev_year_efg_pct_def': [], 'avg_prev_year_tov_pct_def': [], 'avg_prev_year_drb_pct': [], 'avg_prev_year_ft_per_fga_def': [], 'avg_prev_year_netrtg': [], 'avg_prev_year_pace': []})
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
            homeppg = 0
            gamesPlayed = 0
            for row2 in range(row-1): 
                if data.at[row2, 'Team'] == team1: 
                    homeppg+= data.at[row2, 'Final']
                    gamesPlayed += 1
            homeppg /= (gamesPlayed if gamesPlayed>0 else 1)
            awayppg = 0
            gamesPlayed = 0
            for row2 in range(row-1): 
                if data.at[row2, 'Team'] == team2: 
                    awayppg+= data.at[row2, 'Final']
                    gamesPlayed += 1
            awayppg /= (gamesPlayed if gamesPlayed>0 else 1)
            totalppg = homeppg + awayppg
            avg_followers = (get_avg_followers(team2) + get_avg_followers(team1))/2
            
            # four factors stuff
            o_efg = 0
            o_tov = 0
            orb = 0
            o_ftfga = 0
            d_efg = 0
            d_tov = 0
            drb = 0
            d_ftfga = 0
            netrating = 0
            pace = 0
            for row2 in range(leagueData.shape[0]): 
                if leagueData.iat[row2, 0].startswith(convert_team_name(team1)) or leagueData.iat[row2, 0].startswith(convert_team_name(team2)): 
                    o_efg += leagueData.iat[row2, 17]
                    o_tov += leagueData.iat[row2, 18]
                    orb += leagueData.iat[row2, 19]
                    o_ftfga += leagueData.iat[row2, 20]
                    d_efg += leagueData.iat[row2, 22]
                    d_tov += leagueData.iat[row2, 23]
                    drb += leagueData.iat[row2, 24]
                    d_ftfga += leagueData.iat[row2, 25]
                    netrating += leagueData.iat[row2, 11]
                    pace += leagueData.iat[row2, 12]
            o_efg /= 2
            o_tov /= 2
            orb /= 2
            o_ftfga /= 2
            d_efg /= 2
            d_tov /= 2
            drb /= 2
            d_ftfga /= 2
            netrating /= 2
            pace /= 2
            

            ## calculate pace
            game_log_1 = game_logs[(team_name_mapping.get(team1, team1), year)]
            game_log_2 = game_logs[(team_name_mapping.get(team2, team2), year)]

            if not push: 
                new_data.loc[len(new_data.index)] = [year, (1 if hitOver else 0), total, avg_followers, totalppg, size_of_spread, data.at[row, 'Team'], data.at[row-1, 'Team'], None, o_efg, o_tov, orb, o_ftfga, d_efg, d_tov, drb, d_ftfga, netrating, pace]

            print("total: " + str(total))
            print("size of spread: " + str(size_of_spread))
            print("final: " + str(final_score))
            print("hit over? " + str(hitOver))
            print("home ppg: " + str(homeppg))
            print("away ppg: " + str(awayppg))
            print("avg popularity: " + str(avg_followers))
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
    total_data = pd.concat([total_data, new_data.iloc[(ROW_START+1):-ROW_PLAYOFFS]], ignore_index=True)
    
print(total_data)
total_data.to_excel("probit_data.xlsx")