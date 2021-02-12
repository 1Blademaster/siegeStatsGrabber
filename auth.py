import asyncio
import base64
import json
from datetime import datetime, timedelta

import aiohttp
import requests


class Auth:
	def __init__(self, email, password):
		self.token = base64.b64encode((email + ":" + password).encode("utf-8")).decode("utf-8")
		self.appId = '39baebad-39e5-4552-8c25-2c9b919064e2'
		self.getAuthData()

	def getAuthData(self):
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Basic ' + self.token,
			'Ubi-AppId': self.appId
		}
		r = requests.post('https://public-ubiservices.ubi.com/v3/profiles/sessions', headers=headers)

		respData = r.json()
		self.ticket = respData['ticket']
		self.sessionId = respData['sessionId']
		self.sessionKey = respData['sessionKey']
		self.spaceId = respData['spaceId']
		self.ownUserId = respData['userId']

	def getUserId(self, username):
		with open('cachedNames.txt', 'r') as f:
			for line in f.readlines():
				_line = line.split(' : ')
				if _line[0] == username:
					return _line[1].strip()
				
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Ubi_v1 t=' + self.ticket,
			'Ubi-AppId': self.appId,
			'Ubi-SessionId': self.sessionId,
			'Connection': 'keep-alive',
		}
		r = requests.get(f'https://public-ubiservices.ubi.com/v2/profiles?nameOnPlatform={username}&platformType=UPLAY', headers=headers)
		
		try:
			userId = r.json()['profiles'][0]['userId']

			with open('cachedNames.txt', 'a') as f:
				f.write(f'{username} : {userId}\n')

		except:
			print(f'Could not find the user ID for: {username}')
			userId = None

		return userId

	def getLink(self, statType, username):
		userId = self.getUserId(username)
		if not userId: return False

		if statType == 'summary':
			return f'https://r6s-stats.ubisoft.com/v1/current/summary/{userId}?gameMode=all,ranked,unranked,casual&platform=PC&startDate=20151210&endDate={datetime.now().strftime("%Y%m%d")}'
		elif statType == 'seasonal':
			return f'https://r6s-stats.ubisoft.com/v1/seasonal/summary/{userId}?gameMode=all,ranked,casual,unranked&platform=PC&startDate=20151210&endDate={datetime.now().strftime("%Y%m%d")}'
		elif statType == 'operator':
			return f'https://r6s-stats.ubisoft.com/v1/current/operators/{userId}?gameMode=all,ranked,casual,unranked&platform=PC&teamRole=attacker,defender&startDate=20151210&endDate={datetime.now().strftime("%Y%m%d")}'
		elif statType == 'rank':
			return f'https://public-ubiservices.ubi.com/v1/spaces/5172a557-50b5-4665-b7db-e3f2e8c5041d/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&season_id=-1&region_id=ncsa&profile_ids={userId}'
		elif statType == 'map':
			return f'https://r6s-stats.ubisoft.com/v1/current/maps/{userId}?gameMode=all,ranked,unranked,casual&platform=PC&startDate=20151210&endDate={datetime.now().strftime("%Y%m%d")}'
		elif statType == 'all':
			return [
				f'https://r6s-stats.ubisoft.com/v1/current/summary/{userId}?gameMode=all,ranked,unranked,casual&platform=PC&startDate=20151210&endDate={datetime.now().strftime("%Y%m%d")}',
				f'https://r6s-stats.ubisoft.com/v1/seasonal/summary/{userId}?gameMode=all,ranked,casual,unranked&platform=PC&startDate=20151210&endDate={datetime.now().strftime("%Y%m%d")}',
				f'https://r6s-stats.ubisoft.com/v1/current/operators/{userId}?gameMode=all,ranked,casual,unranked&platform=PC&teamRole=attacker,defender&startDate=20151210&endDate={datetime.now().strftime("%Y%m%d")}',
				f'https://public-ubiservices.ubi.com/v1/spaces/5172a557-50b5-4665-b7db-e3f2e8c5041d/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&season_id=-1&region_id=ncsa&profile_ids={userId}',
				f'https://r6s-stats.ubisoft.com/v1/current/maps/{userId}?gameMode=all,ranked,unranked,casual&platform=PC&startDate=20151210&endDate={datetime.now().strftime("%Y%m%d")}'
			]
		else:
			print('Unknown stat type')
			return False

	async def fetchData(self, link):
		headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Ubi_v1 t=' + self.ticket,
			'Ubi-AppId': self.appId,
			'Ubi-SessionId': self.sessionId,
			'Connection': 'keep-alive',
			'expiration': f'{(datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")}.657Z'
		}

		if link:
			async with aiohttp.ClientSession() as session:
				async with session.get(link, headers=headers) as r:
					
					if r.status == 200:
						return await r.json()
					else:
						print('An error occured: ')
						print(r.reason)
						return False
		else:
			return False
