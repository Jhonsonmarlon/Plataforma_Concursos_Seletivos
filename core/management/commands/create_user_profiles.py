from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'Create user profiles for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        count = 0
        
        for user in users:
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {count} user profiles'
            )
        ) 