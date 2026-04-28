from django.shortcuts import redirect
from django.conf import settings

class ForceLoginMiddleware:
    """
    Middleware que fuerza el login en toda la web excepto rutas públicas.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_paths = [
            settings.LOGIN_URL,
            '/logout/',
            '/admin/',
            '/static/',
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not any(request.path.startswith(path) for path in self.public_paths):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
