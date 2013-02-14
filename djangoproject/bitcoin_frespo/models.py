from django.db import models
from django.utils import timezone

class ReceiveAddress(models.Model):
    address = models.CharField(max_length=128, blank=True)
    available = models.BooleanField(default=True)

    @classmethod
    def newAddress(cls, address):
        receive_address = cls()
        receive_address.address = address
        receive_address.available = True
        return receive_address

    def use(self):
        self.available = False
        self.save()

class MoneySent(models.Model):
    from_address = models.CharField(max_length=128)
    to_address = models.CharField(max_length=128)
    value = models.DecimalField(max_digits=16, decimal_places=8)
    transaction_hash = models.CharField(max_length=128, null=True)
    status = models.CharField(max_length=30)
    creationDate = models.DateTimeField()
    lastChangeDate = models.DateTimeField()

    CREATED = 'CREATED'
    SENT = 'SENT'
    CONFIRMED_IPN = 'CONFIRMED_IPN'
    CONFIRMED_TRN = 'CONFIRMED_TRN'

    @classmethod
    def newMoneySent(cls, from_address, to_address, value):
        money_sent = cls()
        money_sent.from_address = from_address
        money_sent.to_address = to_address
        money_sent.value = value
        money_sent.status = MoneySent.CREATED
        money_sent.creationDate = timezone.now()
        money_sent.lastChangeDate = money_sent.creationDate
        return money_sent

    def touch(self):
        self.lastChangeDate = timezone.now()

    def sent(self, transaction_hash):
        self.status = MoneySent.SENT
        self.transaction_hash = transaction_hash
        self.touch()
        self.save()