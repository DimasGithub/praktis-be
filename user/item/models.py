import uuid
from django.db import models
from core.models_helper.timestamp import Timestamp
from django.utils.translation import gettext_lazy as _
from user.models import UserType

class ItemType(models.TextChoices):
    hats = 'hats', _('hats')
    tops = 'tops', _('tops')
    shorts ='shorts', _('shorts')

class Item(Timestamp):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 150)
    type = models.CharField(max_length = 150, default=ItemType.hats, choices=ItemType.choices)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'item'
        verbose_name = 'Item'
        ordering =  ['-created_at']
        verbose_name_plural = 'Items'

class ItemPrice(models.Model):
    pricefor = models.CharField(max_length=150, choices=UserType.choices, default=UserType.REGULAR)
    price = models.BigIntegerField(default=0)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_price')  
    
    def __str__(self):
        return f"{self.item} - {self.price} ({self.pricefor})"
