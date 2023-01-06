import excel "C:\Users\aweso\OneDrive\Desktop\NBA PREDICTOR\probit_data.xlsx", sheet("Sheet1") firstrow
summarize
describe
destring size_of_spread, replace force float
encode home_team, generate(home_s)
encode away_team, generate(away_s)
logit hitOver total size_of_spread pct_overs_hit ortg drtg drb threePAR ts ftr points_over_average_ratio hotness_ratio std_dev