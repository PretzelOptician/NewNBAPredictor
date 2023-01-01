import excel "C:\Users\aweso\OneDrive\Desktop\NBA PREDICTOR\probit_data.xlsx", sheet("Sheet1") firstrow
summarize
describe
destring size_of_spread, replace force float
encode home_team, generate(home_s)
encode away_team, generate(away_s)
logit hitOver size_of_spread drtg threePAR points_over_average_ratio std_dev i.home_s i.away_s
logit hitOver size_of_spread drtg threePAR points_over_average_ratio i.home_s i.away_s
estat classification
predict over_prob
summ
count if over_prob > 0.56
count if over_prob > 0.56 & hitOver == 1
display 755/1249
count if over_prob < 0.44
count if over_prob < 0.44 & hitOver == 0
display 579/1006
display (755+579)/(1006+1249)