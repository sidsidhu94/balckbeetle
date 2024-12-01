from django.db import models
import random
import string

class Institute(models.Model):
    name = models.CharField(max_length=100,null=False)
    code = models.CharField(max_length=10, unique=True, null= False)


    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

  
    def __str__(self):
        return self.name
  
    """
    the code given below is to enter the institute code automatically by the admin when admin enter the institute  
    """ 
    # def save(self, *args, **kwargs):
    #     if not self.code:
    #         self.code = self.generate_code()
    #     super().save(*args, **kwargs)

    # def generate_code(self):
    #     base_code = self.name[:3].upper()
    #     counter = 1
    #     unique_code = base_code
    #     while Institute.objects.filter(code=unique_code).exists():
    #         unique_code = f"{base_code}{counter}"
    #         counter += 1
    #     return unique_code


class Batch(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='batches')
    batch_name = models.CharField(max_length=50)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        """
        Generate a unique referral code for each batch of the same institute
        """
        
        base_code = f"{self.institute.code}-{self.batch_name.upper().replace(' ', '')}"
        unique_code = base_code

        """
        Append a random 4-character string to ensure uniqueness (or use a sequence number if preferred)
        """
        
        while Batch.objects.filter(referral_code=unique_code).exists():
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            unique_code = f"{base_code}-{random_suffix}"
        return unique_code

    def __str__(self):
        return f"{self.institute.name} - {self.batch_name}"
