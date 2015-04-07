# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vatualiza', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vatualiza',
            name='descricao',
            field=models.TextField(verbose_name='Descrição'),
            preserve_default=True,
        ),
    ]
