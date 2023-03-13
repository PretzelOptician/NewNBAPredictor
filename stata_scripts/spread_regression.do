* DEPRECATED: StataBE 17 license expired and Stata is not really needed to do what we want to do. However, keeping the scripts here for reference

import excel "C:\Users\aweso\OneDrive\Desktop\NBA PREDICTOR\historic_data\spread_data.xlsx", sheet("Sheet1") firstrow
encode home_team, generate(home_s)
encode away_team, generate(away_s)
destring spread, replace force float
logit home_spread_hit spread pace_h pace_a ortg_h ortg_a drb_h drb_a threePAR_h threePAR_a ts_h ts_a ftr_h ftr_a d_tov_h d_tov_a o_tov_h o_tov_a ftperfga_h ftperfga_a points_over_average_ratio_h points_over_average_ratio_a hotness_ratio_h hotness_ratio_a std_dev_h std_dev_a win_pct_h win_pct_a rsw_h rsw_a ratings_2k_h ratings_2k_a win_pct_close_h win_pct_close_a sos_h sos_a mov_a_h mov_a_a injury_mins_h injury_mins_a drtg_h drtg_a
estat classification