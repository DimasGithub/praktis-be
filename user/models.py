import uuid
from django.db import models
from core.models_helper.timestamp import Timestamp
from django.utils.translation import gettext_lazy as _

class UserType(models.TextChoices):
    REGULAR = 'REGULAR', _('REGULAR')
    VIP = 'VIP', _('VIP')
    WHOLESALE ='WHOLESALE', _('WHOLESALE')

class User(Timestamp):
    uuid = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 150)
    type = models.CharField(max_length = 150, default=UserType.REGULAR, choices=UserType.choices)

    @property
    def get_spent(self):
        from transaction.models import Transaction
        from django.db.models import Sum

        total_price = Transaction.objects.filter(deleted_at__isnull=True, user=self.uuid).aggregate(Sum('total_price'))['total_price__sum']
        if total_price is None:return 0
        return total_price

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        ordering =  ['-created_at']
        verbose_name_plural = 'Users'