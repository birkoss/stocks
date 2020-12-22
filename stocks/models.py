from django.db import models

from core.models import TimeStampedModel, UUIDModel


class Stock(TimeStampedModel, UUIDModel, models.Model):
    symbol = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=200, default="")
    code = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name + " (" + self.code + ")"


class Share(TimeStampedModel, UUIDModel, models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        null=False
    )

    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        null=False
    )

    amount = models.FloatField(default=0)
    value = models.FloatField(default=0)

class StockValue(TimeStampedModel, UUIDModel, models.Model):
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        null=False
    )

    value = models.FloatField(default=0)