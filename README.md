# Pluralia 📰

**Pluralia** es una API de agregación de noticias que recopila información de múltiples fuentes de medios españoles, clasificándolas por sesgo político y agrupándolas por temas para proporcionar una visión plural de la actualidad.

## 🎯 Características

- **Agregación de noticias**: Recopila noticias de 10+ medios españoles principales
- **Clasificación por sesgo**: Categoriza las fuentes según su orientación política (left, center, right)
- **Agrupación temática**: Agrupa noticias similares usando hashing de títulos
- **API REST**: Endpoints para consultar noticias y métricas
- **Base de datos PostgreSQL**: Almacenamiento persistente de artículos y fuentes
- **Docker**: Contenedorización completa para desarrollo y producción
- **Arquitectura Monorepo**: Servicios separados siguiendo Domain-Driven Design

## 🏗️ Arquitectura

El proyecto está estructurado como un **monorepo** siguiendo principios de **Domain-Driven Design (DDD)** y **Clean Architecture**:

- **libs/domain**: Código compartido del dominio (entidades, value objects, repositorios)
- **services/api**: Servicio de API REST (FastAPI)
- **services/ingest**: Servicio de ingesta de noticias desde feeds RSS
- **services/web**: Frontend web (pendiente de implementación)

### Tecnologías

- **FastAPI**: Framework web moderno y rápido para Python
- **SQLModel**: ORM que combina SQLAlchemy con Pydantic
- **PostgreSQL**: Base de datos relacional para persistencia
- **feedparser**: Biblioteca para parsear feeds RSS/Atom
- **Docker Compose**: Orquestación de servicios

## 📁 Estructura del Proyecto

```
pluralia/
├── libs/
│   └── domain/                    # Código compartido del dominio
│       ├── entities/              # Entidades de dominio (Source, Article, NewsGroup)
│       ├── value_objects/         # Value Objects (Bias, TopicHash)
│       ├── repositories/          # Interfaces de repositorios
│       └── errors/                # Excepciones de dominio
├── services/
│   ├── api/                       # Servicio API REST
│   │   ├── src/
│   │   │   ├── domain/            # Lógica de dominio específica del API
│   │   │   ├── application/       # Casos de uso
│   │   │   └── infrastructure/    # Implementaciones técnicas
│   │   │       ├── api/           # Controladores/rutas FastAPI
│   │   │       ├── repositories/  # Implementaciones de repositorios
│   │   │       └── database/      # Modelos SQLModel y configuración BD
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── ingest/                    # Servicio de ingesta
│   │   ├── src/
│   │   │   ├── domain/
│   │   │   ├── application/       # Casos de uso de ingesta
│   │   │   └── infrastructure/
│   │   │       ├── repositories/
│   │   │       ├── services/      # Servicios técnicos (RSS parser)
│   │   │       └── database/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── web/                       # Frontend (pendiente)
│       └── src/
├── docker-compose.yml             # Orquestación de todos los servicios
├── setup.py                       # Configuración para imports de libs
└── README.md                      # Este archivo
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
   docker-compose exec pluralia-ingest python -m services.ingest.src.main
   ```

5. **Accede a la documentación de la API**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Opción 2: Desarrollo Local (Sin Docker)

1. **Instala las dependencias**:
   ```bash
   # Instalar dependencias del API
   cd services/api
   pip install -r requirements.txt
   
   # Instalar dependencias del ingest
   cd ../ingest
   pip install -r requirements.txt
   ```

2. **Configura PostgreSQL**:
   - Instala PostgreSQL localmente
   - Crea una base de datos llamada `pluralia`
   - Configura las variables de entorno:
     ```bash
     export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/pluralia"
     export PYTHONPATH="${PYTHONPATH}:$(pwd)"
     ```

3. **Ejecuta la aplicación API**:
   ```bash
   cd services/api
   uvicorn services.api.src.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Ejecuta la ingesta**:
   ```bash
   cd services/ingest
   python -m services.ingest.src.main
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
      "id": "uuid",
      "title": "Título de la noticia",
      "link": "https://ejemplo.com/noticia",
      "description": "Descripción de la noticia",
      "published": "2024-01-01T12:00:00",
      "source": "El País",
      "bias": "left"
    }
  ]
}
```

## 🔧 Comandos Útiles

### Docker Compose

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f pluralia-api
docker-compose logs -f pluralia-ingest

# Parar servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Ejecutar ingesta manualmente
docker-compose exec pluralia-ingest python -m services.ingest.src.main

# Acceder a la base de datos
docker-compose exec db psql -U postgres -d pluralia
```

### Desarrollo

```bash
# Ejecutar ingesta de noticias
python -m services.ingest.src.main

# Ejecutar tests (cuando estén implementados)
pytest

# Formatear código
black services/ libs/

# Linting
flake8 services/ libs/
```

## 🗄️ Base de Datos

### Modelos Principales

- **Source**: Fuentes de noticias con su sesgo político
- **Article**: Artículos individuales
- **NewsGroup**: Grupos de noticias relacionadas por tema

### Migraciones

La base de datos se inicializa automáticamente al ejecutar la aplicación por primera vez.

## 🔄 Flujo de Datos

1. **Ingesta**: El servicio `ingest` parsea feeds RSS de múltiples fuentes
2. **Clasificación**: Cada fuente tiene un sesgo político asignado (left, center, right)
3. **Agrupación**: Los artículos se agrupan por similitud de título usando hash SHA256
4. **Almacenamiento**: Los datos se guardan en PostgreSQL
5. **API**: El servicio `api` expone los datos para consumo a través de endpoints REST

## 🏛️ Arquitectura del Dominio

El proyecto sigue **Domain-Driven Design (DDD)**:

- **Entidades**: `Source`, `Article`, `NewsGroup` - Objetos con identidad única
- **Value Objects**: `Bias`, `TopicHash` - Objetos inmutables sin identidad
- **Repositorios**: Interfaces en el dominio, implementaciones en infraestructura
- **Casos de Uso**: Lógica de aplicación orquestando operaciones de dominio

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
- Los feeds RSS se actualizan ejecutando el servicio de ingesta
- La agrupación de noticias usa hashing SHA256 de los títulos normalizados
- El código del dominio está en `libs/domain` y es compartido entre servicios
- Cada servicio tiene su propia implementación de repositorios en la capa de infraestructura

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
