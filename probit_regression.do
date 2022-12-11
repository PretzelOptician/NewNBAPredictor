import excel "C:\Users\aweso\OneDrive\Desktop\NBA PREDICTOR\probit_data.xlsx", sheet("Sheet1") firstrow
summarize
describe
destring size_of_spread, replace force float
display 1166/2120
probit hitOver total totalppg size_of_spread pct_overs_hit avg_*
predict over_prob, pr
count if over_prob > 0.53
count if over_prob > 0.53 & hitOver == 1
count if over_prob < 0.47
count if over_prob < 0.47 & hitOver == 0
estat classification
logit hitOver size_of_spread avg_popularity pct_overs_hit
