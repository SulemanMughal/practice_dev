# Generated by Django 2.2.13 on 2020-10-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='title',
            field=models.CharField(default='Post Title', max_length=100, verbose_name='Post Title'),
        ),
    ]
