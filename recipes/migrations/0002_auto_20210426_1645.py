# Generated by Django 3.1.4 on 2021-04-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='lgccj', verbose_name='слаг тэга'),
        ),
    ]