import asyncio
import json
import os
import time

from datetime import datetime

import aiohttp
import numpy as np
import pyautogui
from colorama import Fore, Style, init
from PIL import Image
from tabulate import tabulate

from auth import Auth

CURRENTSEASON = ('Y5', 'S4')

def getRank(mmr, colour=True):
	rank = 'UNKNOWN'
	if mmr >= 5000:
		rank = 'CHAMPION'
	if mmr < 5000:
		rank = 'DIAMOND'
	if mmr < 4400:
		rank = 'PLAT 1'
	if mmr < 4000:
		rank = 'PLAT 2'
	if mmr < 3600:
		rank = 'PLAT 3'
	if mmr < 3200:
		rank = 'GOLD 1'
	if mmr < 3000:
		rank = 'GOLD 2'
	if mmr < 2800:
		rank = 'GOLD 3'
	if mmr < 2600:
		rank = 'SILVER 1'
	if mmr < 2500:
		rank = 'SILVER 2'
	if mmr < 2400:
		rank = 'SILVER 3'
	if mmr < 2300:
		rank = 'SILVER 4'
	if mmr < 2200:
		rank = 'SILVER 5'
	if mmr < 2100:
		rank = 'BRONZE 1'
	if mmr < 2000:
		rank = 'BRONZE 2'
	if mmr < 1900:
		rank = 'BRONZE 3'
	if mmr < 1800:
		rank = 'BRONZE 4'
	if mmr < 1700:
		rank = 'BRONZE 5'
	if mmr < 1600:
		rank = 'COPPER 1'
	if mmr < 1500:
		rank = 'COPPER 2'
	if mmr < 1400:
		rank = 'COPPER 3'
	if mmr < 1300:
		rank = 'COPPER 4'
	if mmr < 1200:
		rank = 'COPPER 5'

	if colour:
		if 'CHAMPION' in rank:
			rank = f'{Fore.MAGENTA}{Style.BRIGHT}{rank}{Style.RESET_ALL}'
		elif 'DIAMOND' in rank:
			rank = f'{Fore.BLUE}{Style.BRIGHT}{rank}{Style.RESET_ALL}'
		elif 'PLAT' in rank:
			rank = f'{Fore.CYAN}{Style.BRIGHT}{rank}{Style.RESET_ALL}'
		elif 'GOLD' in rank:
			rank = f'{Fore.YELLOW}{Style.BRIGHT}{rank}{Style.RESET_ALL}'
		elif 'SILVER' in rank:
			rank = f'{Fore.WHITE}{Style.BRIGHT}{rank}{Style.RESET_ALL}'
		elif 'BRONZE' in rank:
			rank = f'{Fore.RED}{Style.BRIGHT}{rank}{Style.RESET_ALL}'
		elif 'COPPER' in rank:
			rank = f'{Fore.RED}{Style.DIM}{rank}{Style.RESET_ALL}'

	return rank

def getPosNegNumber(number):
	if number > 1:
		return f'{Fore.GREEN}{number}{Style.RESET_ALL}'
	elif number < 1:
		return f'{Fore.RED}{number}{Style.RESET_ALL}'
	else:
		return f'{number}'

def getMostPlayedOpByTime(operators):
	d = {}
	for op in operators:
		d[op['statsDetail']] = op['minutesPlayed']
	
	for op in operators:
		if op['statsDetail'] == max(d, key=d.get):
			return op

def getMostPlayedMapByTime(maps):
	d = {}
	for _map in maps:
		d[_map['statsDetail']] = _map['minutesPlayed']
	
	for _map in maps:
		if _map['statsDetail'] == max(d, key=d.get):
			return _map

def calcTime(func, args):
    startTime = time.perf_counter()
    func(args)
    actualEndTime = time.perf_counter() - startTime
    formatEndTime = '{:.15f}'.format(float(actualEndTime))

    return formatEndTime

