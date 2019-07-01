# Generated by Django 2.1.7 on 2019-06-05 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.URLField()),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('link_to', models.URLField()),
                ('priority', models.IntegerField()),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-pub_time']},
        ),
        migrations.AlterField(
            model_name='comment',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.News'),
        ),
    ]
