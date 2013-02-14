# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MoneySent'
        db.create_table('bitcoin_frespo_moneysent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('to_address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=8)),
            ('transaction_hash', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('lastChangeDate', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('bitcoin_frespo', ['MoneySent'])


    def backwards(self, orm):
        # Deleting model 'MoneySent'
        db.delete_table('bitcoin_frespo_moneysent')


    models = {
        'bitcoin_frespo.moneysent': {
            'Meta': {'object_name': 'MoneySent'},
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'from_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastChangeDate': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'to_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'transaction_hash': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '8'})
        },
        'bitcoin_frespo.receiveaddress': {
            'Meta': {'object_name': 'ReceiveAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['bitcoin_frespo']