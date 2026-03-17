from django import forms
from .models import (
    User, Profile, PaloFlamenco, Video, Like, Comentario, ChatRoom, ChatMessage,
    DisponibilidadProfesor, ClasePrivada, Guitarra, ArticuloFlamenco, PreguntaIA
)



from django.contrib.auth.forms import UserCreationForm

# Formulario de registro de usuario basado en UserCreationForm, con campos extra de Profile
class RegistroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('name', 'email', 'password1', 'password2', 'display_name', 'nivel_guitarra', 'pais')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    NIVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    display_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre visible'}),
        label='Nombre visible'
    )
    nivel_guitarra = forms.ChoiceField(
        choices=NIVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Nivel de guitarra'
    )
    pais = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}),
        label='País'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este email.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden.')
            if len(password1) < 8:
                raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')
        return password2

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'display_name', 'bio', 'avatar', 'pais']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre visible'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Biografía', 'rows': 3}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}),
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['titulo', 'descripcion', 'palo_flamenco', 'autor', 'miniatura', 'duracion', 'visibilidad', 'slug']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'palo_flamenco': forms.Select(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'miniatura': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'duracion': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'visibilidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['usuario', 'video', 'texto', 'padre']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'video': forms.Select(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comentario', 'rows': 3}),
            'padre': forms.Select(attrs={'class': 'form-control'}),
        }

    PALABRAS_PROHIBIDAS = [
        'tonto', 'idiota', 'gilipollas', 'imbécil', 'cabrón', 'cabrona', 'estúpido', 'estúpida',
        'subnormal', 'retrasado', 'retrasada', 'inútil', 'payaso', 'payasa', 'asqueroso', 'asquerosa',
        'cerdo', 'cerda', 'bastardo', 'bastarda', 'malnacido', 'malnacida', 'mierda', 'joder',
        'puta', 'puto', 'zorra', 'maricón', 'marica', 'pendejo', 'pendeja', 'mamón', 'mamona',
        'huevón', 'huevona', 'cagón', 'cagada', 'coño', 'hostia', 'carajo', 'chinga', 'chingada',
        'pelotudo', 'boludo', 'gil', 'soplapollas', 'capullo', 'pringado', 'pringada', 'petardo', 'petarda'
    ]

    def clean_texto(self):
        texto = self.cleaned_data.get('texto', '')
        if len(texto.strip()) < 10:
            raise forms.ValidationError('El comentario debe tener al menos 10 caracteres.')
        texto_lower = texto.lower()
        for palabra in self.PALABRAS_PROHIBIDAS:
            if palabra in texto_lower:
                raise forms.ValidationError('El comentario contiene lenguaje ofensivo.')
        return texto
    
class ClasePrivadaForm(forms.ModelForm):
    class Meta:
        model = ClasePrivada
        fields = ['profesor', 'alumno', 'titulo', 'descripcion', 'palo_flamenco', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'profesor': forms.Select(attrs={'class': 'form-control'}),
            'alumno': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'palo_flamenco': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        profesor = cleaned_data.get('profesor')
        from django.utils import timezone
        now = timezone.now()
        if fecha_inicio and fecha_inicio < now:
            self.add_error('fecha_inicio', 'La fecha de inicio no puede estar en el pasado.')
        if fecha_fin and fecha_fin < now:
            self.add_error('fecha_fin', 'La fecha de fin no puede estar en el pasado.')
        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            self.add_error('fecha_fin', 'La fecha de fin debe ser posterior a la de inicio.')
        if profesor and fecha_inicio and fecha_fin:
            solapadas = ClasePrivada.objects.filter(
                profesor=profesor,
                fecha_inicio__lt=fecha_fin,
                fecha_fin__gt=fecha_inicio
            )
            if self.instance.pk:
                solapadas = solapadas.exclude(pk=self.instance.pk)
            if solapadas.exists():
                raise forms.ValidationError('El profesor ya tiene una clase en ese horario.')
        return cleaned_data

class GuitarraForm(forms.ModelForm):
    class Meta:
        model = Guitarra
        fields = ['marca', 'modelo', 'tipo', 'descripcion', 'precio', 'stock', 'imagen']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio
    
class ArticuloFlamencoForm(forms.ModelForm):
    class Meta:
        model = ArticuloFlamenco
        fields = ['titulo', 'contenido', 'categoria', 'slug']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenido', 'rows': 5}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
        }

class PreguntaIAForm(forms.ModelForm):
    class Meta:
        model = PreguntaIA
        fields = ['usuario', 'pregunta', 'respuesta']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'pregunta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Pregunta', 'rows': 3}),
            'respuesta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Respuesta', 'rows': 3}),
        }