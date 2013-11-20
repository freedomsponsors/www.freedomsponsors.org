from django.db import models
import json
from django.utils import timezone

__author__ = 'tony'


class Rates(models.Model):
    blockchain_data = models.TextField(null=False)
    last_update_blockchain = models.DateTimeField(null=False)
    oer_data = models.TextField(null=False)
    last_update_oer = models.DateTimeField(null=False)

    def usd2brl(self):
        dict = json.loads(self.oer_data)
        return dict['rates']['BRL'] / dict['rates']['USD']

    def btc2(self, to):
        dict = json.loads(self.blockchain_data)
        return dict[to]['sell']

    def _2btc(self, fron):
        dict = json.loads(self.blockchain_data)
        return 1 / dict[fron]['buy']

    @classmethod
    def create_empty(cls):
        r = cls()
        r.oer_data = ''
        r.blockchain_data = ''
        r.last_update_blockchain = timezone.now()
        r.last_update_oer = timezone.now()
        r.save()
        return r

    @classmethod
    def is_valid_blockchain_data(cls, data):
        try:
            dict = json.loads(data)
            x = dict['USD']['sell']
            return x > 0
        except:
            return False

    @classmethod
    def is_valid_oer_data(cls, data):
        try:
            dict = json.loads(data)
            x = dict['rates']['BRL']
            return x > 0
        except:
            return False
