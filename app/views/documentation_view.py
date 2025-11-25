from django.http import HttpResponse
from app.views.layout import Layout

class DocumentationView:
    """Vista de Documentación del Sistema"""
    
    @staticmethod
    def index(user, request_path):
        """Renderiza la página de documentación completa"""
        
        content = f"""
        <div class="documentation-container">
            <h1 class="doc-main-title"><i class="fas fa-book"></i> Documentación del Sistema</h1>
            <p class="doc-subtitle">Sistema de Gestión de Inventario - Guía Completa de Funcionalidades y Tecnologías</p>
            
            <!-- Funcionalidades -->
            <section class="doc-section">
                <h2 class="doc-section-title"><i class="fas fa-star"></i> ¿Qué funcionalidades ofrece este sistema?</h2>
                <div class="doc-grid">
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-tachometer-alt"></i> Dashboard</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Panel principal con estadísticas en tiempo real: productos, ventas del mes, compras y clientes. Incluye alertas de stock bajo y últimas transacciones.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-box"></i> Gestión de Productos</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>CRUD completo de productos con código, nombre, categoría, precios de compra/venta, stock actual y mínimo, y asignación de proveedor.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-tags"></i> Categorías</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Organiza tus productos por categorías personalizadas. Controla el estado activo/inactivo de cada categoría.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-users"></i> Clientes</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Administra tu cartera de clientes con datos completos: nombre, documento, teléfono, email, dirección y estado.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-truck"></i> Proveedores</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Gestiona proveedores con RUC, datos de contacto y seguimiento de estado. Vincula productos a sus proveedores.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-warehouse"></i> Almacenes</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Control de múltiples almacenes con ubicación, capacidad y seguimiento de movimientos de inventario.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-shopping-cart"></i> Compras</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Registro de compras a proveedores con múltiples productos, control de estados (pendiente/completada/cancelada) y notas.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-cash-register"></i> Ventas</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Sistema completo de ventas con selección de productos, cálculo automático de totales, tipos de pago y gestión de estados.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-exchange-alt"></i> Movimientos de Inventario</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Seguimiento detallado de entradas, salidas y ajustes de inventario con referencias, motivos y registro de usuario responsable.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-chart-bar"></i> Reportes</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Genera reportes de ventas, compras y productos por rangos de fecha. Visualiza tendencias y analiza tu negocio.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-user-shield"></i> Roles y Permisos</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Sistema de roles (Administrador, Gerente, Vendedor, Almacenero) con permisos específicos para cada uno.</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-cog"></i> Configuración</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Panel de administración de usuarios, gestión de perfil personal, cambio de contraseña y estadísticas del sistema.</p>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Tecnologías -->
            <section class="doc-section">
                <h2 class="doc-section-title"><i class="fas fa-laptop-code"></i> Tecnologías Empleadas para el Desarrollo</h2>
                <div class="doc-grid">
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-python"></i> Python 3.11</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Lenguaje de programación moderno y versátil utilizado como base del backend. Ofrece legibilidad, eficiencia y un ecosistema robusto de librerías.</p>
                            <p><a href="https://docs.python.org/3/" target="_blank" class="doc-link">Documentación de Python</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-server"></i> Django 5.0</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Framework web de alto nivel que fomenta el desarrollo rápido y el diseño limpio. Incluye ORM, sistema de autenticación y gestión de sesiones.</p>
                            <p><a href="https://docs.djangoproject.com/en/5.0/" target="_blank" class="doc-link">Documentación de Django</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-database"></i> MySQL</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Sistema de gestión de bases de datos relacional de código abierto. Garantiza integridad de datos con transacciones ACID y soporte de claves foráneas.</p>
                            <p><a href="https://dev.mysql.com/doc/" target="_blank" class="doc-link">Documentación de MySQL</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-paint-brush"></i> CSS3 Modular</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Sistema de estilos organizado en módulos (main.css, forms.css, dashboard.css, auth.css) con 100+ clases utilitarias sin dependencias externas.</p>
                            <p><a href="https://developer.mozilla.org/es/docs/Web/CSS" target="_blank" class="doc-link">Documentación de CSS</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-font-awesome"></i> Font Awesome 6.4</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Biblioteca de iconos vectoriales y logotipos. Proporciona más de 2,000 iconos escalables para una interfaz moderna y profesional.</p>
                            <p><a href="https://fontawesome.com/docs" target="_blank" class="doc-link">Documentación de Font Awesome</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-docker"></i> Docker</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Plataforma de contenedores que garantiza consistencia entre entornos de desarrollo, pruebas y producción. Facilita despliegue y escalabilidad.</p>
                            <p><a href="https://docs.docker.com/" target="_blank" class="doc-link">Documentación de Docker</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-layer-group"></i> Docker Compose</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Herramienta para definir y ejecutar aplicaciones Docker multi-contenedor. Orquesta MySQL, PhpMyAdmin y el servidor Python.</p>
                            <p><a href="https://docs.docker.com/compose/" target="_blank" class="doc-link">Documentación de Docker Compose</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-cogs"></i> Make</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Sistema de automatización que simplifica comandos complejos. Comandos principales: make up, make down, make restart, make logs, make init-app.</p>
                            <p><a href="https://www.gnu.org/software/make/manual/" target="_blank" class="doc-link">Documentación de Make</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-database"></i> PhpMyAdmin</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Herramienta web para administración de MySQL. Permite ejecutar consultas SQL, gestionar tablas y visualizar datos de forma gráfica.</p>
                            <p><a href="https://www.phpmyadmin.net/docs/" target="_blank" class="doc-link">Documentación de PhpMyAdmin</a></p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-shield-alt"></i> Seguridad</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Implementa hash SHA-256 para contraseñas, protección CSRF, control de sesiones, validación de datos y sanitización de entradas SQL.</p>
                            <p><a href="https://owasp.org/www-project-top-ten/" target="_blank" class="doc-link">OWASP Top 10</a></p>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Arquitectura -->
            <section class="doc-section">
                <h2 class="doc-section-title"><i class="fas fa-sitemap"></i> Arquitectura del Sistema</h2>
                <div class="doc-grid">
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-project-diagram"></i> Patrón MVC</h3>
                        </div>
                        <div class="doc-card-body">
                            <p><strong>Models:</strong> Lógica de negocio y acceso a datos (User, Product, Sale, Purchase, etc.)</p>
                            <p><strong>Views:</strong> Generación de HTML dinámico sin templates (AuthView, DashboardView, ProductView, etc.)</p>
                            <p><strong>Controllers:</strong> Coordinan Models y Views, gestionan requests HTTP (auth_controller, product_controller, etc.)</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-folder-tree"></i> Estructura de Directorios</h3>
                        </div>
                        <div class="doc-card-body">
                            <p><strong>app/controllers/:</strong> 15 controladores para cada módulo</p>
                            <p><strong>app/models/:</strong> 15 modelos de datos</p>
                            <p><strong>app/views/:</strong> 15 vistas + Layout compartido</p>
                            <p><strong>app/static/:</strong> CSS (main, forms, dashboard, auth) y JS</p>
                            <p><strong>config/:</strong> URLs, database, settings</p>
                            <p><strong>.docker/:</strong> Configuración de contenedores</p>
                        </div>
                    </div>
                    
                    <div class="doc-card">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-database"></i> Base de Datos</h3>
                        </div>
                        <div class="doc-card-body">
                            <p><strong>12 tablas:</strong> usuarios, roles, productos, categorias, clientes, proveedores, almacenes, compras, ventas, detalle_compras, detalle_ventas, movimientos_inventario</p>
                            <p><strong>Relaciones:</strong> Claves foráneas con integridad referencial</p>
                            <p><strong>Índices:</strong> Optimización en campos de búsqueda frecuente</p>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Usuarios de Prueba -->
            <section class="doc-section">
                <h2 class="doc-section-title"><i class="fas fa-users-cog"></i> Usuarios Ficticios para Pruebas</h2>
                <p class="doc-note"><i class="fas fa-info-circle"></i> Todos los usuarios tienen la contraseña: <code>password</code></p>
                <div class="doc-grid">
                    <div class="doc-card doc-card-user">
                        <div class="doc-card-header bg-gradient-purple">
                            <h3><i class="fas fa-user-shield"></i> Administrador</h3>
                        </div>
                        <div class="doc-card-body">
                            <p><strong>Email:</strong> admin@inventario.com</p>
                            <p><strong>Usuario:</strong> admin</p>
                            <p><strong>Contraseña:</strong> password</p>
                            <p><strong>Rol:</strong> Administrador</p>
                        </div>
                    </div>
                                        
                    <div class="doc-card doc-card-user">
                        <div class="doc-card-header bg-gradient-pink">
                            <h3><i class="fas fa-user-tie"></i> Juan Pérez</h3>
                        </div>
                        <div class="doc-card-body">
                            <p><strong>Email:</strong> jperez@inventario.com</p>
                            <p><strong>Usuario:</strong> jperez</p>
                            <p><strong>Contraseña:</strong> password</p>
                            <p><strong>Rol:</strong> Gerente</p>
                        </div>
                    </div>
                    
                    <div class="doc-card doc-card-user">
                        <div class="doc-card-header bg-gradient-cyan">
                            <h3><i class="fas fa-user"></i> María González</h3>
                        </div>
                        <div class="doc-card-body">
                            <p><strong>Email:</strong> mgonzalez@inventario.com</p>
                            <p><strong>Usuario:</strong> mgonzalez</p>
                            <p><strong>Contraseña:</strong> password</p>
                            <p><strong>Rol:</strong> Vendedor</p>
                        </div>
                    </div>
                    
                    <div class="doc-card doc-card-user">
                        <div class="doc-card-header bg-gradient-green">
                            <h3><i class="fas fa-user"></i> Carlos Rodríguez</h3>
                        </div>
                        <div class="doc-card-body">
                            <p><strong>Email:</strong> crodriguez@inventario.com</p>
                            <p><strong>Usuario:</strong> crodriguez</p>
                            <p><strong>Contraseña:</strong> password</p>
                            <p><strong>Rol:</strong> Almacenero</p>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Datos Demo -->
            <section class="doc-section">
                <h2 class="doc-section-title"><i class="fas fa-database"></i> Base de Datos de Demostración</h2>
                <div class="doc-grid doc-grid-stats">
                    <div class="doc-stat-card">
                        <div class="doc-stat-icon bg-gradient-purple">
                            <i class="fas fa-box"></i>
                        </div>
                        <div class="doc-stat-info">
                            <h3>80</h3>
                            <p>Productos</p>
                        </div>
                    </div>
                    
                    <div class="doc-stat-card">
                        <div class="doc-stat-icon bg-gradient-pink">
                            <i class="fas fa-users"></i>
                        </div>
                        <div class="doc-stat-info">
                            <h3>25</h3>
                            <p>Clientes</p>
                        </div>
                    </div>
                    
                    <div class="doc-stat-card">
                        <div class="doc-stat-icon bg-gradient-cyan">
                            <i class="fas fa-shopping-cart"></i>
                        </div>
                        <div class="doc-stat-info">
                            <h3>20</h3>
                            <p>Compras</p>
                        </div>
                    </div>
                    
                    <div class="doc-stat-card">
                        <div class="doc-stat-icon bg-gradient-green">
                            <i class="fas fa-cash-register"></i>
                        </div>
                        <div class="doc-stat-info">
                            <h3>35</h3>
                            <p>Ventas</p>
                        </div>
                    </div>
                    
                    <div class="doc-stat-card">
                        <div class="doc-stat-icon bg-gradient-purple">
                            <i class="fas fa-truck"></i>
                        </div>
                        <div class="doc-stat-info">
                            <h3>5</h3>
                            <p>Proveedores</p>
                        </div>
                    </div>
                    
                    <div class="doc-stat-card">
                        <div class="doc-stat-icon bg-gradient-pink">
                            <i class="fas fa-tags"></i>
                        </div>
                        <div class="doc-stat-info">
                            <h3>7</h3>
                            <p>Categorías</p>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Contacto -->
            <section class="doc-section">
                <h2 class="doc-section-title"><i class="fas fa-address-card"></i> Contáctame / Sígueme en Redes Sociales</h2>
                <div class="doc-grid">
                    <div class="doc-card doc-card-social">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-github"></i> GitHub</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Visita mi perfil en GitHub para ver mis proyectos y contribuciones al código abierto.</p>
                            <a href="https://github.com/PabloGarciaJC" target="_blank" class="btn btn-primary">
                                <i class="fab fa-github"></i> Ir a GitHub
                            </a>
                        </div>
                    </div>
                    
                    <div class="doc-card doc-card-social">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-linkedin"></i> LinkedIn</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Conéctate conmigo en LinkedIn para seguir mi carrera profesional y establecer conexiones.</p>
                            <a href="https://www.linkedin.com/in/pablogarciajc/" target="_blank" class="btn btn-primary">
                                <i class="fab fa-linkedin"></i> Ir a LinkedIn
                            </a>
                        </div>
                    </div>
                    
                    <div class="doc-card doc-card-social">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-youtube"></i> YouTube</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Visita mi canal de YouTube para ver videos sobre desarrollo web, tutoriales y más.</p>
                            <a href="https://www.youtube.com/channel/UC5I4oY7BeNwT4gBu1ZKsEhw" target="_blank" class="btn btn-primary">
                                <i class="fab fa-youtube"></i> Ir a YouTube
                            </a>
                        </div>
                    </div>
                    
                    <div class="doc-card doc-card-social">
                        <div class="doc-card-header">
                            <h3><i class="fas fa-globe"></i> Página Web</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Visita mi página web personal donde encontrarás más sobre mis proyectos y servicios.</p>
                            <a href="https://pablogarciajc.com/" target="_blank" class="btn btn-primary">
                                <i class="fas fa-globe"></i> Ir a mi sitio web
                            </a>
                        </div>
                    </div>
                    
                    <div class="doc-card doc-card-social">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-facebook"></i> Facebook</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Conéctate conmigo en Facebook y mantente al tanto de mis actualizaciones personales y profesionales.</p>
                            <a href="https://www.facebook.com/PabloGarciaJC" target="_blank" class="btn btn-primary">
                                <i class="fab fa-facebook"></i> Ir a Facebook
                            </a>
                        </div>
                    </div>
                    
                    <div class="doc-card doc-card-social">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-instagram"></i> Instagram</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Sigue mi cuenta de Instagram para ver fotos, proyectos y más contenido relacionado con mi trabajo.</p>
                            <a href="https://www.instagram.com/pablogarciajc/" target="_blank" class="btn btn-primary">
                                <i class="fab fa-instagram"></i> Ir a Instagram
                            </a>
                        </div>
                    </div>
                    
                    <div class="doc-card doc-card-social">
                        <div class="doc-card-header">
                            <h3><i class="fab fa-twitter"></i> Twitter</h3>
                        </div>
                        <div class="doc-card-body">
                            <p>Sigue mi cuenta de Twitter para estar al tanto de mis proyectos, pensamientos y actualizaciones.</p>
                            <a href="https://x.com/PabloGarciaJC?t=lct1gxvE8DkqAr8dgxrHIw&s=09" target="_blank" class="btn btn-primary">
                                <i class="fab fa-twitter"></i> Ir a Twitter
                            </a>
                        </div>
                    </div>
                </div>
            </section>
        </div>
        """
        
        return HttpResponse(Layout.render('Documentación', user, 'documentacion', content))
