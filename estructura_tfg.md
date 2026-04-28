
# Estructura Detallada del Proyecto TFG Flamenco

Este documento resume el estado actual del proyecto web de guitarra flamenca basado en Django.

---

## 1. Modelos (`models.py`)

### 1.1. Autenticación y perfil
- `User`: modelo estándar de Django.
- `Profile`: perfil ampliado con `display_name`, `bio`, `avatar` y `pais`.

### 1.2. Palos y vídeos
- `PaloFlamenco`: catálogo de palos con `nombre`, `descripcion` y `slug`.
- `Video`: vídeos con `titulo`, `descripcion`, `palo_flamenco`, `autor`, `miniatura`, `archivo`, `duracion`, `fecha_publicacion`, `visibilidad` y `slug`.

### 1.3. Interacción social
- `Like`: likes por usuario y vídeo.
- `Comentario`: comentarios sobre vídeos con soporte de respuestas anidadas mediante `padre`.
- `ChatRoom` y `ChatMessage`: base de datos para salas y mensajes asociados a vídeos.

### 1.4. Clases privadas
- `DisponibilidadProfesor`: franjas de disponibilidad del profesor.
- `ClasePrivada`: reserva de clase con `profesor`, `alumno`, `titulo`, `descripcion`, `palo_flamenco`, `fecha_inicio`, `fecha_fin` y `estado`.

### 1.5. Catálogo de guitarras
- `Guitarra`: catálogo con `marca`, `modelo`, `tipo`, `descripcion`, `precio`, `stock` e `imagen`.

### 1.6. IA y contenido flamenco
- `ArticuloFlamenco`: artículos informativos por categoría.
- `PreguntaIA`: historial de preguntas y respuestas del buscador IA.

### 1.7. Notificaciones
- `Notification`: avisos para usuarios con `message`, `url`, `created_at` y `read`.

---

## 2. Administración (`admin.py`)

Panel administrativo para gestionar usuarios, perfiles, vídeos, comentarios, clases privadas, guitarras, artículos, preguntas IA y notificaciones.

---

## 3. Formularios (`forms.py`) y validaciones

- `RegistroUsuarioForm`: registro de usuario y creación del perfil asociado.
- `ProfileForm`: edición de perfil.
- `VideoForm`: creación y edición de vídeos.
- `ComentarioForm`: gestión de comentarios.
- `ClasePrivadaForm`: creación y edición de clases privadas.
- `GuitarraForm`: gestión del catálogo de guitarras.

---

## 4. Vistas (`views.py`) y funcionalidad

### 4.1. Sección vídeos
- Listado de vídeos con filtros.
- Detalle de vídeo con reproductor y comentarios.
- Subida, edición y eliminación de vídeos para usuarios con permisos de administración.

### 4.2. Sección clases privadas
- Listado, detalle, alta, edición y borrado de clases privadas.
- Videollamada embebida con Jitsi Meet.
- Control de acceso por estado de la clase y usuario autenticado.
- Avisos visuales cuando una clase está cancelada, caducada o todavía no ha empezado.

### 4.3. Sección notificaciones
- Listado de notificaciones para cada usuario.
- Indicador de notificaciones no leídas en la interfaz.
- Avisos automáticos al crear o modificar clases privadas.

### 4.4. Sección guitarras
- Listado con filtros por modelo, tipo y precio.
- Detalle de guitarra.
- Carrito de compra simulado con sesión.

### 4.5. Sección IA flamenca
- Buscador de preguntas sobre guitarras, palos, historia y artículos.
- Guarda el historial de consultas y respuestas.

### 4.6. Interacción social
- Gestión de comentarios sobre vídeos.
- Base preparada para chat por vídeo con `ChatRoom` y `ChatMessage`.

---

## 5. Tecnologías y arquitectura

- Django y Django ORM.
- Django Templates y Bootstrap.
- SQLite como base de datos principal.
- Gestión de ficheros multimedia con `MEDIA_URL` y `MEDIA_ROOT`.
- Integración de videollamada embebida con Jitsi Meet External API.
- JavaScript para interacciones de interfaz y notificaciones.

---

## 6. Apartados de la memoria

- Introducción y motivación.
- Análisis de requisitos funcionales y no funcionales.
- Diseño general de la aplicación.
- Implementación por módulos.
- Pruebas y validación.
- Despliegue y configuración.
- Conclusiones y trabajo futuro.

---

Este documento refleja el estado actual del proyecto: vídeos, clases privadas, videollamada Jitsi, notificaciones, catálogo de guitarras, IA y administración.