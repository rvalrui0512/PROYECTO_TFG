from django.core.management.base import BaseCommand
from Guitarra.models import Profile
from django.contrib.auth import get_user_model
import os
from django.conf import settings

AVATAR_CHOICES = [
    'ava.svg', 'blair.svg', 'dean.svg', 'jack.svg', 'lilly.svg', 'lux.svg', 'mary.svg', 'sommer.svg'
]

class Command(BaseCommand):
    help = 'Asigna avatares de ejemplo a los usuarios existentes (seed)'

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.all()
        avatar_dir = os.path.join(settings.BASE_DIR, 'avatars')
        count = 0
        for i, user in enumerate(users):
            profile, _ = Profile.objects.get_or_create(user=user, defaults={'display_name': user.username})
            avatar_file = AVATAR_CHOICES[i % len(AVATAR_CHOICES)]
            profile.avatar = f'avatars/{avatar_file}'
            profile.save()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Asignados {count} avatares de ejemplo a los usuarios.'))
