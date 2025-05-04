from django.db import models
from account.models import Account
# Create your models here.
class AlbumUser(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên album")
    description = models.CharField(null=True,max_length=255, verbose_name="Mô tả")
    img_url = models.FileField(upload_to='album_users/', verbose_name="Ảnh bìa",null=True, blank=True)  # Sử dụng ImageField
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="người dùng", related_name="account_albums")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'album_users'
        verbose_name = "album_user"
        verbose_name_plural = "album_users"