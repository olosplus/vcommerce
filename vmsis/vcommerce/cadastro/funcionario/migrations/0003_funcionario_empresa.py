# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '__first__'),
        ('funcionario', '0002_funcionario_dtcadastro'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='empresa',
            field=models.ForeignKey(to='empresa.Empresa', null=True, blank=True, verbose_name='Empresa'),
            preserve_default=True,
        ),
    ]