async def printPlayerStats(a, username):
	# Seasonal

	seasonalLink = a.getLink('seasonal', username)
	if not seasonalLink:
		print(f'An error occured while fetching the seasonal link for {username}')
		return
	seasonalData = await a.fetchData(seasonalLink)
	if not seasonalData:
		print(f'An error occured while fetching the seasonal data for {username}')
		return
	
	# Rank

	rankLink = a.getLink('rank', username)
	if not rankLink:
		print(f'An error occured while fetching the rank link for {username}')
		return
	rankData = await a.fetchData(rankLink)
	if not rankData:
		print(f'An error occured while fetching the rank data for {username}')
		return
		
	# Summary

	# summaryLink = a.getLink('summary', username)
	# if not summaryLink:
	# 	print(f'An error occured while fetching the summary link for {username}')
	# 	return
	# summaryData = a.fetchData(summaryLink)
	# if not summaryData:
	# 	print(f'An error occured while fetching the summary data for {username}')
	# 	return

	# Operator

	operatorLink = a.getLink('operator', username)
	if not operatorLink:
		print(f'An error occured while fetching the operator link for {username}')
		return
	operatorData = await a.fetchData(operatorLink)
	if not operatorData:
		print(f'An error occured while fetching the operator data for {username}')
		return

	# Map

	mapLink = a.getLink('map', username)
	if not mapLink:
		print(f'An error occured while fetching the map link for {username}')
		return
	mapData = await a.fetchData(mapLink)
	if not mapData:
		print(f'An error occured while fetching the map data for {username}')
		return

	rankData = rankData['players'][list(rankData['players'].keys())[0]]

	updateTime = rankData['update_time']
	# "update_time": "2021-02-08T23:40:46.585000+00:00",
	updateTime = updateTime[:len(updateTime) - 13]
	updateTime = datetime.strptime(updateTime, '%Y-%m-%dT%H:%M:%S') if updateTime != '1970-01-01T0' else 'None'

	attackOpData = operatorData['platforms']['PC']['gameModes']['all']['teamRoles']['attacker']
	defenceOpData = operatorData['platforms']['PC']['gameModes']['all']['teamRoles']['defender']

	mapData = mapData['platforms']['PC']['gameModes']

	tableRows = [['Username', username]]
	
	if 'ranked' in seasonalData['platforms']['PC']['gameModes']:
		for season in seasonalData['platforms']['PC']['gameModes']['ranked']['teamRoles']['all']:
			if season['seasonYear'] == CURRENTSEASON[0] and season['seasonNumber'] == CURRENTSEASON[1]:
				tableRows.append(['Ranked KD', getPosNegNumber(round(season['killDeathRatio']['value'], 2))])
				tableRows.append(['Ranked WL', getPosNegNumber(round(season['winLossRatio'], 2))])
				tableRows.append(['Ranked MATCHES PLAYED', round(season['matchesPlayed'])])
				
				tableRows.append(['Ranked RANK', getRank(rankData['mmr'])])
				tableRows.append(['Ranked MMR', round(rankData['mmr'])])
				tableRows.append(['Ranked MAX MMR', f"{round(rankData['max_mmr'])} : {getRank(rankData['max_mmr'], colour=False)}"])
				tableRows.append(['Ranked LAST MMR DIFF', getPosNegNumber(round(rankData['last_match_mmr_change']))])

				mostPlayedMap = getMostPlayedMapByTime(mapData['ranked']['teamRoles']['all'])
				tableRows.append(['Ranked MAIN MAP', f"{mostPlayedMap['statsDetail']} : {getPosNegNumber(round(mostPlayedMap['killDeathRatio']['value'], 2))}"])
				break
		else:
			tableRows.append(['Ranked KD', 'Unknown'])
	else:
		for season in seasonalData['platforms']['PC']['gameModes']['all']['teamRoles']['all']:
			if season['seasonYear'] == CURRENTSEASON[0] and season['seasonNumber'] == CURRENTSEASON[1]:
				tableRows.append(['General KD', getPosNegNumber(round(season['killDeathRatio']['value'], 2))])
				tableRows.append(['General WL', getPosNegNumber(round(season['winLossRatio'], 2))])

				mostPlayedMap = getMostPlayedMapByTime(mapData['all']['teamRoles']['all'])
				tableRows.append(['General MAIN MAP', f"{mostPlayedMap['statsDetail']} : {getPosNegNumber(round(mostPlayedMap['killDeathRatio']['value'], 2))}"])
				break

	atkOp = getMostPlayedOpByTime(attackOpData)
	defOp = getMostPlayedOpByTime(defenceOpData)

	tableRows.append(['General ATK MAIN', f'{atkOp["statsDetail"]} : {getPosNegNumber(round(atkOp["killDeathRatio"]["value"], 2))}'])

	tableRows.append(['General DEF MAIN', f'{defOp["statsDetail"]} : {getPosNegNumber(round(defOp["killDeathRatio"]["value"], 2))}'])
	
	print(tabulate(tableRows, tablefmt="psql"))
	print(f'Last updated: {updateTime.strftime("%b %d %H:%M:%S")}' if updateTime != 'None' else 'Last updated: Unknown')

def showLeaderboard():
	print('Return to siege and press TAB in 3 seconds')
	time.sleep(3)
	print('Taking screenshot now')
	time.sleep(0.25)

	img = pyautogui.screenshot()
	img = np.array(img)

	croppedImg = img[365:790, 465:900]

	croppedImgObject = Image.fromarray(croppedImg)
	croppedImgObject.show()

async def run():
	try:
		a = Auth(os.environ['email'], os.environ['email_password'])
		while True:
			usernames = input('\nEnter a username to search: ')
			if usernames == '':
				print('Quitting.')
				break
			elif usernames == 't':
				showLeaderboard()
			elif usernames == 's':
				a.test()
			else:
				usernames = usernames.split(',')
				for username in usernames:
					username = username.strip()
					if username:
						startTime = time.perf_counter()

						await printPlayerStats(a, username)

						print('Done in {:.9f}s'.format(float(time.perf_counter() - startTime)))
	except aiohttp.client_exceptions.ServerDisconnectedError:
		print('\n An error occured while connected to the UBISOFT API, please re-run the script to try and reconnect.')
	except KeyboardInterrupt:
		print('\nQuitting.')
		exit()


if __name__ == '__main__':
	init(autoreset=True)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	
	


	
	