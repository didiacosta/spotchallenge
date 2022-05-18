from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
import json
import sqlite3

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

			return Response(Structure.success('', dataReturn),
				status=status.HTTP_200_OK)			

		except Exception as e:
			print (e)
			return Response(Structure.error500(e), status = status.HTTP_400_BAD_REQUEST)
			



	def create(self, request, *args, **kwargs):
		pass

	def destroy(self,request,*args,**kwargs):
		pass

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
