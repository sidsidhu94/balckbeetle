from django.db import models
from user.models import User
from adminside.models import Premium
from django.utils import timezone

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)  
    payment_id = models.CharField(max_length=255, verbose_name="Payment ID")
    order_id = models.CharField(max_length=255, verbose_name="Order ID")
    signature = models.CharField(max_length=255, verbose_name="Signature", blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    premium_selected =  models.ForeignKey(Premium,on_delete=models.CASCADE,null=True)

    def _str_(self):
        return f"Payment #{self.id} for premium #{self.Premium_id}"