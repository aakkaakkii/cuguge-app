# Generated by Django 3.1.1 on 2020-09-04 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200903_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.postimage'),
        ),
    ]
