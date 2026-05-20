# Estructura Detallada del Proyecto TFG Flamenco

Aplicación web de guitarra flamenca desarrollada con Django que integra un catálogo de guitarras, videotutoriales, clases privadas con videollamadas y un módulo de IA conversacional.

---

## 1. Descripción General

**TFG Flamenco** es una plataforma educativa y comercial de guitarra flamenca que proporciona:

- 📹 **Biblioteca de vídeos tutoriales** clasificados por palos flamencos
- 🎓 **Sistema de clases privadas** con videollamadas embebidas (Jitsi Meet)
- 🎸 **Catálogo de guitarras** con carrito de compra y pasarela de pago simulada
- 🤖 **Asistente IA conversacional** para consultas sobre flamenco
- 💬 **Sistema de comentarios anidados** en vídeos
- 🔔 **Sistema de notificaciones** en tiempo real
- 👤 **Gestión de perfiles** con avatares y localización

---

## 2. Arquitectura Técnica

### 2.1. Stack Tecnológico

| Componente | Tecnología |
|---|---|
| **Framework backend** | Django 6.0 |
| **Base de datos** | SQLite |
| **ORM** | Django ORM |
| **Frontend templating** | Django Templates + Bootstrap |
| **Multimedia** | Manejo de archivos (vídeos, imágenes) |
| **Videollamadas** | Jitsi Meet External API |
| **Carrito** | Django Session Storage |
| **Autenticación** | Django Authentication Framework |

### 2.2. Estructura de carpetas

```
TFG_FLAMENCO/
├── Guitarra/              # App principal
│   ├── models.py          # Definición de modelos
│   ├── views.py           # Vistas y lógica de negocio
│   ├── urls.py            # Enrutamiento
│   ├── forms.py           # Formularios
│   ├── admin.py           # Panel administrativo
│   ├── mixins.py          # Mixins de autenticación
│   ├── middleware.py      # Middleware personalizado
│   ├── management/commands/ # Comandos de gestión
│   └── templates/         # Plantillas HTML
├── TFG_FLAMENCO/          # Configuración del proyecto
│   ├── settings.py        # Configuración
│   ├── urls.py            # Enrutamiento global
│   └── wsgi.py            # Configuración WSGI
├── static/                # Archivos estáticos (CSS, JS)
├── media/                 # Archivos de usuario (vídeos, imágenes)
└── manage.py              # Utilidad de administración
```

---

## 3. Modelos de Datos

### 3.1. Autenticación y Perfil de Usuario

**`User`** (modelo estándar de Django)
- Autenticación y autorización centralizada
- Relación 1:1 con `Profile`

- `notas` (text): Comentarios adicionales

**`OrderItem`**
- `order` (FK Order): Orden asociada
- `guitarra` (FK Guitarra): Producto
- `cantidad` (int): Unidades compradas
- `precio_unitario` (decimal): Precio al momento de compra
- Método: `get_subtotal()` = cantidad × precio

### 3.6. IA y Contenido Educativo

**`ArticuloFlamenco`**
- `titulo`, `contenido` (text): Artículos informativos
- `categoria` (choice): Historia, Guitarras, Palos, Artistas
- `slug` (slug): URL amigable

**`PreguntaIA`**
- `usuario` (FK User): Quién preguntó
- `pregunta` (text): Consulta del usuario
- `respuesta` (text): Respuesta generada
- `timestamp` (datetime): Fecha de la pregunta
- Historial para análisis y mejora

### 3.7. Notificaciones

**`Notification`**
- `user` (FK User): Destinatario
- `message` (str): Contenido del aviso
- `url` (str): Enlace a recurso (opcional)
- `created_at` (datetime): Fecha automática
- `read` (bool): Leída o no

---

## 4. Formularios y Validación

