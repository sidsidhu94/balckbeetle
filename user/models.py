from django.utils import timezone
from django.db import models
from datetime import date
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from adminside.models import Premium
from django.db.models import Q

class UserAccountManager(BaseUserManager):
    
    def create_user(self, mobile_number, last_name, first_name, **extra_fields):
        if not mobile_number:
            raise ValueError("The mobile number must be set")
        if not first_name:
            raise ValueError("The first name is required")
        if not last_name:
            raise ValueError("The last name is required")
        
        user = self.model(mobile_number=mobile_number, first_name=first_name, last_name=last_name, **extra_fields)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, mobile_number, first_name, last_name, password=None, **extra_fields):
        if not password:
            raise ValueError("Superusers must have a password.")
        
        user = self.create_user(mobile_number=mobile_number, first_name=first_name, last_name=last_name, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100,null= False,default=None)
    last_name = models.CharField(max_length=100,null= False,default=None)
    mobile_number = models.CharField(max_length=15, unique=True)
    beetle_coin = models.DecimalField(max_digits=10, decimal_places=2, default=300000.00)
    premium_details = models.CharField(blank=True, null=True,max_length=255)
    is_premium_member = models.BooleanField(default=False)
    premium_validity = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  
        blank=True
    )

    objects = UserAccountManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.mobile_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    def is_premium_active(self):
        if self.is_premium_member and self.premium_validity:
            return self.premium_validity >= date.today()
        return False
    
    def is_premium_days_remaining(self):
        if self.is_premium_member and self.premium_validity:
            remaining_days = (self.premium_validity - date.today()).days
            return max(remaining_days, 0)  
        return None
    
    def save(self, *args, **kwargs):
        if not self.password:
            self.set_unusable_password()  
        # if self.is_premium_member and self.premium_validity:
            
        if self.is_premium_member and self.premium_validity:
            # If the premium validity date has passed, expire the membership
            if self.premium_validity < date.today():
                self.is_premium_member = False
                self.premium_validity = None
                self.premium_details = None 

        super(User, self).save(*args, **kwargs)

    @classmethod
    def get_user_counts(cls):
        """Returns the count of quarterly premium members, monthly premium members, and total users."""
        quarterly_members = cls.objects.filter(

            is_premium_member=True, 
            premium_details='Quarterly'
        ).count()
        
        monthly_members = cls.objects.filter(
            is_premium_member=True, 
            premium_details='Monthly'
        ).count()
        
        total_users = cls.objects.filter(is_staff = False).count()

        return {
            'quarterly_members': quarterly_members,
            'monthly_members': monthly_members,
            'total_users': total_users
        }


# class Otp_verify(models.Model):
#     user = 


# class Payment(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     # payment_method = models.CharField(max_length=50)
#     payment_status = models.BooleanField(default=False)  
#     payment_id = models.CharField(max_length=255, verbose_name="Payment ID")
#     order_id = models.CharField(max_length=255, verbose_name="Order ID")
#     signature = models.CharField(max_length=255, verbose_name="Signature", blank=True, null=True)
#     timestamp = models.DateTimeField(default=timezone.now, editable=False)
#     premium_selected =  models.ForeignKey(Premium,on_delete=models.CASCADE,null=True)

#     def _str_(self):
#         return f"Payment #{self.id} for premium #{self.Premium_id}"
    
    
#     @classmethod
#     def get_total_premium_paid(cls):
#         """
#         Get the total premium paid across all users.
#         """
#         total_premium = cls.objects.filter(payment_status=True).aggregate(models.Sum('amount'))['amount__sum']
#         return total_premium if total_premium is not None else 0

#     @classmethod
#     def get_daily_premium(cls):
#         """
#         Get the daily premium paid across all users.
#         """
#         today = timezone.now().date()
#         daily_premium = cls.objects.filter(payment_status=True, timestamp__date=today).aggregate(models.Sum('amount'))['amount__sum']
#         return daily_premium if daily_premium is not None else 0
