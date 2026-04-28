from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredLoginMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para vistas que requieren que el usuario sea staff o superusuario.
    Redirige a login si no está autenticado y lanza 403 si no es admin.
    """
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("No tienes permisos de administrador.")

class OwnerOrAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin para permitir acceso solo al propietario del objeto o admin.
    """
    def test_func(self):
        obj = self.get_object()
        return obj == self.request.user or self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied("No tienes permisos para acceder a este recurso.")

class OnlyAnonymousRequiredMixin:
    """
    Mixin para vistas que solo deben ser accesibles por usuarios no autenticados (por ejemplo, registro).
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('guitarra:home')
        return super().dispatch(request, *args, **kwargs)
