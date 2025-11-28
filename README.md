# Sistema de Inventario (Python + Django)

**Sistema de Inventario** es una aplicación completa desarrollada con **Django** bajo el patrón **MVC**, diseñada para administrar inventarios, ventas, compras, productos, clientes, proveedores y almacenes desde un panel de administración intuitivo y moderno.

## Demo del Proyecto

[https://ecommerce.com/](https://ecommerce.pablogarciajc.com/)

| ![Imagen 1](https://pablogarciajc.com/wp-content/uploads/2025/09/ecommerce_11_11.webp) | ![Imagen 2](https://pablogarciajc.com/wp-content/uploads/2025/01/ecommerce_6_webp.png) |
|-----------|-----------|

## Funcionalidades Principales

- **Dashboard**: Panel principal con estadísticas en tiempo real, gráficos de ventas, productos más vendidos y resumen del inventario.
- **Productos**: Gestión completa de productos con código, nombre, descripción, categoría, precios de compra/venta y control de stock.
- **Categorías**: Organización de productos por categorías personalizables para mejor clasificación.
- **Clientes**: Administración de clientes con datos de contacto, historial de compras y seguimiento de transacciones.
- **Proveedores**: Gestión de proveedores con información de contacto y registro de compras realizadas.
- **Almacenes**: Control de múltiples almacenes con capacidad, ubicación y productos asignados.
- **Movimientos Inventario**: Registro detallado de entradas y salidas de productos con trazabilidad completa.
- **Roles**: Sistema de permisos y roles personalizables para control de acceso granular.
- **Ventas**: Registro de ventas con cliente, productos vendidos, cantidades, precios y métodos de pago.
- **Detalle Ventas**: Desglose completo de cada venta con productos, cantidades, subtotales e IVA.
- **Compras**: Gestión de compras a proveedores con productos, cantidades y costos.
- **Detalle Compras**: Desglose detallado de cada compra realizada con precios y totales.
- **Reportes**: Generación de reportes de ventas, compras, inventario y análisis financiero.
- **Configuración**: Gestión de usuarios del sistema, perfiles, contraseñas y parámetros generales.
- **Documentación**: Página completa con guía de funcionalidades, tecnologías usadas, arquitectura y usuarios de prueba.

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

- Tener **Docker** y **Docker Compose** instalados.
- **Make**: Utilizado para automatizar procesos y gestionar contenedores de manera más eficiente.

### Pasos de Instalación

1. Clona el repositorio desde GitHub.
2. Dentro del repositorio, encontrarás un archivo **Makefile** que contiene los comandos necesarios para iniciar y gestionar tu aplicación.
3. Usa los siguientes comandos de **Make** para interactuar con la aplicación:

   - **`make init-app`**: Inicializa los contenedores y configura la aplicación.
   - **`make up`**: Levanta la aplicación y sus contenedores asociados.
   - **`make down`**: Detiene los contenedores y apaga la aplicación.
   - **`make shell`**: Ingresa al contenedor para interactuar directamente con el sistema en su entorno de ejecución.
   - **`make install-dependencies`**: Instala todas las dependencias necesarias para disponer del sistema de logs y ejecutar pruebas.
   - **`make init-chatbot`**: Instala y configura el chatbot en el sistema.

4. Además de estos comandos, dentro del archivo **Makefile** puedes encontrar otros comandos que te permitirán interactuar de manera más específica con los contenedores y los diferentes servicios que conforman la aplicación.

5. Accede a los siguientes URL:
   - **Aplicación Web**: [http://localhost:8081/](http://localhost:8081/)
   - **PhpMyAdmin**: [http://localhost:8082/](http://localhost:8082/)

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
> _"El buen manejo de tus finanzas hoy construye la seguridad del mañana."_
