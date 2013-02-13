from django.db import models

class ReceiveAddress(models.Model):
    address = models.CharField(max_length=128, blank=True)
    available = models.BooleanField(default=True)

    def use(self):
        self.available = False
        self.save()