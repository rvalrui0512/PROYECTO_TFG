from django.db import models

# Autenticación y perfil
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, error_messages={
        'unique': 'Ya existe un usuario registrado con este email.'
    })
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Name: {self.display_name} | pais: {self.pais}"
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


# Palos y vídeos
class PaloFlamenco(models.Model):

    NOMBRE_CHOICES = [
        ('Bulería', 'Bulería'),
        ('Alegrías', 'Alegrías'),
        ('Tangos', 'Tangos'),
        ('Soleá', 'Soleá'),
        ('Tanguillo', 'Tanguillo'),
        ('Fandango', 'Fandango'),
        ('Rumba', 'Rumba'),
        ('Canción Famosa', 'Canción Famosa'),
    ]

    nombre = models.CharField(max_length=100, choices=NOMBRE_CHOICES)
    descripcion = models.TextField(blank=True)
    slug= models.SlugField(unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Palo Flamenco'
        verbose_name_plural = 'Palos Flamencos'

class Video(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    palo_flamenco = models.ForeignKey(PaloFlamenco, on_delete=models.CASCADE, related_name='videos')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    miniatura = models.ImageField(upload_to='miniaturas/', blank=True, null=True)
    duracion = models.DurationField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    visibilidad = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"Título: {self.titulo} | Palo: {self.palo_flamenco.nombre} | Autor: {self.autor.name} | duración: {self.duracion} | Fecha: {self.fecha_publicacion}"

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'


# Interacción social
class Like(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['usuario', 'video'], name='unique_like')]
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='respuestas')

    def __str__(self):
        return f"Comentario de {self.usuario.name} en {self.video.titulo}: {self.texto[:30]}..."

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

class ChatRoom(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='chat_rooms')
    es_publico = models.BooleanField(default=True)

    def __str__(self):
        return f"ChatRoom: {self.nombre} | Video: {self.video.titulo} | Público: {self.es_publico}"

    class Meta:
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'

class ChatMessage(models.Model):
    chatroom= models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    mensaje = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.usuario.name} en {self.chatroom.nombre}: {self.mensaje[:30]}..."
    
    class Meta:
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'


# Clases y Reservas

# Disponibilidad de profesores para clases privadas
class DisponibilidadProfesor(models.Model):
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disponibilidades')
    dia_semana = models.CharField(max_length=10, choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.profesor.name} - {self.dia_semana}: {self.hora_inicio} a {self.hora_fin}"

    class Meta:
        verbose_name = 'Disponibilidad Profesor'
        verbose_name_plural = 'Disponibilidades Profesores'

class ClasePrivada(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clases_impartidas')
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clases_tomadas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    palo_flamenco = models.CharField(max_length=100, choices=PaloFlamenco.NOMBRE_CHOICES)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Clase: {self.titulo} | Profesor: {self.profesor.name} | Alumno: {self.alumno.name} | Estado: {self.estado}"

    class Meta:
        verbose_name = 'Clase Privada'
        verbose_name_plural = 'Clases Privadas'


# Catalogo de guitarras
class Guitarra(models.Model):

    TIPO_CHOICES = [
        ('Acústica', 'Acústica'),
        ('Eléctrica', 'Eléctrica'),
        ('Clásica', 'Clásica'),
        ('Flamenca', 'Flamenca'),
    ]

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='guitarras/', blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} | Tipo: {self.tipo} | Precio: ${self.precio}"

    class Meta:
        verbose_name = 'Guitarra'
        verbose_name_plural = 'Guitarras'


#IA y Contenido Flamenco
class ArticuloFlamenco(models.Model):
    CATEGORIA_CHOICES = [
        ('historia', 'Historia'),
        ('guitarras', 'Guitarras'),
        ('palos', 'Palos'),
        ('artistas', 'Artistas'),
    ]
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='historia')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Artículo Flamenco'
        verbose_name_plural = 'Artículos Flamencos'

class PreguntaIA(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preguntas_ia')
    pregunta = models.TextField()
    respuesta = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pregunta de {self.usuario.name}: {self.pregunta[:30]}..."

    class Meta:
        verbose_name = 'Pregunta IA'
        verbose_name_plural = 'Preguntas IA'
    