| Formulario | Propósito |
|---|---|
| `RegistroUsuarioForm` | Registro + creación de Profile |
| `ProfileForm` | Edición de avatar, bio, país |
| `VideoForm` | Creación/edición de vídeos |
| `ComentarioForm` | Comentarios en vídeos |
| `ClasePrivadaForm` | Creación/edición de clases |
| `CheckoutForm` | Datos de envío (checkout) |
| `FakePaymentForm` | Simulación de pago |

---

## 5. Vistas y Funcionalidad

### 5.1. Usuarios

- **Registro**: Creación con perfil asociado automático
- **Listado**: Solo admin ve todos; usuario ve su registro
- **Detalle**: Información pública (owner/admin)
- **Edición**: Avatar predefinido o subido, bio, país
- **Eliminación**: Admin con limpieza de referencias en BD

### 5.2. Vídeos

- **Listado**: Filtros por palo y duración
- **Detalle**: Reproductor con soporte Range, comentarios, likes
- **Subida**: Solo admin; campos: título, descripción, palo, archivo, miniatura
- **Edición**: Metadatos + archivo
- **Eliminación**: Solo admin
- **Toggle Like**: AJAX, devuelve JSON con conteo

### 5.3. Clases Privadas

- **Listado**: Admin ve todas; usuario ve sus clases (como profesor o alumno)
- **Detalle**: Estado, información, botón de videollamada
- **Creación**: Admin; genera notificaciones automáticas
- **Videollamada**: Acceso embebido a Jitsi con validaciones de:
  - Permisos (profesor, alumno, admin)
  - Fecha/hora (no empezada, activa, caducada)
  - Estado (no cancelada)
- **Cambio de estado**: POST JSON; valida transiciones (pendiente → confirmada → realizada/cancelada)
- **Edición**: Solo admin
- **Eliminación**: Solo admin

### 5.4. Guitarras

- **Listado**: Filtros por modelo, color, precio
- **Detalle**: Especificaciones, precio, stock
- **Creación**: Admin
- **Edición**: Admin (marca, modelo, color, precio, stock, descripción)
- **Eliminación**: Admin

### 5.5. Carrito y Checkout

**Carrito**
- Almacenado en sesión (`request.session['cart']`)
- Añadir: POST a `/carrito/agregar/<id>/` → incrementa cantidad
- Eliminar: POST a `/carrito/eliminar/<id>/` → borra del carrito
- Vista: muestra items, precios, subtotal

**Checkout** (flujo de 3 pasos)
1. **Paso 1 - Checkout**: Formulario de envío; pre-llena con datos de usuario
2. **Paso 2 - Confirmar**: Resumen de orden; validación final
3. **Paso 3 - Pago**: Simulación de pasarela (sin cobro real); crea `Order` + `OrderItem`, descuenta stock
4. **Éxito**: Página de confirmación con número de pedido

### 5.6. IA Conversacional

- **GET**: Muestra formulario vacío
- **POST**: Procesa pregunta; tipos de consulta:
  - Saludos/despedidas
  - Información sobre guitarras (modelos Alhambra con especificaciones)
  - Palos flamencos (Bulería, Soleá, Tangos, etc.)
  - Artículos flamencos
- Guarda en `PreguntaIA` para historial

### 5.7. Notificaciones

- **Listado**: Muestra últimas 10 notificaciones del usuario
- **AJAX**: Soporte para `?ajax=1` (HTML) y `?count=1` (JSON con contador)
- **Automáticas**: Creadas al asignar/cambiar clases privadas
- **Lectura**: Marcadas como leídas al acceder

---

## 6. Tabla Completa de Endpoints

