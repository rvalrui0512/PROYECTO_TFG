from django.urls import path
from .views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView
from .views import VideoListView, VideoDetailView, VideoCreateView, VideoUpdateView, VideoDeleteView
from .views import GuitarraListView, GuitarraDetailView, GuitarraCreateView, GuitarraUpdateView, GuitarraDeleteView
from .views import ClasePrivadaListView, ClasePrivadaDetailView, ClasePrivadaCreateView, ClasePrivadaUpdateView, ClasePrivadaDeleteView
from .views import IABusquedaView, NotificationListView, NotificationPopupView
from .views import add_to_cart, cart_view, remove_from_cart
from .views import checkout_view, checkout_confirm_view, checkout_payment_view, checkout_success_view, my_orders_view, order_detail_view
from .views import *

app_name = 'guitarra'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('usuarios/', UserListView.as_view(), name='user_list'),
    path('usuarios/nuevo/', UserCreateView.as_view(), name='user_create'),
    path('usuarios/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('usuarios/<int:pk>/editar/', UserUpdateView.as_view(), name='user_update'),
    path('usuarios/<int:pk>/eliminar/', UserDeleteView.as_view(), name='user_delete'),

    path('videos/', VideoListView.as_view(), name='video_list'),
    path('videos/nuevo/', VideoCreateView.as_view(), name='video_create'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('videos/<int:pk>/editar/', VideoUpdateView.as_view(), name='video_update'),
    path('videos/<int:pk>/eliminar/', VideoDeleteView.as_view(), name='video_delete'),
    path('videos/<int:pk>/toggle-like/', toggle_like, name='video_toggle_like'),

    path('guitarras/', GuitarraListView.as_view(), name='guitarra_list'),
    path('guitarras/nueva/', GuitarraCreateView.as_view(), name='guitarra_create'),
    path('guitarras/<int:pk>/', GuitarraDetailView.as_view(), name='guitarra_detail'),
    path('guitarras/<int:pk>/editar/', GuitarraUpdateView.as_view(), name='guitarra_update'),
    path('guitarras/<int:pk>/eliminar/', GuitarraDeleteView.as_view(), name='guitarra_delete'),

    path('clases/', ClasePrivadaListView.as_view(), name='claseprivada_list'),
    path('clases/nueva/', ClasePrivadaCreateView.as_view(), name='claseprivada_create'),
    path('clases/<int:pk>/', ClasePrivadaDetailView.as_view(), name='claseprivada_detail'),
    path('clases/<int:pk>/videollamada/', claseprivada_videollamada, name='claseprivada_videollamada'),
    path('clases/<int:pk>/cambiar-estado/', cambiar_estado_clase, name='cambiar_estado_clase'),
    path('clases/<int:pk>/editar/', ClasePrivadaUpdateView.as_view(), name='claseprivada_update'),
    path('clases/<int:pk>/eliminar/', ClasePrivadaDeleteView.as_view(), name='claseprivada_delete'),

    path('ia/', IABusquedaView.as_view(), name='ia_busqueda'),
    path('notificaciones/', NotificationPopupView.as_view(), name='notification_list'),
    
    # Carrito
    path('carrito/', cart_view, name='cart_view'),
    path('carrito/agregar/<int:guitarra_id>/', add_to_cart, name='add_to_cart'),
    path('carrito/eliminar/<int:guitarra_id>/', remove_from_cart, name='remove_from_cart'),
    
    # Checkout
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/confirmar/', checkout_confirm_view, name='checkout_confirm'),
    path('checkout/pago/', checkout_payment_view, name='checkout_payment'),
    path('checkout/exito/<int:order_id>/', checkout_success_view, name='checkout_success'),
    path('mis-pedidos/', my_orders_view, name='my_orders'),
    path('pedidos/<int:order_id>/', order_detail_view, name='order_detail'),
]
