from django.db import models
from django.utils import timezone

# Create your models here.
class I(models.Model):
    item_code = models.CharField(max_length=20)
    item_name = models.CharField(max_length=100,null=False,blank=False)
    item_count = models.IntegerField(default=1)

class O(models.Model):
    order_number = models.IntegerField()
    code_name = models.ForeignKey(I, on_delete=models.CASCADE)
    order_date = models.DateField(default=timezone.now)
    quantity = models.IntegerField(default=1)

