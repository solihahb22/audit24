# Generated by Django 4.1.3 on 2023-02-15 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bebankalor", "0005_bebanluarbeton_arah"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bebandalampenghuni",
            name="lama_aktivitas",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="bebandalampenghuni",
            name="total_aktivitas",
            field=models.IntegerField(),
        ),
    ]
