# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('cdbanco', models.CharField(blank=True, verbose_name='Codigo', max_length=30)),
                ('nmbanco', models.CharField(verbose_name='Banco', max_length=200)),
                ('cnpjbanco', models.CharField(verbose_name='CNPJ', max_length=16)),
            ],
            options={
                'verbose_name': 'Banco',
                'db_table': 'banco',
                'verbose_name_plural': 'Bancos',
            },
            bases=(models.Model,),
        ),
    ]
