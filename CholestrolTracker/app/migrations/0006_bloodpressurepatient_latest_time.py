# Generated by Django 3.0.6 on 2020-06-18 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200612_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodpressurepatient',
            name='latest_time',
            field=models.CharField(default='', max_length=300),
        ),
    ]