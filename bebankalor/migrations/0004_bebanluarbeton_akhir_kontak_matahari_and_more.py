# Generated by Django 4.1.3 on 2023-02-04 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bebankalor", "0003_bebanluardinding_kategori"),
    ]

    operations = [
        migrations.AddField(
            model_name="bebanluarbeton",
            name="akhir_kontak_matahari",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="bebanluarbeton",
            name="awal_kontak_matahari",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="bebanluarbeton",
            name="temp_rerata_ruang_berdekatan",
            field=models.FloatField(default=0, max_length=5),
        ),
    ]
