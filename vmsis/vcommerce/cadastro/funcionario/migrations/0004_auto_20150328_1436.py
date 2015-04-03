# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unidade', '__first__'),
        ('funcionario', '0003_funcionario_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='empresa',
        ),
        migrations.AddField(
            model_name='funcionario',
            name='unidade',
            field=models.ForeignKey(to='unidade.Unidade', verbose_name='Unidade', blank=True, null=True),
            preserve_default=True,
        ),
    ]
