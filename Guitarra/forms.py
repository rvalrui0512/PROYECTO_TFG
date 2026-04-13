from django import forms
from django.contrib.auth.hashers import make_password
from .models import (
    Profile, Video, Comentario, ClasePrivada, Guitarra, ArticuloFlamenco, PreguntaIA
)
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistroUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite la contraseña'}),
        label='Repite la contraseña'
    )

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

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'avatar', 'pais']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre visible'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Biografía', 'rows': 3}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['titulo', 'descripcion', 'palo_flamenco', 'autor', 'miniatura', 'archivo', 'duracion', 'visibilidad', 'slug']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'palo_flamenco': forms.Select(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'miniatura': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'duracion': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'visibilidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slug'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario...', 'rows': 3}),
        }

    PALABRAS_PROHIBIDAS = [
        # Variantes con y sin tilde
        'tonto', 'tonta', 'idiota', 'gilipollas', 'imbecil', 'imbécil', 'cabron', 'cabrón', 'cabrona',
        'estupido', 'estúpido', 'estupida', 'estúpida', 'subnormal', 'retrasado', 'retrasada', 'inutil', 'inútil',
        'payaso', 'payasa', 'asqueroso', 'asquerosa', 'cerdo', 'cerda', 'bastardo', 'bastarda', 'malnacido', 'malnacida',
        'mierda', 'joder', 'puta', 'puto', 'zorra', 'maricon', 'maricón', 'marica', 'pendejo', 'pendeja', 'mamon', 'mamón', 'mamona',
        'huevon', 'huevón', 'huevona', 'cagon', 'cagón', 'cagada', 'cono', 'coño', 'hostia', 'carajo', 'chinga', 'chingada',
        'pelotudo', 'boludo', 'gil', 'soplapollas', 'capullo', 'pringado', 'pringada', 'petardo', 'petarda', 'perro', 'perra',
        'zopenco', 'zopenca', 'tusco', 'tusca', 'hijo de puta', 'hija de puta', 'maldito', 'maldita',
        # Más insultos y variantes
        'baboso', 'babosa',
        'anormal', 'bestia', 'burro', 'burra', 'cacho', 'cacho de carne', 'cacho de mierda',
        'cacho de tonto', 'cacho de tonta', 'cacho de gilipollas', 'cacho de subnormal', 'cacho de inutil', 'cacho de inútil',
        'cacho de payaso', 'cacho de payasa', 'cacho de asqueroso', 'cacho de asquerosa', 'cacho de cerdo', 'cacho de cerda',
        'cacho de bastardo', 'cacho de bastarda', 'cacho de malnacido', 'cacho de malnacida', 'cacho de mierda',
        'cacho de joder', 'cacho de puta', 'cacho de puto', 'cacho de zorra', 'cacho de maricon', 'cacho de maricón',
        'cacho de marica', 'cacho de pendejo', 'cacho de pendeja', 'cacho de mamon', 'cacho de mamón', 'cacho de mamona',
        'cacho de huevon', 'cacho de huevón', 'cacho de huevona', 'cacho de cagon', 'cacho de cagón', 'cacho de cagada',
        'cacho de cono', 'cacho de coño', 'cacho de hostia', 'cacho de carajo', 'cacho de chinga', 'cacho de chingada',
        'cacho de pelotudo', 'cacho de boludo', 'cacho de gil', 'cacho de soplapollas', 'cacho de capullo',
        'cacho de pringado', 'cacho de pringada', 'cacho de petardo', 'cacho de petarda', 'cacho de perro', 'cacho de perra',
        'cacho de zopenco', 'cacho de zopenca', 'cacho de tusco', 'cacho de tusca', 'cacho de hijo de puta', 'cacho de hija de puta',
        'cacho de maldito', 'cacho de maldita',
        # Insultos internacionales y variantes
        'asshole', 'bastard', 'bitch', 'dick', 'dumb', 'fuck', 'fucker', 'shit', 'stupid', 'moron', 'jerk', 'retard',
        'idiot', 'loser', 'sucker', 'twat', 'wanker', 'slut', 'whore', 'cunt', 'arsehole', 'bollocks', 'bugger', 'git',
        'prick', 'tosser', 'wank', 'wanker', 'arse', 'arsewipe', 'arsehead', 'arseface', 'arsehole', 'arselicker',
        'arsewipe', 'arse', 'arsehole', 'arsehead', 'arseface', 'arsewipe', 'arselicker',
        # Variantes sin espacios
        'hijodeputa', 'hijaputa', 'malparido', 'malparida', 'cabronazo', 'cabroncete', 'cabronazo', 'cabroncete',
        'mierdoso', 'mierdosa', 'mierdecilla', 'mierdilla', 'mierdoso', 'mierdosa',
        # Diminutivos y aumentativos
        'tontito', 'tontita', 'tontazo', 'tontaza', 'idiotita', 'idiotazo', 'gilipollitas', 'gilipollita', 'gilipollazo',
        'imbecilito', 'imbecilita', 'imbecilazo', 'imbecilaza', 'payasete', 'payaseta', 'payasazo', 'payasaza',
        'asquerosito', 'asquerosita', 'asquerosazo', 'asquerosaza', 'cerdito', 'cerdita', 'cerdazo', 'cerdaza',
        'bastardito', 'bastardita', 'bastardazo', 'bastardaza', 'malnacidito', 'malnacidita', 'malnacidazo', 'malnacidaza',
        'mierdecita', 'mierdecito', 'mierdecilla', 'mierdecillo', 'mierdecazo', 'mierdecaza',
        # Otros
        'mongol', 'mongolo', 'mongolica', 'mongólica', 'mongolico', 'mongólico', 'mongolita', 'mongolita',
        'tarado', 'tarada', 'taradito', 'taradita', 'taradazo', 'taradaza',
        'imbecil', 'imbécil', 'anormal', 'bestia', 'burro', 'burra', 'animal', 'animalito', 'animalazo',
        'bobo', 'boba', 'bobito', 'bobita', 'bobazo', 'bobaza',
        'lerdo', 'lerda', 'lerdito', 'lerdita', 'lerdazo', 'lerdaza',
        'memo', 'memito', 'memazo', 'memaza',
        'necio', 'necia', 'neciito', 'neciaza',
        'tontoelculo', 'tontolculo', 'tontolaba', 'tontolaba',
        'subnormalito', 'subnormalazo', 'subnormalaza',
        'gilipuertas', 'gilipuertas', 'gilipuertas',
        'caraculo', 'caraculo', 'caraculo',
        'carapolla', 'carapolla', 'carapolla',
        'caraculo', 'caraculo', 'caraculo',
        'carapene', 'carapene', 'carapene',
    ]

    def clean_texto(self):
        texto = self.cleaned_data.get('texto', '')
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