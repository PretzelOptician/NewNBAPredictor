import requests
import json
import pandas as pd
import numpy as np
import xlsxwriter
from bs4 import BeautifulSoup

for x in range(14): 
	api_url = "https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_" + str(2009+x) + ".html&div=div_advanced-team"
	response = requests.get(api_url) 
	soup = BeautifulSoup(response.content, 'html.parser')
	table = soup.find('table')
	df = pd.read_html(str(table))[0]
	df = df.drop(['Unnamed: 0_level_0'], axis=1)
	df.to_excel('../NBA-Spreadsheets/' + str(2009+x) + '/leagueStats.xlsx')
	print("Downloaded advanced stats for the " + str(2008+x) + "-" + str(2009+x) + " " + "season")