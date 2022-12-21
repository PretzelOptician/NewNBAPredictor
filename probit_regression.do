import excel "C:\Users\aweso\OneDrive\Desktop\NBA PREDICTOR\probit_data.xlsx", sheet("Sheet1") firstrow
summarize
describe
destring size_of_spread, replace force float
logit hitOver size_of_spread avg_popularity pct_overs_hit
logit hitOver total avg_popularity totalppg size_of_spread pct_overs_hit pace drtg threePAR ts ftr ftperfga
drop over_prob
predict over_prob, pr
count if over_prob > 0.55
count if over_prob > 0.53
count if over_prob > 0.53 & hitOver==1
display 743/1377
count if over_prob > 0.54
count if over_prob > 0.54 & hitOver==1
display 384/692