# Generated by Django 3.1.1 on 2020-09-17 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200904_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
    ]