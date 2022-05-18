from django.db import models

# Create your models here.
class Song(models.Model):
	customId = models.IntegerField()
	artistName = models.CharField(max_length = 50)
	id = models.CharField(max_length = 12, primary_key = True)
	name = models.CharField(max_length = 50)
	releaseDate = models.DateField()
	kind = models.CharField(max_length = 30)
	artistId = models.CharField(max_length = 12)
	artistUrl = models.CharField(max_length = 100)
	contentAdvisoryRating = models.CharField(max_length = 30)
	artworkUrl100 = models.CharField(max_length = 100)
	genres = models.CharField(max_length = 200)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'song'


