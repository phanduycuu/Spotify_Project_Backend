from django.db import models
from account.models import Account
from song.models import Song
# Create your models here.
class FavouriteSong(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="account", related_name="account_favourite_songs")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name="song", related_name="favourite_songs")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")


    class Meta:
        db_table = 'favourite_songs'
        verbose_name = "favourite_song"
        verbose_name_plural = "favourite_songs"