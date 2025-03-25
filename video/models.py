from django.db import models

# Create your models here.
class Video(models.Model):
    video_url = models.CharField(max_length=255, verbose_name="Đường dẫn")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'videos'
        verbose_name = "video"
        verbose_name_plural = "videos"