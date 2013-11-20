# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Rates.google_data'
        db.delete_column('frespo_currencies_rates', 'google_data')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Rates.google_data'
        raise RuntimeError("Cannot reverse this migration. 'Rates.google_data' and its values cannot be restored.")

    models = {
        'frespo_currencies.rates': {
            'Meta': {'object_name': 'Rates'},
            'blockchain_data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update_blockchain': ('django.db.models.fields.DateTimeField', [], {}),
            'last_update_oer': ('django.db.models.fields.DateTimeField', [], {}),
            'oer_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['frespo_currencies']