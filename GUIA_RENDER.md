# 🚀 Guía de Despliegue en Render.com

## Pasos para desplegar tu proyecto Django en Render

### 1️⃣ Preparación local
```powershell
# Tu proyecto ya está configurado ✓
# Archivos creados:
# ✓ requirements.txt (con whitenoise y python-dotenv)
# ✓ settings.py (configurado para producción)
# ✓ render.yaml (configuración de despliegue)
# ✓ .env.example (plantilla de variables)
# ✓ Procfile (alternativa a render.yaml)
```

### 2️⃣ Subir a GitHub

```powershell
# Navega a tu proyecto
cd "c:\Users\rvalde01\OneDrive - dentsu\Desktop\PROYECTO_TFG"

# Inicializa Git si no lo has hecho
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Preparación para despliegue en Render"

# Push a tu repositorio (necesitas crear uno en GitHub)
git branch -M main
git remote add origin https://github.com/TU_USUARIO/tu-repo.git
git push -u origin main
```

### 3️⃣ Crear cuenta en Render

1. Ve a https://render.com
2. Sign Up (puedes usar GitHub para facilitar)
3. Autoriza Render a acceder a tu GitHub

### 4️⃣ Crear el servicio Web

1. Dashboard → New+ → Web Service
2. Conecta tu repositorio
3. Configura:
   - **Name**: tfg-flamenco
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn TFG_FLAMENCO.wsgi:application --bind 0.0.0.0:$PORT`

### 5️⃣ Configurar Variables de Entorno

En Render Dashboard → tu servicio → Environment

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-aleatoria-aqui

ALLOWED_HOSTS=tu-app.onrender.com

CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
```

**Para generar SECRET_KEY fuerte:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 6️⃣ Esperar el despliegue

- Render descargará el código
- Ejecutará `pip install -r requirements.txt`
- Ejecutará `python manage.py migrate`
- Ejecutará `python manage.py collectstatic --noinput`
- Iniciará la aplicación con gunicorn

### 7️⃣ Verificar que funciona

1. Abre tu URL: `https://tu-app.onrender.com`
2. Accede a `/admin` para probar
3. Revisa logs en: Dashboard → tu servicio → Logs

---

## ⚠️ Notas importantes

### Base de datos SQLite en Render
- Render usa almacenamiento **efímero**, así que SQLite se perderá en cada deploy
- **Solución**: Cambiar a PostgreSQL (gratis en Render)

**Para usar PostgreSQL:**
1. Render Dashboard → New+ → PostgreSQL
2. Copia la URL de conexión
3. En variables de entorno, modifica `settings.py` para usar:

```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

4. Instala: `pip install dj-database-url psycopg2-binary`

### Media files
- Los archivos subidos también se pierden en redeploys
- Considera usar AWS S3 o Cloudinary para guardar imágenes

### Archivos estáticos
- ✓ Ya está configurado con WhiteNoise
- ✓ Los CSS/JS se comprimen automáticamente

---

## 🔄 Despliegues futuros

Una vez configurado, cada `git push` a main desplegará automáticamente:

```powershell
git add .
git commit -m "Cambios"
git push origin main
# ¡Automáticamente en Render!
```

---

## 📝 Archivo .env.example
Actualiza con tus datos reales antes de desplegar:

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-super-segura-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,tu-app.onrender.com
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://tu-app.onrender.com
```

---

¿Necesitas ayuda con PostgreSQL o S3? 📧
