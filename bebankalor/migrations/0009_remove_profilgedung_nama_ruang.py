# Generated by Django 4.1.3 on 2023-02-24 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bebankalor", "0008_profilgedung_nama_ruang_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profilgedung",
            name="nama_ruang",
        ),
    ]
