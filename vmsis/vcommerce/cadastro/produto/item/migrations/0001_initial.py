# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unimedida', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nmproduto', models.CharField(max_length=200, verbose_name='Nome', blank=True)),
                ('posarvore', models.CharField(max_length=40, verbose_name='Arvore')),
                ('fatorconv', models.FloatField(verbose_name='Fator de conversão')),
                ('cdbarra', models.CharField(max_length=100, verbose_name='Código de barras', blank=True)),
                ('prodcmp', models.OneToOneField(related_name='Produto_prodcmp', to='item.Item', verbose_name='Produto de compra')),
                ('prodest', models.OneToOneField(related_name='Produto_prodest', to='item.Item', verbose_name='Produto de estoque')),
                ('unimedida', models.ForeignKey(to='unimedida.Unimedida', verbose_name='Unidade de medida')),
            ],
            options={
                'db_table': 'produto',
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
            bases=(models.Model,),
        ),
    ]
