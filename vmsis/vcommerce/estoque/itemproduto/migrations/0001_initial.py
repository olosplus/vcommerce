# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '__first__'),
        ('almoxarifado', '__first__'),
        ('item', '0002_item_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Itemproduto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('qtdeprod', models.FloatField(verbose_name='Quantidade')),
                ('almoxarifado', models.ForeignKey(to='almoxarifado.Almoxarifado', verbose_name='Almoxarifado')),
                ('master', models.ForeignKey(to='estoque.Movimentacaoest')),
                ('produto', models.ForeignKey(to='item.Item', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Item',
                'db_table': 'itemproduto',
                'verbose_name_plural': 'Itens',
            },
            bases=(models.Model,),
        ),
    ]
