from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=256)
    quantity = models.IntegerField()

    def __str__(self):
        return "{} units of {}".format(self.quantity, self.name)
