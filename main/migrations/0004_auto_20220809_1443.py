# Generated by Django 3.0.8 on 2022-08-09 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20220809_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api_6',
            name='pm10Grade1h',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='api_6',
            name='pm10Value24',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='api_6',
            name='pm25Grade1h',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='api_6',
            name='pm25Value24',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
