# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relay', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='torch',
            options={'ordering': ('relay', 'ring', 'pos'), 'verbose_name_plural': 'torches'},
        ),
        migrations.AlterOrderWithRespectTo(
            name='torch',
            order_with_respect_to=None,
        ),
    ]
