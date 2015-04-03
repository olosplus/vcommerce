# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('funcionario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='dtcadastro',
            field=models.DateField(default=datetime.datetime(2015, 3, 19, 2, 45, 5, 319233, tzinfo=utc), verbose_name='Data de cadastro', auto_now_add=True),
            preserve_default=False,
        ),
    ]
