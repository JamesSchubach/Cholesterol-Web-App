# Generated by Django 3.0.6 on 2020-06-18 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_cholesterolpatient_latest_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloodpressurepatient',
            old_name='highlighted',
            new_name='highlighted_dia',
        ),
        migrations.AddField(
            model_name='bloodpressurepatient',
            name='highlighted_sys',
            field=models.BooleanField(default=False),
        ),
    ]
