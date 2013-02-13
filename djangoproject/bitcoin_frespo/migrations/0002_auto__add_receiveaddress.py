# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReceiveAddress'
        db.create_table('bitcoin_frespo_receiveaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('bitcoin_frespo', ['ReceiveAddress'])


    def backwards(self, orm):
        # Deleting model 'ReceiveAddress'
        db.delete_table('bitcoin_frespo_receiveaddress')


    models = {
        'bitcoin_frespo.receiveaddress': {
            'Meta': {'object_name': 'ReceiveAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['bitcoin_frespo']