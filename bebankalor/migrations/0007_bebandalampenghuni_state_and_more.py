# Generated by Django 4.1.3 on 2023-02-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bebankalor", "0006_alter_bebandalampenghuni_lama_aktivitas_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bebandalampenghuni",
            name="state",
            field=models.CharField(default="tidak merokok", max_length=50),
        ),
        migrations.AddField(
            model_name="bebaninfiltrasiventilasi",
            name="jenis_ceiling",
            field=models.CharField(default="ceiling drop", max_length=20),
        ),
        migrations.AddField(
            model_name="bebanluarpintu",
            name="frame",
            field=models.CharField(default="door frame wood caulked", max_length=50),
        ),
    ]
