# Generated by Django 2.2.5 on 2019-10-30 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='schoolid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='program',
            name='subjectid',
            field=models.IntegerField(default=0),
        ),
    ]
