"""
URL configuration for TFG_FLAMENCO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve
from Guitarra import views as guitarra_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('Guitarra.urls')),
    # Servir static/media también con DEBUG=False (Render) para garantizar assets visibles en la entrega
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # Catch-all (development): redirige a handler_404 para ver la plantilla personalizada
    re_path(r'^(?!admin/)(?!accounts/)(?!static/)(?!media/).*$', guitarra_views.handler_404),
]

# Registrar el handler para uso en producción (DEBUG=False)
handler404 = 'Guitarra.views.handler_404'
