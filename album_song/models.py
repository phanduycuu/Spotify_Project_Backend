from django.db import models
from album_user.models import AlbumUser
from song.models import Song
# Create your models here.
class AlbumSong(models.Model):
    album_user = models.ForeignKey(AlbumUser, on_delete=models.CASCADE, verbose_name="album_user", related_name="album_user_song")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name="song", related_name="song_album_user")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    class Meta:
        db_table = 'album_songs'
        verbose_name = "album_songs"
        verbose_name_plural = "album_song"