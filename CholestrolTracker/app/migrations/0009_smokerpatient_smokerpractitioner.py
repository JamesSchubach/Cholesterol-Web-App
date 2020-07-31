# Generated by Django 3.0.7 on 2020-06-18 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200618_0152'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmokerPractitioner',
            fields=[
                ('smoker_prac_id', models.IntegerField(primary_key=True, serialize=False)),
                ('non_smoker_count', models.IntegerField(default=0)),
                ('original_practitioner', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='smoker_original_practitioner', to='app.Practitioner')),
            ],
        ),
        migrations.CreateModel(
            name='SmokerPatient',
            fields=[
                ('smoker_patient_id', models.IntegerField(primary_key=True, serialize=False)),
                ('smoker_status', models.CharField(max_length=100)),
                ('original_patient', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='smoker_original_patient', to='app.Patient')),
            ],
        ),
    ]
