from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên nghệ sĩ")
    img_url = models.CharField(max_length=255, verbose_name="Đường dẫn")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'artists'
        verbose_name = "artist"
        verbose_name_plural = "artists"