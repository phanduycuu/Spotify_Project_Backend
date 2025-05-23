# Generated by Django 5.0.12 on 2025-04-14 16:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('album', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Đã xóa')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_favourite_albums', to=settings.AUTH_USER_MODEL, verbose_name='account')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_albums', to='album.album', verbose_name='album')),
            ],
            options={
                'verbose_name': 'favourite_album',
                'verbose_name_plural': 'favourite_albums',
                'db_table': 'favourite_albums',
            },
        ),
    ]
