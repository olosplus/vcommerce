# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nragencia', models.CharField(verbose_name='Agencia', max_length=30)),
                ('nrconta', models.CharField(verbose_name='Numero', max_length=30)),
                ('vlsaldo', models.FloatField(verbose_name='Saldo')),
                ('banco', models.ForeignKey(to='banco.Banco', verbose_name='Banco')),
            ],
            options={
                'verbose_name': 'Conta',
                'db_table': 'conta',
                'verbose_name_plural': 'Contas',
            },
            bases=(models.Model,),
        ),
    ]
