from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
import json
import sqlite3
import math

from .models import Song
from .serializers import SongSerializer
from utilities.structure import Structure

# Create your views here.
class SongViewSet(viewsets.ModelViewSet):
	model = Song
	serializer_class = SongSerializer
	queryset = model.objects.all()


	def retrieve(self,request,*args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		#return serializer.data
		#return {'status':'success', 'message':'', 'data':serializer.data}	
		return Response(Structure.success('',serializer.data),
			status=status.HTTP_200_OK)

	def list(self,request,*args, **kwargs):
		queryset = super(SongViewSet, self).get_queryset()
		name = self.request.query_params.get('name', None)
		artistName = self.request.query_params.get('artistName', None)
		id = self.request.query_params.get('id', None)
		dateReleaseFrom = self.request.query_params.get('dateReleaseFrom', None)
		dateReleaseTo = self.request.query_params.get('dateReleaseTo', None)
		genreName = self.request.query_params.get('genreName', None)
		top50 = self.request.query_params.get('top50', None)
		page = self.request.query_params.get('page', None)

		try:
			sqlCommand = "SELECT * FROM song WHERE id <> 0 "
			if name:
				sqlCommand = sqlCommand + "AND name like '%" + name + "%'"
			if artistName:
				sqlCommand = sqlCommand + "AND artistName like '%" + artistName + "%'"
			if id:
				sqlCommand = sqlCommand + "AND id like '%" + id + "%'"
			if dateReleaseFrom:
				sqlCommand = sqlCommand + "AND ReleaseDate >= '" + dateReleaseFrom + "'"
			if dateReleaseTo:
				sqlCommand = sqlCommand + "AND ReleaseDate <= '" + dateReleaseTo + "'"
			if genreName:
				if len(genreName) > 4:
					sqlCommand = sqlCommand + "AND genres like '%" + genreName + "%'"
				else:
					return Response(Structure.warning('The genreName param must to be at least 4 characters'),
						status=status.HTTP_400_BAD_REQUEST)

			connection = sqlite3.connect('song.sqlite3')
			cursor = connection.cursor()
			cursor.execute(sqlCommand)
			columns = cursor.description
			rowData = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
			dataReturn = []
			for row in rowData:
				objGenres = []
				splitedGenres = row['genres'].split('|')
				for objString in splitedGenres:
					objGenres.append(json.loads(objString))

				#import pdb; pdb.set_trace()

				dataReturn.append({
					'customId': row['customId'],
					'artistName': row['artistName'],
					'id': row['id'],
					'name': row['name'],
					'ReleaseDate': row['releaseDate'],
					'kind': row['kind'],
					'artistId': row['artistId'],
					'artistUrl': row['artistUrl'],
					'contentAdvisoryRating': row['contentAdvisoryRating'],
					'artworkUrl100': row['artworkUrl100'],
					'genres': objGenres
					})
			if page:
				page = int(page)
				perPage = 10
				totalPage = math.ceil(len(dataReturn) / perPage)
				
				if page <= int(totalPage):
					if page == 1:
						objectfrom = 0
						objectTo = perPage
					else:
						objectfrom = ((page - 1) * perPage)
						objectTo = objectfrom + perPage
					data = {
						'page': page,
						'perPage': perPage,
						'totalPages': int(totalPage),
						'results': dataReturn[objectfrom:objectTo],
						'next': page + 1 if page < totalPage else None,
						'previus': page - 1 if page > 1 else None
					}
					return Response(Structure.success('', data),
						status=status.HTTP_200_OK)
				else:
					return Response(
						Structure.warning(
							'The param page must be less than or equals to total pages (' + 
							str(int(totalPage)) +')'),
					 status = status.HTTP_400_BAD_REQUEST)
			else:
				if top50:
					return Response(Structure.success('', dataReturn[0:50]),
						status=status.HTTP_200_OK)								
				else:
					return Response(Structure.success('', dataReturn),
						status=status.HTTP_200_OK)			

		except Exception as e:
			return Response(Structure.error500(e), status = status.HTTP_400_BAD_REQUEST)

	def create(self, request, *args, **kwargs):
		try:
			if request.method == 'POST':
				artistName = request.data['artistName'] if 'artistName' in request.data else None
				name = request.data['name'] if 'name' in request.data else None
				id = request.data['id'] if 'id' in request.data else None
				releaseDate = request.data['releaseDate'] if 'releaseDate' in request.data else None
				kind = request.data['kind'] if 'kind' in request.data else None
				artistId = request.data['artistId'] if 'artistId' in request.data else None
				artistUrl = request.data['artistUrl'] if 'artistUrl' in request.data else None
				contentAdvisoryRating = request.data['contentAdvisoryRating'] if 'contentAdvisoryRating' in request.data else ''
				artworkUrl100 = request.data['artworkUrl100'] if 'artworkUrl100' in request.data else None
				genresId = request.data['genresId'] if 'genresId' in request.data else None

				

				if artistName and id and name and releaseDate and kind and artistId and artistUrl and artworkUrl100 and genresId:
					genresValue = ''
					if genresId == '34':
						return Response(
							Structure.warning(
								'The param genres value is not permited'),
						 status = status.HTTP_400_BAD_REQUEST)
					else:
						sqlCommand = "SELECT DISTINCT genres FROM song WHERE genres like '%\"" + genresId + "\"%'"
						sqlCommand = sqlCommand.replace('\\','')
						
						connection = sqlite3.connect('song.sqlite3')
						cursor = connection.cursor()
						cursor.execute(sqlCommand)
						for value in cursor.fetchall():
							genresValue = value[0]
							break

					lastId = self.model.objects.all().order_by('customId').last().customId if self.model.objects.all().order_by('customId').last() else 0
					lastId = int(lastId) + 1
					song = Song(
						customId = lastId,
						id = id,
						artistName = artistName,
						name = name,
						releaseDate = releaseDate,
						kind = kind,
						artistId = artistId,
						artistUrl = artistUrl,
						contentAdvisoryRating = contentAdvisoryRating,
						artworkUrl100 = artworkUrl100,
						genres = genresValue
						)
					song.save()
					return Response(Structure.success('The song has been added succesfully', None),
						status=status.HTTP_200_OK)

				else:
					return Response(
						Structure.warning(
							'The params required were not received'),
					 status = status.HTTP_400_BAD_REQUEST)
			else:
				return Response(
					Structure.warning(
						'Method is not permited'),
				 status = status.HTTP_400_BAD_REQUEST)				

		except Exception as e:
			print(e)
			return Response(Structure.error500(e), status = status.HTTP_400_BAD_REQUEST)

	@action(methods=['delete'], detail=False, url_path='delete', url_name='song.delete')
	def delete(self, request, *args, **kwargs):
		try:
			customId = self.request.query_params.get('customId', None)
			if customId:
				song = self.model.objects.filter(customId = customId).first()
				song.delete()
				return Response(Structure.success('The song has been deleted succesfully', None),
				status=status.HTTP_200_OK)
			else:
				return Response(Structure.warning('The param customId is required by to delete a song'),
				 status = status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response(Structure.error500(e), status = status.HTTP_400_BAD_REQUEST)
