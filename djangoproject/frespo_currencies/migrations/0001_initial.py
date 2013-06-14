# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rates'
        db.create_table('frespo_currencies_rates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')()),
            ('google_data', self.gf('django.db.models.fields.TextField')()),
            ('blockchain_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('frespo_currencies', ['Rates'])


    def backwards(self, orm):
        # Deleting model 'Rates'
        db.delete_table('frespo_currencies_rates')


    models = {
        'frespo_currencies.rates': {
            'Meta': {'object_name': 'Rates'},
            'blockchain_data': ('django.db.models.fields.TextField', [], {}),
            'google_data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['frespo_currencies']