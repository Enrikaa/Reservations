# Generated by Django 3.1.7 on 2021-08-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingroom',
            name='room_number',
            field=models.CharField(max_length=16),
        ),
    ]
