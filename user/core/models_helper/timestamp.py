from django.db import models
class Timestamp(models.Model):
    created_at = models.DateField(auto_now=False, auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, auto_now_add=False, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        abstract = True