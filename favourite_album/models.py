from django.db import models
from account.models import Account
from album.models import Album
# Create your models here.
class FavouriteAlbum(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="account", related_name="account_favourite_albums")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name="album", related_name="favourite_albums")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")


    class Meta:
        db_table = 'favourite_albums'
        verbose_name = "favourite_album"
        verbose_name_plural = "favourite_albums"
        constraints = [
            models.UniqueConstraint(fields=['account', 'album'], name='unique_account_album_favourite')
        ]
