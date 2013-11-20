# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Rates.last_update'
        db.delete_column('frespo_currencies_rates', 'last_update')

        # Adding field 'Rates.last_update_blockchain'
        db.add_column('frespo_currencies_rates', 'last_update_blockchain',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 19, 0, 0)),
                      keep_default=False)

        # Adding field 'Rates.oer_data'
        db.add_column('frespo_currencies_rates', 'oer_data',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Rates.last_update_oer'
        db.add_column('frespo_currencies_rates', 'last_update_oer',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 19, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Rates.last_update'
        raise RuntimeError("Cannot reverse this migration. 'Rates.last_update' and its values cannot be restored.")
        # Deleting field 'Rates.last_update_blockchain'
        db.delete_column('frespo_currencies_rates', 'last_update_blockchain')

        # Deleting field 'Rates.oer_data'
        db.delete_column('frespo_currencies_rates', 'oer_data')

        # Deleting field 'Rates.last_update_oer'
        db.delete_column('frespo_currencies_rates', 'last_update_oer')


    models = {
        'frespo_currencies.rates': {
            'Meta': {'object_name': 'Rates'},
            'blockchain_data': ('django.db.models.fields.TextField', [], {}),
            'google_data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update_blockchain': ('django.db.models.fields.DateTimeField', [], {}),
            'last_update_oer': ('django.db.models.fields.DateTimeField', [], {}),
            'oer_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['frespo_currencies']