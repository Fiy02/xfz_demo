# Generated by Django 2.1.7 on 2019-06-06 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20190605_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='priority',
            field=models.IntegerField(unique=True),
        ),
    ]
