# Sistema de Gestión de Inventario (Python + Django)

**Sistema de Gestión de Inventario** es una aplicación completa desarrollada con **Django** bajo el patrón **MVC**, diseñada para administrar inventarios, ventas, compras, productos, clientes, proveedores y almacenes desde un panel de administración intuitivo y moderno.

## Demo del Proyecto

[http://localhost:8081/](http://localhost:8081/)

| ![Dashboard](https://via.placeholder.com/400x250?text=Dashboard+con+Estadísticas) | ![Gestión de Productos](https://via.placeholder.com/400x250?text=Gestión+de+Productos) |
|-----------|-----------|

## Funcionalidades Principales

- **Dashboard**
- **Productos**
- **Categorías**
- **Clientes**
- **Proveedores**
- **Almacenes**
- **Movimientos Inventario**
- **Roles**
- **Ventas**
- **Detalle Ventas**
- **Compras**
- **Detalle Compras**
- **Reportes**
- **Configuración**

### Roles de Usuario Iniciales

El sistema está diseñado con **roles personalizables**:

1. **Administrador**: Acceso completo a todos los módulos del sistema
2. **Vendedor**: Acceso a ventas, clientes y consulta de productos
3. **Almacenero**: Gestión de inventario, movimientos y almacenes
4. **Supervisor**: Visualización de reportes y estadísticas

## Tecnologías Usadas

| **Tecnología**             | **Descripción**                                                                                                                                                   |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Django 5.0**             | Framework web de alto nivel para Python que fomenta el desarrollo rápido y el diseño limpio.                                                                     |
| **Python 3.11**            | Lenguaje de programación potente y versátil para desarrollo backend.                                                                                              |
| **MySQL 8.0**              | Sistema de gestión de bases de datos relacional robusto y escalable.                                                                                              |
| **Docker & Docker Compose**| Plataforma de contenerización para desarrollo, envío y ejecución de aplicaciones de forma aislada.                                                                |
| **Make**                   | Herramienta de automatización de tareas que simplifica comandos complejos.                                                                                        |
| **phpMyAdmin**             | Interfaz web para administración de bases de datos MySQL.                                                                                                         |

---

## Usuarios Ficticios para Pruebas

| **Nombre**                     | **Usuario**                       | **Contraseña** | **Rol**         |
|---------------------------------|-----------------------------------|----------------|-----------------|
| Administrador del Sistema       | admin                            | admin123       | Administrador   |
| Juan Pérez                      | jperez                           | vendedor123    | Vendedor        |
| María González                  | mgonzalez                        | almacen123     | Almacenero      |

---

## Instalación

### Requisitos Previos

- Tener **Docker** y **Docker Compose** instalados
- **Make**: Para automatizar comandos
- Puerto **8081** (aplicación) y **8082** (phpMyAdmin) disponibles

### Pasos de Instalación

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/PabloGarciaJC/python.git
   cd python
   ```

2. **Comandos disponibles en el Makefile**

   - **`make up`**: Levanta todos los contenedores (aplicación y base de datos)
   - **`make down`**: Detiene y elimina los contenedores
   - **`make restart`**: Reinicia los contenedores
   - **`make logs`**: Muestra los logs de la aplicación
   - **`make shell`**: Accede al contenedor de Python
   - **`make mysql`**: Accede al contenedor de MySQL
   - **`make ps`**: Lista los contenedores en ejecución

3. **Inicia la aplicación**
   ```bash
   make up
   ```

4. **Accede a las URLs**
   - **Aplicación Web**: [http://localhost:8081/](http://localhost:8081/)
   - **phpMyAdmin**: [http://localhost:8082/](http://localhost:8082/)
     - Servidor: `mysql`
     - Usuario: `pablogarciajcuser`
     - Contraseña: `pablogarciajcpassword`
     - Base de datos: `pablogarciajcbd`

5. **Credenciales de acceso inicial**
   - Usuario: `admin`
   - Contraseña: `admin123`

---

## Arquitectura del Sistema

### Patrón MVC

- **Models**: Lógica de acceso a datos (app/models/)
- **Views**: Renderizado HTML (app/views/)
- **Controllers**: Lógica de negocio (app/controllers/)

### Base de Datos

El sistema utiliza **14 tablas principales**:

- usuarios, roles, clientes, proveedores
- productos, categorias, almacenes
- ventas, detalle_ventas
- compras, detalle_compras
- movimientos_inventario

### Seguridad

- Protección CSRF en formularios
- Validación de sesiones
- Sanitización de inputs
- Control de acceso por roles

---

## Contáctame / Sígueme en mis redes sociales

| Red Social   | Descripción                                              | Enlace                   |
|--------------|----------------------------------------------------------|--------------------------|
| **Facebook** | Conéctate y mantente al tanto de mis actualizaciones.    | [Presiona aquí](https://www.facebook.com/PabloGarciaJC) |
| **YouTube**  | Fundamentos de la programación, tutoriales y noticias.   | [Presiona aquí](https://www.youtube.com/@pablogarciajc)     |
| **Página Web** | Más información sobre mis proyectos y servicios.        | [Presiona aquí](https://pablogarciajc.com/)              |
| **LinkedIn** | Sigue mi carrera profesional y establece conexiones.     | [Presiona aquí](https://www.linkedin.com/in/pablogarciajc) |
| **Instagram**| Fotos, proyectos y contenido relacionado.                 | [Presiona aquí](https://www.instagram.com/pablogarciajc) |
| **Twitter**  | Proyectos, pensamientos y actualizaciones.                | [Presiona aquí](https://x.com/PabloGarciaJC?t=lct1gxvE8DkqAr8dgxrHIw&s=09)   |

---
> _"La gestión eficiente del inventario es clave para el éxito de cualquier negocio."_
