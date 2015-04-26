# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '__first__'),
        ('itemproduto', '0002_remove_itemproduto_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemproduto',
            name='movimentacaoest',
            field=models.ForeignKey(to='estoque.Movimentacaoest', null=True),
            preserve_default=True,
        ),
    ]
