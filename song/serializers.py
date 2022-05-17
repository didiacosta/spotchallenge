from .models import Song
from rest_framework import serializers

class SongSerializer(serializers.HyperlinkedModelSerializer):

	genres = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Song
		fields = ('id', 'artistName', 'name', 'releaseDate', 'kind', 'artistId',
			'artistUrl', 'contentAdvisoryRating', 'artworkUrl100', 'genres')

	def get_genres(self,obj):
		return obj.genres