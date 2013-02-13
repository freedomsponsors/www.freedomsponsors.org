from django.db import models

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