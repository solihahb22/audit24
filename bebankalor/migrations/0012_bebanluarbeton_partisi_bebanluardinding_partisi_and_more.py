# Generated by Django 4.2.8 on 2024-01-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bebankalor', '0011_bebanluarkaca_jenis_frame_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bebanluarbeton',
            name='partisi',
            field=models.CharField(default='P', max_length=1),
        ),
        migrations.AddField(
            model_name='bebanluardinding',
            name='partisi',
            field=models.CharField(default='P', max_length=1),
        ),
        migrations.AddField(
            model_name='bebanluarkaca',
            name='partisi',
            field=models.CharField(default='P', max_length=1),
        ),
        migrations.AddField(
            model_name='bebanluarpintu',
            name='partisi',
            field=models.CharField(default='P', max_length=1),
        ),
    ]
