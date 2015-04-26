# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '__first__'),
        ('banco', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banco',
            name='id',
        ),
        migrations.AddField(
            model_name='banco',
            name='master_empresa_ptr',
            field=models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='control.Master_empresa', default=2, serialize=False),
            preserve_default=False,
        ),
    ]
