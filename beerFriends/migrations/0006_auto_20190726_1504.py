# Generated by Django 2.2.3 on 2019-07-26 15:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beerFriends', '0005_auto_20190726_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beer',
            name='rating',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
