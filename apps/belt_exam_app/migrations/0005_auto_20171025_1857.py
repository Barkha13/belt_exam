# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-25 18:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam_app', '0004_quote_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='quote',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='user',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]