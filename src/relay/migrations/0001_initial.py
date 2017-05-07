# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import relay.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True, editable=False, null=True)),
                ('name', models.CharField(blank=True, unique=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True, editable=False, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('cals_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='relays', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Relay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True, editable=False, null=True)),
                ('name', models.CharField(max_length=40)),
                ('subtype', models.CharField(choices=[('standard', 'Standard'), ('inverse', 'Inverse')], default='standard', max_length=20)),
                ('homepage', models.URLField(blank=True, null=True)),
                ('rules', models.TextField(blank=True, verbose_name='Rules specific to this relay', null=True)),
                ('notes', models.TextField(blank=True, verbose_name='Additional notes', null=True)),
                ('pos', models.IntegerField(default=0, verbose_name='position', unique=True)),
                ('missing', models.BooleanField(default=True)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('relay_master', models.ForeignKey(to='relay.Participant', related_name='relay_mastering')),
            ],
            options={
                'ordering': ['pos'],
            },
        ),
        migrations.CreateModel(
            name='Ring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(default='_', max_length=10)),
                ('slug', models.SlugField(blank=True, default='_', null=True)),
                ('subtype', models.CharField(choices=[('standard', 'Standard'), ('romance', 'Romance')], default='standard', max_length=20)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('num_torches', models.PositiveIntegerField(default=0, verbose_name='Number of torches')),
                ('relay', models.ForeignKey(to='relay.Relay', related_name='rings')),
                ('ring_master', models.ForeignKey(blank=True, to='relay.Participant', related_name='ring_mastering', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Torch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('first', models.BooleanField(default=False)),
                ('last', models.BooleanField(default=False)),
                ('pos', models.IntegerField(default=0, verbose_name='position')),
                ('torch', models.TextField(help_text='The text that was sent to the next participant')),
                ('smooth_translation', models.TextField(blank=True, help_text='Smooth English translation of the torch sent', null=True)),
                ('translation_of_received', models.TextField(blank=True, help_text='Translation of the torch received', null=True)),
                ('mini_dictionary', models.TextField(blank=True, help_text='Mini dictionary covering the expressions, words and affixes in the torch', null=True)),
                ('mini_grammar', models.TextField(blank=True, help_text='Mini grammar covering the phenomena in the torch', null=True)),
                ('abbreviations', models.TextField(blank=True, help_text='Abbreviations', null=True)),
                ('interlinear', models.TextField(db_column='il_text', blank=True, verbose_name='Interlinear', default='', null=True)),
                ('il_xhtml', models.TextField(db_column='il_xhtml', blank=True, verbose_name='Interlinear, formatted', editable=False, default='', null=True)),
                ('il_format', models.CharField(choices=[('monospace', 'WYSIWYG monospace'), ('leipzig', 'Leipzig Glossing Rules')], blank=True, max_length=20, default='monospace', verbose_name='Interlinear format')),
                ('language', models.ForeignKey(to='relay.Language', related_name='torches')),
                ('participant', models.ForeignKey(to='relay.Participant', related_name='torches')),
                ('relay', models.ForeignKey(to='relay.Relay', related_name='torches')),
                ('ring', models.ForeignKey(blank=True, to='relay.Ring', related_name='torches', null=True)),
            ],
            options={
                'verbose_name_plural': 'torches',
            },
        ),
        migrations.CreateModel(
            name='TorchFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('filename', models.FileField(upload_to=relay.models.TorchFile.upload_to)),
                ('category', models.CharField(choices=[('alttorch', 'Alternate version'), ('recording', 'Recording'), ('orthopgraphy', 'Native orthopgraphy'), ('print', 'Printable version'), ('pronunciation-ascii', 'Pronunciation (ASCII)'), ('pronunciation-ipa', 'Pronunciation (IPA)'), ('notes', 'Other notes')], max_length=20)),
                ('mimetype', models.CharField(blank=True, max_length=256, default='application/octet-stream')),
                ('torch', models.ForeignKey(to='relay.Torch', related_name='files')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='language',
            unique_together=set([('name', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='torch',
            unique_together=set([('relay', 'ring', 'pos')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='torch',
            order_with_respect_to='ring',
        ),
        migrations.AlterUniqueTogether(
            name='ring',
            unique_together=set([('relay', 'name')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='ring',
            order_with_respect_to='relay',
        ),
    ]
