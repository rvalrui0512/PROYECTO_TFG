from django.core.management.base import BaseCommand
from Guitarra.models import Video
from django.contrib.auth import get_user_model
from datetime import timedelta

class Command(BaseCommand):
    help = 'Crea un video de prueba usando el archivo media/videos/prueba.mp4'

    def handle(self, *args, **options):
        User = get_user_model()
        autor = User.objects.first()
        if not autor:
            self.stdout.write(self.style.ERROR('No hay usuarios en la base de datos.'))
            return
        from django.utils.text import slugify
        from datetime import datetime
        archivo = 'videos/prueba.mp4'
        base_slug = slugify('video-de-prueba')
        slug = base_slug
        i = 1
        while Video.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{datetime.now().strftime('%Y%m%d%H%M%S')}-{i}"
            i += 1
        video = Video.objects.create(
            titulo='Video de prueba',
            descripcion='Video de prueba subido automáticamente',
            palo_flamenco='Bulería',
            autor=autor,
            miniatura=None,
            archivo=archivo,
            duracion=timedelta(minutes=2),
            visibilidad=True,
            slug=slug
        )
        self.stdout.write(self.style.SUCCESS(f'Video creado: {video}'))
