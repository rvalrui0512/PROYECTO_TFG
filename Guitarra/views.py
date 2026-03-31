from django.views import View
from django.utils import timezone
from .models import ArticuloFlamenco, PreguntaIA

# Vista para el buscador de IA
class IABusquedaView(View):
    template_name = 'IA/ia_busqueda.html'

    def get(self, request):
        return render(request, self.template_name, {'respuesta': None, 'pregunta': ''})

    def post(self, request):
        pregunta = request.POST.get('pregunta', '').strip()
        respuesta = None
        if pregunta:
            articulo = ArticuloFlamenco.objects.filter(titulo__icontains=pregunta).first()
            if articulo:
                respuesta = articulo.contenido
            else:
                # Aquí iría la llamada real a la IA
                respuesta = f"Respuesta generada por IA para: {pregunta}"
                PreguntaIA.objects.create(
                    usuario=request.user if request.user.is_authenticated else None,
                    pregunta=pregunta,
                    respuesta=respuesta,
                    timestamp=timezone.now()
                )
        return render(request, self.template_name, {'respuesta': respuesta, 'pregunta': pregunta})

from django.shortcuts import render
from .models import User, Profile, PaloFlamenco, Video, Like, Comentario, ChatRoom, ChatMessage, DisponibilidadProfesor, ClasePrivada, Guitarra, ArticuloFlamenco, PreguntaIA
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegistroUsuarioForm, ProfileForm, ClasePrivadaForm, VideoForm

# Create your views here.
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

class UserCreateView(CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('guitarra:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        Profile.objects.create(
            user=user,
            display_name=form.cleaned_data['display_name'],
            pais=form.cleaned_data['pais'],
        )
        return response


# Vista para editar usuario y perfil asociado
from django.shortcuts import redirect
from django.contrib import messages

class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['name', 'email']
    success_url = reverse_lazy('guitarra:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST, self.request.FILES, instance=self.object.profile)
        else:
            context['profile_form'] = ProfileForm(instance=self.object.profile)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        if profile_form.is_valid():
            self.object = form.save()
            profile_form.save()
            messages.success(self.request, 'Usuario y perfil actualizados correctamente.')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('guitarra:user_list')


class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    paginate_by = 5

class VideoDetailView(DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'

class VideoCreateView(CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'videos/video_form.html'
    success_url = reverse_lazy('guitarra:video_list')

class VideoUpdateView(UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'videos/video_form.html'
    success_url = reverse_lazy('guitarra:video_list')

class VideoDeleteView(DeleteView):
    model = Video
    template_name = 'videos/video_confirm_delete.html'
    success_url = reverse_lazy('guitarra:video_list')


class GuitarraListView(ListView):
    model = Guitarra
    template_name = 'guitarras/guitarra_list.html'
    context_object_name = 'guitarras'
    paginate_by = 5

class GuitarraDetailView(DetailView):
    model = Guitarra
    template_name = 'guitarras/guitarra_detail.html'
    context_object_name = 'guitarra'

class GuitarraCreateView(CreateView):
    model = Guitarra
    fields = ['modelo', 'marca', 'precio', 'descripcion']
    template_name = 'guitarras/guitarra_form.html'
    success_url = reverse_lazy('guitarra:guitarra_list')

class GuitarraUpdateView(UpdateView):
    model = Guitarra
    fields = ['modelo', 'marca', 'precio', 'descripcion']
    template_name = 'guitarras/guitarra_form.html'
    success_url = reverse_lazy('guitarra:guitarra_list')

class GuitarraDeleteView(DeleteView):
    model = Guitarra
    template_name = 'guitarras/guitarra_confirm_delete.html'
    success_url = reverse_lazy('guitarra:guitarra_list')


class ClasePrivadaListView(ListView):
    model = ClasePrivada
    template_name = 'clases_privadas/claseprivada_list.html'
    context_object_name = 'clases'
    paginate_by = 5

class ClasePrivadaDetailView(DetailView):
    model = ClasePrivada
    template_name = 'clases_privadas/claseprivada_detail.html'
    context_object_name = 'clase'

class ClasePrivadaCreateView(CreateView):
    model = ClasePrivada
    form_class = ClasePrivadaForm
    template_name = 'clases_privadas/claseprivada_form.html'
    success_url = reverse_lazy('guitarra:claseprivada_list')

class ClasePrivadaUpdateView(UpdateView):
    model = ClasePrivada
    form_class = ClasePrivadaForm
    template_name = 'clases_privadas/claseprivada_form.html'
    success_url = reverse_lazy('guitarra:claseprivada_list')

class ClasePrivadaDeleteView(DeleteView):
    model = ClasePrivada
    template_name = 'clases_privadas/claseprivada_confirm_delete.html'
    success_url = reverse_lazy('guitarra:claseprivada_list')

