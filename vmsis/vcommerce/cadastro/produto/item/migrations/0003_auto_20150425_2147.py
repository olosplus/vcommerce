# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_item_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='prodcmp',
        ),
        migrations.RemoveField(
            model_name='item',
            name='prodest',
        ),
    ]
