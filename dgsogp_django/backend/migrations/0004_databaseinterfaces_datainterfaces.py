# Generated by Django 3.0.3 on 2020-03-10 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_datasources_hadoopsources_metadata_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Databaseinterfaces',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('wserver', models.CharField(max_length=255)),
                ('wport', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('datasource_id', models.IntegerField()),
            ],
            options={
                'db_table': 'databaseinterfaces',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Datainterfaces',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('metadata_id', models.IntegerField()),
            ],
            options={
                'db_table': 'datainterfaces',
                'managed': False,
            },
        ),
    ]