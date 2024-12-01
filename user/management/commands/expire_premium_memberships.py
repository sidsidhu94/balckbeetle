from django.core.management.base import BaseCommand
from user.models import User  
from datetime import date

class Command(BaseCommand):
    help = 'Expire premium memberships that have passed their validity date'

    def handle(self, *args, **kwargs):
        
        users_to_expire = User.objects.filter(is_premium_member=True, premium_validity__lt=date.today())
        
        
        for user in users_to_expire:
            user.is_premium_member = False
            user.premium_validity = None
            user.premium_details = None
            user.save()
        
        self.stdout.write(self.style.SUCCESS(f'Expired {users_to_expire.count()} premium memberships.'))
