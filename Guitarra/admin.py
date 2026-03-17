from django.contrib import admin
from .models import Like, User, Profile, PaloFlamenco, Video, Comentario, ChatRoom, ChatMessage, DisponibilidadProfesor, ClasePrivada, Guitarra, ArticuloFlamenco, PreguntaIA

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('name',)

    fieldsets = [
        ('User', {
            'fields': ['name', 'email', 'password'],
        })
    ]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'pais', 'bio')
    search_fields = ('display_name', 'pais', 'bio')
    list_filter = ('pais', 'bio')

    fieldsets = [
        ('Profile', {
            'fields': ['user', 'display_name', 'bio', 'avatar', 'pais'],
        })
    ]

@admin.register(PaloFlamenco)
class PaloFlamencoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('nombre',)

    fieldsets = [
        ('Palo Flamenco', {
            'fields': ['nombre', 'descripcion', 'slug'],
        })
    ]

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descripcion', 'palo_flamenco', 'autor', 'duracion', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion', 'duracion', 'fecha_publicacion')
    list_filter = ('palo_flamenco', 'autor')

    fieldsets = [
        ('Video', {
            'fields': ['titulo', 'descripcion', 'palo_flamenco', 'autor', 'duracion', 'fecha_publicacion'],
        })
    ]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'video', 'fecha')
    search_fields = ('usuario__name', 'video__titulo', 'fecha')
    list_filter = ('usuario', 'video')

    fieldsets = [
        ('Like', {
            'fields': ['usuario', 'video', 'fecha'],
        })
    ]

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'video', 'texto', 'fecha_creacion')
    search_fields = ('usuario__name', 'video__titulo', 'texto', 'fecha_creacion')
    list_filter = ('usuario', 'video')

    fieldsets = [
        ('Comentario', {
            'fields': ['usuario', 'video', 'texto', 'fecha_creacion'],
        })
    ]

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'video')
    search_fields = ('nombre', 'video__titulo')
    list_filter = ('nombre', 'video')

    fieldsets = [
        ('Chat Room', {
            'fields': ['nombre', 'video'],
        })
    ]

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('chatroom', 'usuario', 'mensaje', 'timestamp')
    search_fields = ('chatroom__nombre', 'usuario__name', 'mensaje', 'timestamp')
    list_filter = ('chatroom', 'usuario', 'timestamp')

    fieldsets = [
        ('Chat Message', {
            'fields': ['chatroom', 'usuario', 'mensaje', 'timestamp'],
        })
    ]

@admin.register(DisponibilidadProfesor)
class DisponibilidadProfesorAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'dia_semana', 'hora_inicio', 'hora_fin')
    search_fields = ('profesor__name', 'dia_semana')
    list_filter = ('profesor', 'dia_semana')

    fieldsets = [
        ('Disponibilidad Profesor', {
            'fields': ['profesor', 'dia_semana', 'hora_inicio', 'hora_fin'],
        })
    ]

@admin.register(ClasePrivada)
class ClasePrivadaAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'alumno', 'titulo', 'fecha_inicio', 'fecha_fin', 'palo_flamenco', 'estado')
    search_fields = ('profesor__name', 'alumno__name', 'titulo', 'fecha_inicio', 'fecha_fin', 'palo_flamenco', 'estado')
    list_filter = ('profesor', 'alumno', 'palo_flamenco', 'estado')

    fieldsets = [
        ('Clase Privada', {
            'fields': ['profesor', 'alumno', 'titulo', 'fecha_inicio', 'fecha_fin', 'palo_flamenco', 'estado'],
        })
    ]

@admin.register(Guitarra)
class GuitarraAdmin(admin.ModelAdmin):
    list_display = ('marca', 'tipo', 'modelo', 'precio')
    search_fields = ('marca', 'tipo', 'modelo', 'precio')
    list_filter = ('marca', 'tipo', 'precio')

    fieldsets = [
        ('Guitarra', {
            'fields': ['marca', 'tipo', 'modelo', 'precio'],
        })
    ]

@admin.register(ArticuloFlamenco)
class ArticuloFlamencoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contenido', 'categoria')
    search_fields = ('titulo', 'contenido', 'categoria')
    list_filter = ('categoria', 'titulo')

    fieldsets = [
        ('Artículo Flamenco', {
            'fields': ['titulo', 'contenido', 'categoria', 'slug'],
        })
    ]

@admin.register(PreguntaIA)
class PreguntaIAAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pregunta', 'respuesta', 'timestamp')
    search_fields = ('usuario__name', 'pregunta', 'respuesta', 'timestamp')
    list_filter = ('usuario', 'timestamp')

    fieldsets = [
        ('Pregunta IA', {
            'fields': ['usuario', 'pregunta', 'respuesta', 'timestamp'],
        })
    ]
