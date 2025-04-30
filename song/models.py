from django.db import models
from album.models import Album
from video.models import Video
from artist.models import Artist
# Create your models here.
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Album", related_name="album_songs")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    audio_url = models.FileField(upload_to='songs/', verbose_name="File nhạc")  # Đổi sang FileField
    duration = models.IntegerField(verbose_name="Thời lượng (giây)",null=True, blank=True)
    lyrics = models.CharField(max_length=1000, verbose_name="Lời bài hát")
    name = models.CharField(max_length=255, verbose_name="Tên bài hát")
    genre = models.CharField(max_length=100, verbose_name="Thể loại", blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Video", related_name="video_songs")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'songs'
        verbose_name = "song"
        verbose_name_plural = "songs"