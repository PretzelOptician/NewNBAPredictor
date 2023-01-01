import numpy as np
import pandas as pd

## takes a dataframe with game information (see get_curr_spreadsheets.py) and returns the same dataframe with a column for predicted probabilities

def logit(df): 
    home_dummy = {
        'Atlanta': 0.0,
        'Boston': -0.0049771,
        'Brooklyn': -0.0976231,
        'Charlotte': -0.1616863,
        'Chicago': -0.1792073,
        'Cleveland': -0.09652,
        'Dallas': -0.1852565, 
        'Denver': 0.1810079, 
        'Detroit': 0.1986823,
        'GoldenState': -0.255966,
        'Houston': 0.0367426, 
        'Indiana': -0.0293679, 
        'LAClippers': -0.065803, 
        'LALakers': -0.2043106, 
        'Memphis': -0.1364876, 
        'Miami': 0.0986813, 
        'Milwaukee': 0.0950917, 
        'Minnesota': 0.1531429,
        'NewOrleans': 0.3482693, 
        'NewYork': -0.1498722, 
        'OklahomaCity': -0.0853131, 
        'Orlando': 0.0034486, 
        'Philadelphia': 0.0431477, 
        'Phoenix': 0.1017284, 
        'Portland': 0.045715, 
        'Sacramento': 0.1420166, 
        'SanAntonio': 0.0354622, 
        'Toronto': 0.0958902, 
        'Utah': -0.2651519, 
        'Washington': 0.1219588, 
    }
    away_dummy = {
        'Atlanta': 0.0,
        'Boston': 0.082884,
        'Brooklyn': 0.0886438,
        'Charlotte': 0.1817,
        'Chicago': -0.0423023,
        'Cleveland': 0.1211452,
        'Dallas': -0.0623778, 
        'Denver': 0.1134192, 
        'Detroit': -0.133122,
        'GoldenState': -0.2301149,
        'Houston': -0.0220769, 
        'Indiana': 0.0618522, 
        'LAClippers': 0.0357576, 
        'LALakers': 0.1241524, 
        'Memphis': 0.0785158, 
        'Miami': -0.1313578, 
        'Milwaukee': 0.1319199, 
        'Minnesota': 0.3885524,
        'NewOrleans': 0.0353463, 
        'NewYork': 0.042184, 
        'OklahomaCity': -0.0733661, 
        'Orlando': -0.1777448, 
        'Philadelphia': -0.1730964, 
        'Phoenix': 0.0218554, 
        'Portland': 0.2001103, 
        'Sacramento': 0.0612493, 
        'SanAntonio': 0.1352708, 
        'Toronto': 0.1909384, 
        'Utah': -0.1020129, 
        'Washington': 0.2796706,
    }
    #chatGPT code:: 
    # Extract the relevant columns from the dataframe
    X = df[['size_of_spread', 'drtg', 'threePAR', 'points_over_average_ratio', 'std_dev']]
    # Add a column of consts to the dataframe to represent the intercept term
    X['intercept'] = 5.472246
    print(X)
    coefs = [0.0162176, -0.0308513, 1.435453, -3.168072, 0.0409806, 1]
    z = np.dot(X, coefs)
    for game in range(len(z)): 
        home_dummy_val = home_dummy.get(df.at[game, 'home_team'])
        print(home_dummy_val)
        away_dummy_val = away_dummy.get(df.at[game, 'away_team'])
        print(away_dummy_val)
        z[game] += (home_dummy_val + away_dummy_val)
    prob = 1 / (1 + np.exp(-z))
    print(prob)
    # Calculate the probability using the sigmoid function
    #THIS ALL WORKS LMAO
    df['calc_over_prob'] = prob
    return df

df = pd.read_excel('probit_data_2023.xlsx')
print(logit(df))
