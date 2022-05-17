from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action

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
		pass

	def create(self, request, *args, **kwargs):
		pass

	def destroy(self,request,*args,**kwargs):
		pass

	@action(methods=['get'], detail=False, url_path='loadData', url_name='song.loadDataFromJson')
	def loadData(self, request, *args, **kwargs):
		pass
