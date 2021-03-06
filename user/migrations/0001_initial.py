# Generated by Django 2.2.5 on 2019-11-02 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntryLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('login_time', models.DateTimeField()),
                ('logout_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'log',
                'verbose_name_plural': 'logs',
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('school_id', models.IntegerField()),
                ('permission', models.IntegerField()),
            ],
            options={
                'verbose_name': 'permission',
                'verbose_name_plural': 'permissions',
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=11)),
                ('email', models.CharField(default='', max_length=64)),
                ('email_verify', models.CharField(default='', max_length=64)),
                ('realname', models.CharField(default='', max_length=32)),
                ('motto', models.CharField(default='', max_length=256)),
                ('permission', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.IntegerField()),
                ('phone', models.CharField(max_length=11)),
                ('code', models.CharField(max_length=8)),
                ('send_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'verifycode',
                'verbose_name_plural': 'verifycodes',
                'get_latest_by': 'id',
            },
        ),
    ]
