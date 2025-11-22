# CMS Ecommerce - Python/Flask

Sistema de gestión de contenidos para comercio electrónico desarrollado con Python, Flask y MySQL.

## 🚀 Stack Tecnológico

- **Backend**: Python 3.11 + Flask
- **Base de datos**: MySQL 9.3
- **ORM**: SQLAlchemy
- **Containerización**: Docker + Docker Compose
- **Automatización**: Make

## 📋 Requisitos Previos

- Docker y Docker Compose instalados
- Make para automatización de tareas

## 🛠️ Instalación

1. **Clonar el repositorio**

2. **Inicializar la aplicación**
```bash
make init-app
```

Este comando:
- Copia el archivo `.env.example` a `.env`
- Crea el enlace simbólico para las variables de entorno
- Levanta los contenedores
- Muestra las URLs de acceso

## 🎯 Comandos Disponibles

### Gestión de contenedores
```bash
make up              # Levantar contenedores
make down            # Detener contenedores
make restart         # Reiniciar contenedores
make ps              # Ver estado de contenedores
make logs            # Ver logs
make build           # Construir imágenes
make stop            # Detener sin eliminar
```

### Desarrollo
```bash
make shell           # Acceder al contenedor de Python
```

### Limpieza
```bash
make clean-docker    # Limpiar recursos Docker
```

## 🌐 URLs de Acceso

- **Aplicación**: http://localhost:5000/
- **phpMyAdmin**: http://localhost:8082/

## 📦 Dependencias Python

Las dependencias principales incluyen:
- Flask 3.0.0
- SQLAlchemy 2.0.23
- Flask-Login para autenticación
- pytest para testing
- gunicorn para producción

Ver `requirements.txt` completo en `.docker/requirements.txt`

## 🏗️ Estructura del Proyecto

```
.
├── app.py                      # Aplicación principal Flask
├── .docker/
│   ├── docker-compose.yml      # Configuración de servicios
│   ├── requirements.txt        # Dependencias Python
│   └── server/
│       ├── Dockerfile          # Imagen Python
│       └── bash/
│           └── terminal        # Configuración de shell
├── .env.example                # Variables de entorno template
├── Makefile                    # Comandos de automatización
└── README.md
```

## 🔧 Configuración

### Variables de Entorno (.env)

```env
PYTHON_APP_PORT=5000
PYTHON_VERSION=3.11
FLASK_ENV=development
FLASK_DEBUG=1
DB_DATABASE=ecommerce_pablogarciajc
MYSQL_USER=pablogarciajcbd
MYSQL_PASSWORD=password
```

## 🧪 Testing

```bash
# Dentro del contenedor
make shell
pytest
```

## 📝 Notas de Desarrollo

- El servidor Flask corre en modo debug en desarrollo
- Hot reload activado para cambios en tiempo real
- Volúmenes montados para desarrollo local
- MySQL configurado con persistencia de datos

## 👤 Autor

**Pablo García JC**

- [Sitio Web](https://pablogarciajc.com/)
- [LinkedIn](https://www.linkedin.com/in/pablogarciajc)
- [YouTube](https://www.youtube.com/@pablogarciajc)
- [GitHub](https://github.com/PabloGarciaJC)

---

> _"Code is poetry"_ 🐍
