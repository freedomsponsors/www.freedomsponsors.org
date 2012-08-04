# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserInfo'
        db.create_table('core_userinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('paypalEmail', self.gf('django.db.models.fields.EmailField')(max_length=256)),
            ('screenName', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('realName', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('receiveAllEmail', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('brazilianPaypal', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['UserInfo'])

        # Adding model 'Project'
        db.create_table('core_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('createdByUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('homeURL', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('trackerURL', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Project'])

        # Adding model 'Issue'
        db.create_table('core_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'], null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('createdByUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('trackerURL', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Issue'])

        # Adding model 'IssueComment'
        db.create_table('core_issuecomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Issue'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['IssueComment'])

        # Adding model 'IssueCommentHistEvent'
        db.create_table('core_issuecommenthistevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.IssueComment'])),
            ('eventDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('core', ['IssueCommentHistEvent'])

        # Adding model 'Offer'
        db.create_table('core_offer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Issue'])),
            ('sponsor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('lastChangeDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('acceptanceCriteria', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('core', ['Offer'])

        # Adding model 'OfferHistEvent'
        db.create_table('core_offerhistevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Offer'])),
            ('eventDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('acceptanceCriteria', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('core', ['OfferHistEvent'])

        # Adding model 'OfferComment'
        db.create_table('core_offercomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Offer'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core', ['OfferComment'])

        # Adding model 'OfferCommentHistEvent'
        db.create_table('core_offercommenthistevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.OfferComment'])),
            ('eventDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('core', ['OfferCommentHistEvent'])

        # Adding model 'Solution'
        db.create_table('core_solution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Issue'])),
            ('programmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('lastChangeDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('core', ['Solution'])

        # Adding model 'SolutionHistEvent'
        db.create_table('core_solutionhistevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Solution'])),
            ('eventDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('core', ['SolutionHistEvent'])

        # Adding model 'Payment'
        db.create_table('core_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Offer'])),
            ('creationDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('lastChangeDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('paykey', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('confirm_key', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('fee', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('core', ['Payment'])

        # Adding model 'PaymentHistEvent'
        db.create_table('core_paymenthistevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Payment'])),
            ('eventDate', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('core', ['PaymentHistEvent'])

        # Adding model 'PaymentPart'
        db.create_table('core_paymentpart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Payment'])),
            ('programmer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('realprice', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal('core', ['PaymentPart'])


    def backwards(self, orm):
        # Deleting model 'UserInfo'
        db.delete_table('core_userinfo')

        # Deleting model 'Project'
        db.delete_table('core_project')

        # Deleting model 'Issue'
        db.delete_table('core_issue')

        # Deleting model 'IssueComment'
        db.delete_table('core_issuecomment')

        # Deleting model 'IssueCommentHistEvent'
        db.delete_table('core_issuecommenthistevent')

        # Deleting model 'Offer'
        db.delete_table('core_offer')

        # Deleting model 'OfferHistEvent'
        db.delete_table('core_offerhistevent')

        # Deleting model 'OfferComment'
        db.delete_table('core_offercomment')

        # Deleting model 'OfferCommentHistEvent'
        db.delete_table('core_offercommenthistevent')

        # Deleting model 'Solution'
        db.delete_table('core_solution')

        # Deleting model 'SolutionHistEvent'
        db.delete_table('core_solutionhistevent')

        # Deleting model 'Payment'
        db.delete_table('core_payment')

        # Deleting model 'PaymentHistEvent'
        db.delete_table('core_paymenthistevent')

        # Deleting model 'PaymentPart'
        db.delete_table('core_paymentpart')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.issue': {
            'Meta': {'object_name': 'Issue'},
            'createdByUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'trackerURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.issuecomment': {
            'Meta': {'object_name': 'IssueComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Issue']"})
        },
        'core.issuecommenthistevent': {
            'Meta': {'object_name': 'IssueCommentHistEvent'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.IssueComment']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.offer': {
            'Meta': {'object_name': 'Offer'},
            'acceptanceCriteria': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Issue']"}),
            'lastChangeDate': ('django.db.models.fields.DateTimeField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'core.offercomment': {
            'Meta': {'object_name': 'OfferComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Offer']"})
        },
        'core.offercommenthistevent': {
            'Meta': {'object_name': 'OfferCommentHistEvent'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.OfferComment']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.offerhistevent': {
            'Meta': {'object_name': 'OfferHistEvent'},
            'acceptanceCriteria': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Offer']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'core.payment': {
            'Meta': {'object_name': 'Payment'},
            'confirm_key': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'fee': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastChangeDate': ('django.db.models.fields.DateTimeField', [], {}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Offer']"}),
            'paykey': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'})
        },
        'core.paymenthistevent': {
            'Meta': {'object_name': 'PaymentHistEvent'},
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Payment']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'core.paymentpart': {
            'Meta': {'object_name': 'PaymentPart'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Payment']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'realprice': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'})
        },
        'core.project': {
            'Meta': {'object_name': 'Project'},
            'createdByUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'homeURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'trackerURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.solution': {
            'Meta': {'object_name': 'Solution'},
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Issue']"}),
            'lastChangeDate': ('django.db.models.fields.DateTimeField', [], {}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'core.solutionhistevent': {
            'Meta': {'object_name': 'SolutionHistEvent'},
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Solution']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'core.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'brazilianPaypal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paypalEmail': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'realName': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'receiveAllEmail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'screenName': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']