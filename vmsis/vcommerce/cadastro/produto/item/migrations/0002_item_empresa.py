# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '__first__'),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='empresa',
            field=models.ForeignKey(verbose_name='Empresa', null=True, to='empresa.Empresa'),
            preserve_default=True,
        ),
    ]
