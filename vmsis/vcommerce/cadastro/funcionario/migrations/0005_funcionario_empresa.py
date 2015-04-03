# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '__first__'),
        ('funcionario', '0004_auto_20150328_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='empresa',
            field=models.ForeignKey(verbose_name='Empresa', null=True, to='empresa.Empresa'),
            preserve_default=True,
        ),
    ]
