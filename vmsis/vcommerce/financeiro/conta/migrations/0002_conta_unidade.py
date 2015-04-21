# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unidade', '__first__'),
        ('conta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conta',
            name='unidade',
            field=models.ForeignKey(to='unidade.Unidade', null=True, verbose_name='Unidade', blank=True),
            preserve_default=True,
        ),
    ]
