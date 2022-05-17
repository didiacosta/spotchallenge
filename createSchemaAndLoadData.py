import sqlite3
import json
import requests
import os
try:
	os.remove('song.sqlite3')
	connection = sqlite3.connect('song.sqlite3')
	cursor = connection.cursor()
	print('creating database song.sqlite3...')
	cursor.execute('''CREATE TABLE IF NOT EXISTS song
	              (artistName TEXT, id TEXT, name TEXT, \
	               releaseDate DATE, kind TEXT, artistId TEXT, \
	               artistUrl TEXT, contentAdvisoryRating TEXT, \
	               artworkUrl100 TEXT, genres JSON)''')
	connection.commit()
	print ('song.sqlite3 database created !!')
	#connection.close()
	response = requests.get('https://rss.applemarketingtools.com/api/v2/us/music/most-played/100/songs.json')
	if response:
		data = response.json()
		sqlite_insert = """INSERT INTO song
				(artistName, id, name, releaseDate, kind, artistId, 
				artistUrl, contentAdvisoryRating, artworkUrl100, 
				genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
		print ('Start insert registers in song.sqlite3 database....')
		count = 0
		for obj in data['feed']['results']:
			
			genres = ''
			sep = ''
			for genre in obj['genres']:
				genres = genres + sep + json.dumps(genre)
				sep = '|'
			#import pdb; pdb.set_trace()
			artistName = obj['artistName'] if 'artistName' in obj else ''
			id = obj['id'] if 'id' in obj else ''
			name = obj['name'] if 'name' in obj else ''
			releaseDate = obj['releaseDate'] if 'releaseDate' in obj else ''
			kind = obj['kind'] if 'kind' in obj else ''
			artistId = obj['artistId'] if 'artistId' in obj else ''
			artistUrl = obj['artistUrl'] if 'artistUrl' in obj else ''
			contentAdvisoryRating = obj['contentAdvisoryRating'] if 'contentAdvisoryRating' in obj else ''
			artworkUrl100 = obj['artworkUrl100'] if 'artworkUrl100' in obj else ''

			dataTupla = (artistName, id, name, releaseDate
				, kind, artistId, artistUrl , contentAdvisoryRating
				, artworkUrl100, genres)

			cursor.execute(sqlite_insert, dataTupla)
			connection.commit()
			count = count + 1
			print ('Song register inserted in database: ' + obj['name'])
			
		print(str(count) + ' Registers inserted successfully into song.sqlite3 database !!!')
		connection.close()
except Exception as e:
	print (e)
finally:
	if connection:
		connection.close()

