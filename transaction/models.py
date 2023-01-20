import uuid
from django.db import models
from django.db.models import Sum
from core.models_helper.timestamp import Timestamp
from item.models import Item, ItemPrice
from user.models import User, UserType

class Transaction(Timestamp):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    qty = models.BigIntegerField(default=0)
    total_price = models.BigIntegerField(default=0)
    item  = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items')
    
    class Meta:
        db_table = 'transaction'
        verbose_name = 'Transaction'
        ordering =  ['-created_at']
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return str(self.uuid)

    def save(self,*args, **kwargs) -> None:
        try:
            item_prices = self.item.item_price.get(pricefor__iexact=self.user.type)
        
        except ItemPrice.DoesNotExist:
            item_prices = self.item.item_price.get(pricefor__iexact=UserType.REGULAR)

        self.total_price = (self.qty * item_prices.price)
        super(Transaction, self).save(*args, **kwargs)