# Generated by Django 5.0.12 on 2025-04-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0004_song_artist_song_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio_url',
            field=models.FileField(upload_to='songs/', verbose_name='File nhạc'),
        ),
    ]
