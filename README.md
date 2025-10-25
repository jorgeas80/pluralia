# Pluralia 📰

**Pluralia** es una API de agregación de noticias que recopila información de múltiples fuentes de medios españoles, clasificándolas por sesgo político y agrupándolas por temas para proporcionar una visión plural de la actualidad.

## 🎯 Características

- **Agregación de noticias**: Recopila noticias de 10+ medios españoles principales
- **Clasificación por sesgo**: Categoriza las fuentes según su orientación política (left, center, right)
- **Agrupación temática**: Agrupa noticias similares usando hashing de títulos
- **API REST**: Endpoints para consultar noticias y métricas
- **Base de datos PostgreSQL**: Almacenamiento persistente de artículos y fuentes
- **Docker**: Contenedorización completa para desarrollo y producción

## 🏗️ Arquitectura

El proyecto está estructurado con:

- **FastAPI**: Framework web moderno y rápido para Python
- **SQLModel**: ORM que combina SQLAlchemy con Pydantic
- **PostgreSQL**: Base de datos relacional para persistencia
- **feedparser**: Biblioteca para parsear feeds RSS/Atom
- **Docker Compose**: Orquestación de servicios

## 📁 Estructura del Proyecto

```
pluralia/
├── api/
│   └── app/
│       ├── main.py          # Aplicación FastAPI principal
│       ├── routes.py        # Endpoints de la API
│       ├── models.py        # Modelos de datos (SQLModel)
│       ├── db.py           # Configuración de base de datos
│       ├── ingest.py       # Script de ingesta de noticias
│       └── rss.py          # Utilidades RSS (vacío)
├── docker-compose.yml      # Orquestación de servicios
├── Dockerfile             # Imagen de la aplicación
└── README.md              # Este archivo
```

## 🚀 Instalación y Desarrollo Local

### Prerrequisitos

- **Docker** y **Docker Compose**
- **Python 3.11+** (para desarrollo local sin Docker)
- **PostgreSQL** (si ejecutas sin Docker)

### Opción 1: Desarrollo con Docker (Recomendado)

1. **Clona el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd pluralia
   ```

2. **Levanta los servicios**:
   ```bash
   docker-compose up -d
   ```

3. **Verifica que todo funciona**:
   ```bash
   # Verificar que la API responde
   curl http://localhost:8000/health
   
   # Verificar que la base de datos está disponible
   docker-compose logs db
   ```

4. **Ejecuta la ingesta inicial de noticias**:
   ```bash
   docker-compose exec pluralia-api python -m api.app.ingest
   ```

5. **Accede a la documentación de la API**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Opción 2: Desarrollo Local (Sin Docker)

1. **Instala las dependencias**:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

2. **Configura PostgreSQL**:
   - Instala PostgreSQL localmente
   - Crea una base de datos llamada `pluralia`
   - Configura las variables de entorno:
     ```bash
     export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/pluralia"
     ```

3. **Ejecuta la aplicación**:
   ```bash
   cd api
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Ejecuta la ingesta**:
   ```bash
   python -m app.ingest
   ```

## 📊 Endpoints de la API

### `GET /health`
Verifica el estado de la API.

**Respuesta**:
```json
{
  "status": "ok"
}
```

### `GET /news`
Obtiene noticias recientes de múltiples fuentes.

**Parámetros**:
- `limit` (opcional): Número de noticias por fuente (default: 20)

**Respuesta**:
```json
{
  "news": [
    {
      "title": "Título de la noticia",
      "link": "https://ejemplo.com/noticia",
      "published": "Mon, 01 Jan 2024 12:00:00 GMT",
      "source": "El País"
    }
  ]
}
```

## 🔧 Comandos Útiles

### Docker Compose

```bash
# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Reconstruir imagen
docker-compose build --no-cache

# Ejecutar comando en el contenedor
docker-compose exec pluralia-api <comando>

# Acceder a la base de datos
docker-compose exec db psql -U postgres -d pluralia
```

### Desarrollo

```bash
# Ejecutar ingesta de noticias
python -m api.app.ingest

# Ejecutar tests (cuando estén implementados)
pytest

# Formatear código
black api/

# Linting
flake8 api/
```

## 🗄️ Base de Datos

### Modelos Principales

- **Source**: Fuentes de noticias con su sesgo político
- **Article**: Artículos individuales
- **NewsGroup**: Grupos de noticias relacionadas por tema

### Migraciones

La base de datos se inicializa automáticamente al ejecutar la aplicación por primera vez.

## 🔄 Flujo de Datos

1. **Ingesta**: El script `ingest.py` parsea feeds RSS de múltiples fuentes
2. **Clasificación**: Cada fuente tiene un sesgo político asignado
3. **Agrupación**: Los artículos se agrupan por similitud de título usando hash
4. **Almacenamiento**: Los datos se guardan en PostgreSQL
5. **API**: Los endpoints exponen los datos para consumo

## 🛠️ Tecnologías Utilizadas

- **Python 3.11**
- **FastAPI** - Framework web
- **SQLModel** - ORM y validación
- **PostgreSQL** - Base de datos
- **feedparser** - Parseo de feeds RSS
- **Docker** - Contenedorización
- **Uvicorn** - Servidor ASGI

## 📝 Notas de Desarrollo

- El proyecto usa **SQLModel** que combina SQLAlchemy con Pydantic
- Los feeds RSS se actualizan manualmente ejecutando el script de ingesta
- La agrupación de noticias usa hashing SHA256 de los títulos normalizados
- El proyecto está preparado para escalar con más fuentes y funcionalidades

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Desarrollado con ❤️ para promover el pluralismo informativo**
