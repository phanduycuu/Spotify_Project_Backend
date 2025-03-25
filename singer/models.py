from django.db import models
from artist.models import Artist
from song.models import Song
# Create your models here.
class Singer(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name="artist", related_name="artist_singers")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name="song", related_name="song_singers")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'singers'
        verbose_name = "singer"
        verbose_name_plural = "singers"