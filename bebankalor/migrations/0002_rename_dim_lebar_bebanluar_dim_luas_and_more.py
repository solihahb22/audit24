# Generated by Django 4.1.3 on 2023-01-27 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bebankalor", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bebanluar",
            old_name="dim_lebar",
            new_name="dim_luas",
        ),
        migrations.RenameField(
            model_name="bebanluarceiling",
            old_name="dim_lebar",
            new_name="dim_luas",
        ),
        migrations.RemoveField(
            model_name="bebanluar",
            name="dim_panjang",
        ),
        migrations.RemoveField(
            model_name="bebanluarceiling",
            name="dim_panjang",
        ),
        migrations.RemoveField(
            model_name="bebanluardinding",
            name="dim_lebar",
        ),
        migrations.RemoveField(
            model_name="bebanluardinding",
            name="dim_panjang",
        ),
        migrations.RemoveField(
            model_name="bebanluarkaca",
            name="dim_lebar",
        ),
        migrations.RemoveField(
            model_name="bebanluarkaca",
            name="dim_panjang",
        ),
        migrations.RemoveField(
            model_name="bebanluarpintu",
            name="dim_lebar",
        ),
        migrations.RemoveField(
            model_name="bebanluarpintu",
            name="dim_panjang",
        ),
        migrations.AddField(
            model_name="bebanluarbeton",
            name="dim_luas",
            field=models.FloatField(default=0, max_length=5),
        ),
        migrations.AddField(
            model_name="bebanluardinding",
            name="dim_luas",
            field=models.FloatField(default=0, max_length=5),
        ),
        migrations.AddField(
            model_name="bebanluarkaca",
            name="dim_luas",
            field=models.FloatField(default=0, max_length=5),
        ),
        migrations.AddField(
            model_name="bebanluarpintu",
            name="dim_luas",
            field=models.FloatField(default=0, max_length=5),
        ),
    ]
