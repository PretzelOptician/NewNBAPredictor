import excel "C:\Users\aweso\OneDrive\Desktop\NBA PREDICTOR\total_data.xlsx", sheet("Sheet1") firstrow
summarize
describe
destring size_of_spread, replace force float
encode home_team, generate(home_s)
encode away_team, generate(away_s)
logit hitOver total size_of_spread pct_overs_hit ortg drtg drb threePAR ts ftr points_over_average_ratio hotness_ratio std_dev
logit hitOver d_tov drb drtg ftr hotness_ratio injury_gmsc injury_mins ortg pace pct_overs_hit points_over_average_ratio size_of_spread std_dev threePAR total totalppg ts