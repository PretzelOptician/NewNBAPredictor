import excel "C:\Users\aweso\OneDrive\Desktop\NBA PREDICTOR\probit_data.xlsx", sheet("Sheet1") firstrow
summarize
describe
destring size_of_spread, replace force float
logit hitOver size_of_spread avg_popularity pct_overs_hit
logit hitOver total avg_popularity totalppg size_of_spread pct_overs_hit pace drtg threePAR ts ftr ftperfga points_over_average_ratio hotness_ratio std_dev
predict over_prob, pr
count if over_prob > 0.53
count if over_prob > 0.53 & hitOver == 1
display 927/1665
count if over_prob < 0.47
count if over_prob < 0.47 & hitOver == 0
display 630/1155
encode home_team, generate(home_s)
encode away_team, generate(away_s)
logit hitOver total avg_popularity totalppg size_of_spread pct_overs_hit pace drtg threePAR ts ftr ftperfga points_over_average_ratio hotness_ratio std_dev i.home_s i.away_s
estat classification