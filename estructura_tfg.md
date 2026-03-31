# Estructura Detallada del Proyecto TFG Flamenco

Este documento describe de forma detallada y extensa la estructura y los pasos clave para el desarrollo de una plataforma web de guitarra flamenca basada en Django. Incluye la organización de modelos, administración, formularios, vistas, funcionalidades, tecnologías y apartados recomendados para la memoria del TFG.

---

## 1. Modelos (`models.py`)

### 1.1. Autenticación y Perfil
- **User**: Utilizar el modelo de usuario de Django o un `AbstractUser` personalizado para mayor flexibilidad.
- **Profile**: Modelo extendido con los siguientes campos:
  - `user` (OneToOneField a User)
  - `display_name`
  - `bio`
  - `avatar` (imagen)
  - `nivel_guitarra` (opciones: principiante, intermedio, avanzado)
  - `pais`

### 1.2. Palos y Vídeos
- **PaloFlamenco**:
  - `nombre` (bulería, tangos, alegrías, etc.)
  - `descripcion`
  - `slug`
- **Video**:
  - `titulo`
  - `descripcion`
  - `palo` (ForeignKey a PaloFlamenco)
  - `autor` (ForeignKey a User)
  - `archivo_video` o `url_video`
  - `miniatura`
  - `duracion`
  - `fecha_publicacion`
  - `visibilidad` (público/privado)
  - `slug`

### 1.3. Interacción Social
- **Like**:
  - `usuario` (ForeignKey a User)
  - `video` (ForeignKey a Video)
  - `created_at`
  - Restricción de unicidad (`usuario`, `video`)
- **Comentario**:
  - `video`
  - `usuario`
  - `texto`
  - `created_at`, `updated_at`
  - `parent` (ForeignKey opcional para hilos)
- **ChatRoom**:
  - `nombre`
  - `video` (ForeignKey opcional)
  - `is_public`
- **ChatMessage**:
  - `room` (ForeignKey a ChatRoom)
  - `usuario`
  - `mensaje`
  - `timestamp`

### 1.4. Clases y Reservas
- **ClasePrivada**:
  - `profesor` (User)
  - `alumno` (User)
  - `titulo`, `descripcion`
  - `palo_principal` (ForeignKey a PaloFlamenco)
  - `fecha_hora_inicio`, `fecha_hora_fin`
  - `estado` (pendiente, confirmada, realizada, cancelada)
- **DisponibilidadProfesor**:
  - `profesor`
  - `dia_semana`
  - `hora_inicio`, `hora_fin`

### 1.5. Catálogo de Guitarras
- **Guitarra**:
  - `nombre`, `fabricante`, `descripcion`
  - `precio_aproximado`
  - `imagen`
  - `tipo_madera`
  - `nivel_recomendado`
  - `stock_simulado`

### 1.6. IA y Contenido Histórico
- **ArticuloFlamenco**:
  - `titulo`, `contenido`
  - `categoria` (historia, guitarras, palos, artistas)
  - `slug`
- **PreguntaIA**:
  - `usuario`
  - `texto_pregunta`
  - `respuesta_generada`
  - `timestamp`

---

## 2. Administración (`admin.py`)

Personalización del panel de administración para gestionar contenidos y usuarios avanzados:

- **PaloFlamencoAdmin**: `list_display = ("nombre", "slug")`, `prepopulated_fields = {"slug": ("nombre",)}`
- **VideoAdmin**: `list_display = ("titulo", "palo", "autor", "fecha_publicacion")`, filtros por palo y fecha, búsqueda por título.
- **ComentarioAdmin**: Moderación, filtro por video, usuario, fecha; acción para marcar como “aprobado/eliminado lógicamente”.
- **ClasePrivadaAdmin**: Filtros por profesor, alumno, estado; listado para ver la agenda de clases.
- **GuitarraAdmin**: `list_display = ("nombre", "fabricante", "precio_aproximado", "nivel_recomendado")`
- **ArticuloFlamencoAdmin**: Editor enriquecido (si usas plugin) y prepopulación de slug.
- **Opcional**: Añadir `InlineModelAdmin` para mostrar comentarios dentro del detalle de un vídeo.

---

## 3. Formularios (`forms.py`) y Validaciones

- **RegistroUsuarioForm**: Basado en `UserCreationForm`, con campos extra de Profile (nivel, país). Validación de emails únicos y contraseñas fuertes.
- **PerfilForm**: Edición de bio, avatar y nivel de guitarra.
- **VideoForm**
- **ComentarioForm**: Validación de longitud mínima y filtro de lenguaje ofensivo.
- **ClasePrivadaForm**: Validación de fechas (no en el pasado), solapamiento de clases y disponibilidad del profesor.
- **GuitarraForm (solo admin)**: Validar que el precio sea positivo.

---

## 4. Vistas (`views.py`) y Funcionalidad

### 4.1. Sección Vídeos
- Listado de vídeos por palo (paginado)
- Detalle de vídeo con reproductor, lista de comentarios, formulario para comentar, botón de like/unlike (AJAX), enlace a sala de chat en tiempo real

### 4.2. Sección Chat en Tiempo Real
- Uso de Django Channels para WebSockets
- Vista de sala: lista de mensajes, frontend JS para WebSocket

### 4.3. Sección Clases Privadas
- Vista calendario/listado de próximas clases
- Vista para solicitar clase (formulario, email de confirmación, calendario)

### 4.4. Sección Guitarras
- Listado con filtros (fabricante, nivel, precio)
- Detalle con foto y descripción

### 4.5. Sección IA Flamenca
- Buscador tipo “haz una pregunta”
- Busca primero en ArticuloFlamenco, si no hay info llama a backend IA y guarda en PreguntaIA
- Muestra respuestas formateadas

---

## 5. Tecnologías y Arquitectura

- Django + Django ORM
- Django Templates + Bootstrap
- Gestión de ficheros multimedia (`MEDIA_URL`, `MEDIA_ROOT`)
- Django Channels + Redis para chat
- Integración IA (API real o backend simulado)

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

Este documento sirve como guía detallada para el desarrollo y documentación de la plataforma TFG Flamenco, asegurando que cada aspecto funcional y técnico esté bien definido y estructurado.