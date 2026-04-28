import os
import re
from django.core.management.base import BaseCommand
from Guitarra.models import Guitarra
from django.conf import settings

class Command(BaseCommand):
    help = 'Crea guitarras automáticamente a partir de las imágenes en media/guitarras/'

    def handle(self, *args, **options):
        media_guitarras = os.path.join(settings.MEDIA_ROOT, 'guitarras')
        if not os.path.exists(media_guitarras):
            self.stdout.write(self.style.ERROR('No existe la carpeta media/guitarras'))
            return
        archivos = [f for f in os.listdir(media_guitarras) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not archivos:
            self.stdout.write(self.style.WARNING('No hay imágenes en media/guitarras'))
            return
        patron = re.compile(r'guitarra([A-Za-z]+)([0-9A-Za-z]+)([A-Z]+)?(\d+)')
        creadas = 0
        for archivo in archivos:
            nombre, _ = os.path.splitext(archivo)
            match = patron.match(nombre)
            if not match:
                self.stdout.write(self.style.WARNING(f'Nombre no reconocido: {archivo}'))
                continue
            marca = match.group(1)
            modelo = match.group(2)
            color = match.group(3) or ''
            precio = match.group(4)
            # Evitar duplicados
            if Guitarra.objects.filter(marca=marca, modelo=modelo, precio=precio).exists():
                self.stdout.write(self.style.WARNING(f'Ya existe: {marca} {modelo} {precio}'))
                continue
            guitarra = Guitarra(
                marca=marca,
                modelo=modelo,
                tipo='Clásica',  # Puedes ajustar esto si tienes lógica para el tipo
                descripcion=f'{marca} {modelo} {color}'.strip(),
                precio=precio,
                stock=1,
                imagen=f'guitarras/{archivo}'
            )
            guitarra.save()
            creadas += 1
            self.stdout.write(self.style.SUCCESS(f'Creada: {marca} {modelo} {color} {precio}'))
        self.stdout.write(self.style.SUCCESS(f'Total guitarras creadas: {creadas}'))
