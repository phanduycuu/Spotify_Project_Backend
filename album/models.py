from django.db import models

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên album")
    img_url = models.CharField(max_length=255, verbose_name="Đường dẫn")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'albums'
        verbose_name = "album"
        verbose_name_plural = "albums"