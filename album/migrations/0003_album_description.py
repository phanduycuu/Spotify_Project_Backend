# Generated by Django 5.0.12 on 2025-04-30 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0002_alter_album_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.CharField(max_length=255, null=True, verbose_name='Mô tả'),
        ),
    ]
