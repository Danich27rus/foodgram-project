# Generated by Django 3.1.4 on 2021-04-27 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='ssfnn', verbose_name='слаг тэга'),
        ),
    ]
