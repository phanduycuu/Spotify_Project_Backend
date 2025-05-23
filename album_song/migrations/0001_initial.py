# Generated by Django 5.0.12 on 2025-05-04 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('album_user', '0001_initial'),
        ('song', '0008_song_img_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Đã xóa')),
                ('album_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='album_user_song', to='album_user.albumuser', verbose_name='album_user')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song_album_user', to='song.song', verbose_name='song')),
            ],
            options={
                'verbose_name': 'album_songs',
                'verbose_name_plural': 'album_song',
                'db_table': 'album_songs',
            },
        ),
    ]
