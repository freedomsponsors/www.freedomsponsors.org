from django.db import models
import json

__author__ = 'tony'


class Rates(models.Model):
    last_update = models.DateTimeField(null=False)
    google_data = models.TextField(null=False)
    blockchain_data = models.TextField(null=False)

    def usd2brl(self):
        return float(self.google_data.split('rhs:')[1].split(',')[0].split('"')[1].split(' ')[0])

    def btc2(self, to):
        dict = json.loads(self.blockchain_data)
        return dict[to]['sell']

    def _2btc(self, fron):
        dict = json.loads(self.blockchain_data)
        return 1 / dict[fron]['buy']