| **Path** | **Métodos** | **Nombre** | **Vista** | **Auth** | **Descripción** |
|---|---|---|---|---|---|
| / | GET | `guitarra:home` | `HomeView` | Public | Página principal con accesos a secciones. |
| /usuarios/ | GET | `guitarra:user_list` | `UserListView` | Login | Listado de usuarios. |
| /usuarios/nuevo/ | GET, POST | `guitarra:user_create` | `UserCreateView` | Public | Registro de usuario + Profile. |
| /usuarios/<int:pk>/ | GET | `guitarra:user_detail` | `UserDetailView` | Login+owner | Detalle de usuario. |
| /usuarios/<int:pk>/editar/ | GET, POST | `guitarra:user_update` | `UserUpdateView` | Login+owner | Edición de usuario y perfil. |
| /usuarios/<int:pk>/eliminar/ | POST | `guitarra:user_delete` | `UserDeleteView` | Admin | Eliminación de usuario. |
| /videos/ | GET | `guitarra:video_list` | `VideoListView` | Login | Listado con filtros. |
| /videos/nuevo/ | GET, POST | `guitarra:video_create` | `VideoCreateView` | Admin | Crear vídeo. |
| /videos/<int:pk>/ | GET, POST | `guitarra:video_detail` | `VideoDetailView` | Login | Detalle + comentarios. |
| /videos/<int:pk>/stream/ | GET | `guitarra:video_stream` | `video_stream` | Public | Servir archivo con Range. |
| /videos/<int:pk>/editar/ | GET, POST | `guitarra:video_update` | `VideoUpdateView` | Admin | Editar vídeo. |
| /videos/<int:pk>/eliminar/ | POST | `guitarra:video_delete` | `VideoDeleteView` | Admin | Eliminar vídeo. |
| /videos/<int:pk>/toggle-like/ | POST | `guitarra:video_toggle_like` | `toggle_like` | Login | Alternar like (AJAX). |
| /guitarras/ | GET | `guitarra:guitarra_list` | `GuitarraListView` | Login | Catálogo con filtros. |
| /guitarras/nueva/ | GET, POST | `guitarra:guitarra_create` | `GuitarraCreateView` | Admin | Añadir guitarra. |
| /guitarras/<int:pk>/ | GET | `guitarra:guitarra_detail` | `GuitarraDetailView` | Login | Ficha de producto. |
| /guitarras/<int:pk>/editar/ | GET, POST | `guitarra:guitarra_update` | `GuitarraUpdateView` | Admin | Editar guitarra. |
| /guitarras/<int:pk>/eliminar/ | POST | `guitarra:guitarra_delete` | `GuitarraDeleteView` | Admin | Eliminar guitarra. |
| /clases/ | GET | `guitarra:claseprivada_list` | `ClasePrivadaListView` | Login | Listado de clases. |
| /clases/nueva/ | GET, POST | `guitarra:claseprivada_create` | `ClasePrivadaCreateView` | Admin | Crear clase. |
| /clases/<int:pk>/ | GET | `guitarra:claseprivada_detail` | `ClasePrivadaDetailView` | Login | Detalle de clase. |
| /clases/<int:pk>/videollamada/ | GET | `guitarra:claseprivada_videollamada` | `claseprivada_videollamada` | Login | Acceso a Jitsi. |
| /clases/<int:pk>/cambiar-estado/ | POST | `guitarra:cambiar_estado_clase` | `cambiar_estado_clase` | Login | Cambiar estado (JSON). |
| /clases/<int:pk>/editar/ | GET, POST | `guitarra:claseprivada_update` | `ClasePrivadaUpdateView` | Admin | Editar clase. |
| /clases/<int:pk>/eliminar/ | POST | `guitarra:claseprivada_delete` | `ClasePrivadaDeleteView` | Admin | Eliminar clase. |
| /ia/ | GET, POST | `guitarra:ia_busqueda` | `IABusquedaView` | Login | Buscador IA. |
| /notificaciones/ | GET | `guitarra:notification_list` | `NotificationPopupView` | Login | Popup notificaciones. |
| /carrito/ | GET | `guitarra:cart_view` | `cart_view` | Public | Ver carrito. |
| /carrito/agregar/<int:guitarra_id>/ | POST | `guitarra:add_to_cart` | `add_to_cart` | Public | Añadir al carrito. |
| /carrito/eliminar/<int:guitarra_id>/ | POST | `guitarra:remove_from_cart` | `remove_from_cart` | Public | Eliminar del carrito. |
| /checkout/ | GET, POST | `guitarra:checkout` | `checkout_view` | Login | Formulario de envío. |
| /checkout/confirmar/ | GET, POST | `guitarra:checkout_confirm` | `checkout_confirm_view` | Login | Resumen de orden. |
| /checkout/pago/ | GET, POST | `guitarra:checkout_payment` | `checkout_payment_view` | Login | Pago simulado. |
| /checkout/exito/<int:order_id>/ | GET | `guitarra:checkout_success` | `checkout_success_view` | Login | Confirmación. |
| /mis-pedidos/ | GET | `guitarra:my_orders` | `my_orders_view` | Login | Historial de pedidos. |
| /pedidos/<int:order_id>/ | GET | `guitarra:order_detail` | `order_detail_view` | Login | Detalle de pedido. |
| /admin/ | GET, POST | `admin` | Django admin | Admin | Panel administrativo. |
| /accounts/login/ | GET, POST | `login` | Django auth | Public | Login. |
| /accounts/logout/ | GET | `logout` | Django auth | Login | Logout. |
| /accounts/password_change/ | GET, POST | `password_change` | Django auth | Login | Cambiar contraseña. |
| /accounts/password_change/done/ | GET | `password_change_done` | Django auth | Login | Confirmación. |
| /accounts/password_reset/ | GET, POST | `password_reset` | Django auth | Public | Reset contraseña. |
| /accounts/password_reset/done/ | GET | `password_reset_done` | Django auth | Public | Confirmación envío. |
| /accounts/reset/<uid>/<token>/ | GET, POST | `password_reset_confirm` | Django auth | Public | Confirmar reset. |
| /accounts/reset/done/ | GET | `password_reset_complete` | Django auth | Public | Reset completado. |
| (Catch-all) | GET | — | `handler_404` | Public | Página 404. |

