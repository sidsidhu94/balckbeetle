from django.db import models
from django.utils import timezone

##################################################
#################### AI MODEL ####################
##################################################

class Trade(models.Model):
    SEGMENT_CHOICES = [
        ('EQUITY', 'Equity'),
        ('FUTURES', 'Futures'),
        ('OPTIONS', 'Options'),
        ('COMMODITY', 'Commodity'),
        ('FOREX', 'Forex'),
    ]
    TYPE_CHOICES = [
        ('INTRADAY', 'Intraday'),
        ('BTST', 'BTST'),
        ('SHORT_TERM', 'Short Term'),
        ('POSITIONAL', 'Positional'),
        ('LONG_TERM', 'Long Term'),
    ]
    stock_index = models.CharField(max_length=255, null=False)
    company_name = models.CharField(max_length= 255,null= False)
    segment = models.CharField(max_length=255, null=False,choices=SEGMENT_CHOICES)
    expiry_date = models.DateField(null=True, blank=True)
    trade_type = models.CharField(max_length=255, null=False,choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.stock_index 
    
    @classmethod
    def count_trades_daily(cls):
        today = timezone.now().date()
        return cls.objects.filter(created_at__date=today).count()

    @classmethod
    def count_trades_monthly(cls):
        today = timezone.now()
        start_of_month = today.replace(day=1)
        return cls.objects.filter(created_at__gte=start_of_month).count()
    
    @classmethod
    def get_expired_trades(cls):
        return cls.objects.filter(expiry_date__lt=timezone.now().date()).count()

class TradeHistory(models.Model):
    trade = models.ForeignKey(Trade,on_delete=models.CASCADE,related_name='history')
    buy = models.DecimalField(max_digits=10, decimal_places=2)
    target = models.DecimalField(max_digits=10, decimal_places=2)
    sl = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Stop Loss")
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.trade} - {self.changed_at}'
    
class Analysis(models.Model):
    
    STATUS_CHOICES = [
        ('BEARISH', 'Bearish'),
        ('BULLISH', 'Bullish'),
        ('NEUTRAL', ' Neutral'),
        
    ]
    trade = models.ForeignKey(Trade,on_delete=models.CASCADE,related_name='analysis')
    bull_scenario = models.CharField(max_length=1000, null=False)
    bear_scenario = models.CharField(max_length=1000, null=False)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)

class Insight(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name="insights")
    prediction = models.CharField(max_length=255,default= "Not updated")
    actual = models.CharField(max_length=255,default= "Not updated")

####################################################
################### AI MODEL END ###################
####################################################


######################################################
##############TO HANDLE PREMIUM DETAILS ##############
######################################################



class Premium(models.Model):
    PREMIUM_PERIOD_CHOICES = [
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly'),
    ]
    
    premium_amount = models.IntegerField()
    premium_period = models.CharField(
        max_length=255, 
        choices=PREMIUM_PERIOD_CHOICES, 
        null=False
    )

    def __str__(self):
        return f"{self.premium_amount} - {self.premium_period}"

    def get_premium_duration(self):
        """Returns the duration in months based on the premium period."""
        if self.premium_period == 'quarterly':
            return 3
        elif self.premium_period == 'monthly':
            return 1
        return None




######################################################
############TO HANDLE PREMIUM DETAILS END ############
######################################################


class Orders(models.Model):
    pass 

