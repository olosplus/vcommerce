# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vatualiza',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('resumo', models.CharField(max_length=100, verbose_name='Resumo')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('versao', models.CharField(max_length=20, verbose_name='Versão')),
                ('dtatualiza', models.DateField(verbose_name='Data de atualização')),
            ],
            options={
                'db_table': 'vatualiza',
                'verbose_name': 'Atualização',
                'verbose_name_plural': 'Atualizações',
            },
            bases=(models.Model,),
        ),
    ]