### 6.1. Leyenda de Autenticación

- **Public**: Sin autenticación
- **Login**: Usuario autenticado
- **Login+owner**: Propietario del recurso o admin
- **Admin**: Staff/Superuser

### 6.2. Notas Técnicas

- **Namespace**: `guitarra:` para todas las rutas de la app
- **AJAX endpoints**: `/videos/<id>/toggle-like/`, `/clases/<id>/cambiar-estado/`, `/notificaciones/?ajax=1`
- **Streaming**: `/videos/<id>/stream/` soporta HTTP Range headers
- **Carrito**: Sesión (sin BD), flujo: agregar → eliminar → checkout
- **Checkout**: 3 pasos (formulario → confirmar → pago → success)
- **Notificaciones**: Se crean automáticamente al crear/modificar clases

---

## 7. Seguridad y Autenticación

- **Django Authentication**: Contraseñas hashadas con PBKDF2
- **Login Required Mixin**: Protección de vistas
- **Mixins personalizados**:
  - `AdminRequiredLoginMixin`: Solo admin
  - `OwnerOrAdminRequiredMixin`: Propietario o admin
- **CSRF Protection**: Todos los formularios POST protegidos
- **Permission checks**: En vistas sensibles (videollamadas, eliminación, etc.)

---

## 8. Gestión de Archivos Multimedia

- **Vídeos**: Carpeta `media/videos/` con soporte Range header (streaming)
- **Imágenes**: Miniaturas (`media/miniaturas/`), guitarras (`media/guitarras/`), avatares (`media/avatars/`)
- **Almacenamiento**: Sistema de archivos local (adaptable a S3 en producción)

---

## 9. Flujos de Usuario Principales

### 9.1. Usuario estudiante

