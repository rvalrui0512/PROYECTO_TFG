
# Estructura Detallada del Proyecto TFG Flamenco (Actualizada)

Este documento describe la estructura real y las funcionalidades implementadas en la plataforma web de guitarra flamenca basada en Django.

---

## 1. Modelos (`models.py`)

### 1.1. Autenticación y Perfil
- **User**: Modelo de usuario estándar de Django.
- **Profile**: Extiende al usuario con:
  - `user` (OneToOneField a User)
  - `display_name`, `bio`, `avatar`, `pais`

### 1.2. Palos y Vídeos
- **PaloFlamenco**: `nombre`, `descripcion`, `slug`
- **Video**: `titulo`, `descripcion`, `palo_flamenco`, `autor`, `miniatura`, `archivo`, `duracion`, `fecha_publicacion`, `visibilidad`, `slug`

### 1.3. Interacción Social
- **Like**: `usuario`, `video`, `fecha` (único por usuario y vídeo)
- **Comentario**: `usuario`, `video`, `texto`, `fecha_creacion`, `fecha_actualizacion`, `padre` (para hilos)
- **ChatRoom**: `nombre`, `video`, `es_publico`
- **ChatMessage**: `chatroom`, `usuario`, `mensaje`, `timestamp`
- **Favorito**: genérico para vídeos y otros objetos


### 1.4. Clases y Reservas
- **ClasePrivada**: `profesor`, `alumno`, `titulo`, `descripcion`, `palo_flamenco`, `fecha_inicio`, `fecha_fin`, `estado`
- **DisponibilidadProfesor**: `profesor`, `dia_semana`, `hora_inicio`, `hora_fin`

### 1.5. Catálogo de Guitarras
- **Guitarra**: `marca`, `modelo`, `tipo`, `descripcion`, `precio`, `stock`, `imagen`

### 1.6. IA y Contenido Histórico
- **ArticuloFlamenco**: `titulo`, `contenido`, `categoria`, `slug`
- **PreguntaIA**: `usuario`, `pregunta`, `respuesta`, `timestamp`

---

## 2. Administración (`admin.py`)

Panel de administración personalizado para gestionar todos los modelos principales, con filtros, búsquedas y acciones rápidas.

---

## 3. Formularios (`forms.py`) y Validaciones

- **RegistroUsuarioForm**: Registro de usuario con validación de email único y contraseña fuerte.
- **ProfileForm**: Edición de perfil.
- **VideoForm**: Creación/edición de vídeos.
- **ComentarioForm**: Validación de longitud mínima y lenguaje ofensivo.
- **ClasePrivadaForm**: Validación de fechas y solapamiento de clases.
- **GuitarraForm**: Solo admin, valida precio positivo.

---

## 4. Vistas (`views.py`) y Funcionalidad

### 4.1. Sección Vídeos
- Listado de vídeos por palo (paginado y filtrado)
- Detalle de vídeo con reproductor, comentarios, likes, favoritos y miniatura
- Subida de vídeos (solo admin)

### 4.2. Sección Chat en Tiempo Real
- Chat por vídeo usando Django Channels (WebSockets)

### 4.3. Sección Clases Privadas
- Listado y detalle de clases privadas
- Solicitud y gestión de clases (solo admin/profesor)

### 4.4. Sección Guitarras
- Listado con filtros (modelo, tipo, precio)
- Detalle con foto, descripción y stock
- Añadir al carrito (simulado)

### 4.5. Sección IA Flamenca
- Buscador tipo “haz una pregunta”
- Responde con información de guitarras, historia, palos y artículos
- Guarda preguntas y respuestas en la base de datos

---

## 5. Tecnologías y Arquitectura

- Django + Django ORM
- Django Templates + Bootstrap
- Gestión de ficheros multimedia (`MEDIA_URL`, `MEDIA_ROOT`)
- Django Channels + Redis para chat
- Integración IA (backend propio)

---

## 6. Apartados de la Memoria

- Introducción y motivación
- Análisis de requisitos funcionales y no funcionales
- Diseño (diagramas de clases, navegación, casos de uso)
- Implementación (estructura de apps, modelos, forms, vistas, templates, Channels)
- Pruebas (tests de modelos y vistas)
- Despliegue (configuración para producción)
- Conclusiones y trabajo futuro

---

Este documento refleja la estructura y funcionamiento real del proyecto TFG Flamenco, incluyendo la gestión de vídeos, IA, catálogo de guitarras, clases privadas, interacción social y administración. Puedes añadir vídeos grabados y mejorar la presentación según lo necesites.