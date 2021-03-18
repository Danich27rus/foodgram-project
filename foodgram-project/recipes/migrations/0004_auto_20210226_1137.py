# Generated by Django 2.2 on 2021-02-26 11:37

import colorful.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210222_2018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('product',), 'verbose_name': 'Ингредиенты'},
        ),
        migrations.AddField(
            model_name='tag',
            name='color_slug',
            field=models.SlugField(default='Black'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorful.fields.RGBColorField(colors=['#00ff00', '#ff0000', '#ffff00']),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='neery'),
        ),
    ]