1. Registro y creación de perfil
2. Visualiza catálogo de vídeos (filtrado por palo)
3. Ve vídeos, comenta, da likes
4. Se inscribe en clases privadas (si admin las crea)
5. Accede a videollamada Jitsi en horario
6. Navega catálogo de guitarras
7. Compra guitarras (carrito → checkout → pago simulado)

### 9.2. Profesor

1. Registro
2. Sube vídeos tutoriales
3. Recibe notificaciones de clases asignadas
4. Accede a videollamadas Jitsi
5. Puede ver órdenes (si admin)

### 9.3. Administrador

1. Acceso a panel Django completo
2. Gestión de usuarios, vídeos, clases, guitarras, órdenes
3. Edición de artículos IA
4. Visualización de historial de preguntas IA

---

## 10. Base de Datos

**SQLite** (`db.sqlite3`)

Modelos:
- `auth_user` (Django)
- `guitarra_profile`
- `guitarra_paloflamenco`
- `guitarra_video`, `guitarra_like`, `guitarra_comentario`
- `guitarra_chatroom`, `guitarra_chatmessage`
- `guitarra_disponibilidadprofesor`, `guitarra_claseprivada`
- `guitarra_guitarra`
- `guitarra_notification`
- `guitarra_articuloflamenco`, `guitarra_preguntaia`
- `guitarra_order`, `guitarra_orderitem`

---

## 11. Configuración del Proyecto (`settings.py`)

### Aplicaciones instaladas
- `django.contrib.admin`
- `django.contrib.auth`
- `django.contrib.contenttypes`
- `django.contrib.sessions`
- `django.contrib.messages`
- `django.contrib.staticfiles`
- `Guitarra` (app principal)

### Bases de datos
- SQLite (desarrollo)

### Configuración de archivos
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`
- `STATIC_URL = '/static/'`

### Jitsi Meet (si aplicable)
- `JITSI_MEET_DOMAIN` (ajustable en settings)
- `JITSI_MEET_EXTERNAL_API_URL`

---

## 12. Conclusión

TFG Flamenco es una plataforma educativa completa que integra múltiples módulos (vídeos, clases, tienda, IA) en un único ecosistema Django profesional, con gestión robusta de usuarios, contenido multimedia y transacciones simuladas.

---

## 13. Despliegue en Render (resumen explicativo)

Este proyecto se ha preparado para desplegarse en Render mediante ajustes en la configuración y en las dependencias. En producción se utiliza `gunicorn` como servidor WSGI y `WhiteNoise` para servir los archivos estáticos empaquetados; las credenciales y ajustes sensibles se leen desde variables de entorno para no almacenarlas en el código.

En el repositorio se incluyen orientaciones para Render (por ejemplo `render.yaml`, `Procfile` y `.env.example`), pero la parte esencial es garantizar que las dependencias de producción estén en `requirements.txt`, que la aplicación ejecute las migraciones al desplegarse y que `collectstatic` genere los assets estáticos. Para la persistencia de datos se recomienda usar una base de datos gestionada (por ejemplo PostgreSQL) y, para los archivos subidos por usuarios, un almacenamiento externo (S3, Cloudinary u otro), ya que el sistema de ficheros de Render no es persistente entre despliegues.

Se han restaurado en el repositorio los activos necesarios en `static/` y `media/` para que la fase de empaquetado disponga de los recursos visuales requeridos. Además, se añadió `gunicorn` a las dependencias para garantizar que el servicio arranque correctamente y se configuró `WhiteNoise` en la capa de middleware para atender recursos estáticos cuando la aplicación se ejecuta con `DEBUG` desactivado.

En términos generales, el despliegue en Render consiste en proveer las variables de entorno necesarias desde el panel de Render, asegurar las dependencias en `requirements.txt`, utilizar una base de datos gestionada para producción y emplear un almacenamiento externo para `MEDIA` si se necesita persistencia. Estas decisiones garantizan seguridad, rendimiento y persistencia apropiados para una entrega en producción alojada en Render.

