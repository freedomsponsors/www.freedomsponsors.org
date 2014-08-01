# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Issue.trackerURL_noprotocol'
        db.alter_column(u'core_issue', 'trackerURL_noprotocol', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True))

    def backwards(self, orm):

        # Changing field 'Issue.trackerURL_noprotocol'
        db.alter_column(u'core_issue', 'trackerURL_noprotocol', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bitcoin_frespo.moneysent': {
            'Meta': {'object_name': 'MoneySent'},
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'from_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastChangeDate': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'to_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'transaction_hash': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '8'})
        },
        u'bitcoin_frespo.receiveaddress': {
            'Meta': {'object_name': 'ReceiveAddress'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.actionlog': {
            'Meta': {'object_name': 'ActionLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Issue']", 'null': 'True'}),
            'issue_comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.IssueComment']", 'null': 'True'}),
            'new_json': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Offer']", 'null': 'True'}),
            'old_json': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Payment']", 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True'}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Solution']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'core.issue': {
            'Meta': {'object_name': 'Issue'},
            'createdByUser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_feedback': ('django.db.models.fields.BooleanField', [], {}),
            'is_sponsored': ('django.db.models.fields.BooleanField', [], {}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'trackerURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'trackerURL_noprotocol': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updatedDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.issuecomment': {
            'Meta': {'object_name': 'IssueComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Issue']"})
        },
        u'core.issuecommenthistevent': {
            'Meta': {'object_name': 'IssueCommentHistEvent'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.IssueComment']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.offer': {
            'Meta': {'object_name': 'Offer'},
            'acceptanceCriteria': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'expirationDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Issue']"}),
            'lastChangeDate': ('django.db.models.fields.DateTimeField', [], {}),
            'no_forking': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '8'}),
            'require_release': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sponsor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'core.offercomment': {
            'Meta': {'object_name': 'OfferComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Offer']"})
        },
        u'core.offercommenthistevent': {
            'Meta': {'object_name': 'OfferCommentHistEvent'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.OfferComment']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.payment': {
            'Meta': {'object_name': 'Payment'},
            'bitcoin_fee': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8'}),
            'bitcoin_receive_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bitcoin_frespo.ReceiveAddress']", 'null': 'True'}),
            'bitcoin_transaction_hash': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'confirm_key': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'fee': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastChangeDate': ('django.db.models.fields.DateTimeField', [], {}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Offer']"}),
            'offer2payment_suggested_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8'}),
            'offer_currency': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'paykey': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '8'}),
            'total_bitcoin_received': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8'}),
            'usd2payment_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '8'})
        },
        u'core.paymenthistevent': {
            'Meta': {'object_name': 'PaymentHistEvent'},
            'event': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eventDate': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Payment']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'core.paymentpart': {
            'Meta': {'object_name': 'PaymentPart'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money_sent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bitcoin_frespo.MoneySent']", 'null': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Payment']"}),
            'paypalEmail': ('django.db.models.fields.EmailField', [], {'max_length': '256', 'null': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '8'}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Solution']"})
        },
        u'core.project': {
            'Meta': {'object_name': 'Project'},
            'createdByUser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'homeURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image3x1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'redirectto_project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True'}),
            'trackerURL': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.solution': {
            'Meta': {'object_name': 'Solution'},
            'accepting_payments': ('django.db.models.fields.BooleanField', [], {}),
            'creationDate': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Issue']"}),
            'lastChangeDate': ('django.db.models.fields.DateTimeField', [], {}),
            'programmer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'core.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'objid': ('django.db.models.fields.IntegerField', [], {}),
            'objtype': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'core.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bitcoin_receive_address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'brazilianPaypal': ('django.db.models.fields.BooleanField', [], {}),
            'hide_from_userlist': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_paypal_email_verified': ('django.db.models.fields.BooleanField', [], {}),
            'is_primary_email_verified': ('django.db.models.fields.BooleanField', [], {}),
            'paypalEmail': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'paypal_verified': ('django.db.models.fields.BooleanField', [], {}),
            'preferred_language_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'realName': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'receiveAllEmail': ('django.db.models.fields.BooleanField', [], {}),
            'receiveEmail_announcements': ('django.db.models.fields.BooleanField', [], {}),
            'receiveEmail_issue_comments': ('django.db.models.fields.BooleanField', [], {}),
            'receiveEmail_issue_offer': ('django.db.models.fields.BooleanField', [], {}),
            'receiveEmail_issue_payment': ('django.db.models.fields.BooleanField', [], {}),
            'receiveEmail_issue_work': ('django.db.models.fields.BooleanField', [], {}),
            'screenName': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'core.watch': {
            'Meta': {'object_name': 'Watch'},
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Issue']", 'null': 'True'}),
            'objid': ('django.db.models.fields.IntegerField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['core']