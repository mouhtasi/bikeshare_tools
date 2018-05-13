# Generated by Django 2.0.3 on 2018-05-11 05:22

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bikesharestationcatalog', '0002_stationimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='StationAverageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(max_length=10)),
                ('time_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bikesharestationcatalog.Station')),
            ],
        ),
    ]