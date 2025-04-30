from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tiêu đề video")  # Thêm field title
    video_url = models.FileField(upload_to='videos/', verbose_name="File video")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    def __str__(self):
        return self.title  # Sửa để trả về title thay vì name

    class Meta:
        db_table = 'videos'
        verbose_name = "video"
        verbose_name_plural = "videos"