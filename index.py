import os
import hashlib
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import path
from django.middleware.csrf import get_token
import MySQLdb

# Configuración de Django con MySQL
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='mi-clave-secreta-super-segura',
        ALLOWED_HOSTS=['*'],
        ROOT_URLCONF=__name__,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': False,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                ],
            },
        }],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.getenv('DB_DATABASE', 'pablogarciajcbd'),
                'USER': os.getenv('MYSQL_USER', 'pablogarciajcuser'),
                'PASSWORD': os.getenv('MYSQL_PASSWORD', 'password'),
                'HOST': 'mysql',
                'PORT': '3306',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.sessions',
            'django.contrib.contenttypes',
        ],
        SESSION_ENGINE='django.contrib.sessions.backends.db',
        USE_TZ=True,
    )

# Conexión a MySQL
def get_db():
    return MySQLdb.connect(
        host='mysql',
        user=os.getenv('MYSQL_USER', 'pablogarciajcuser'),
        password=os.getenv('MYSQL_PASSWORD', 'password'),
        database=os.getenv('DB_DATABASE', 'pablogarciajcbd'),
        charset='utf8mb4'
    )

# Templates HTML integrados
CSS_STYLES = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        
        /* Navbar */
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .navbar-content { display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto; }
        .navbar h1 { font-size: 1.5rem; }
        .navbar-menu { display: flex; gap: 20px; align-items: center; }
        .navbar-menu a { color: white; text-decoration: none; padding: 8px 15px; border-radius: 5px; transition: background 0.3s; }
        .navbar-menu a:hover { background: rgba(255,255,255,0.2); }
        
        /* Sidebar */
        .layout { display: flex; min-height: calc(100vh - 70px); }
        .sidebar { width: 250px; background: white; padding: 20px; box-shadow: 2px 0 5px rgba(0,0,0,0.05); }
        .sidebar-menu { list-style: none; }
        .sidebar-menu li { margin: 10px 0; }
        .sidebar-menu a { display: block; padding: 12px 15px; color: #333; text-decoration: none; border-radius: 8px; transition: all 0.3s; }
        .sidebar-menu a:hover, .sidebar-menu a.active { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .sidebar-menu i { margin-right: 10px; }
        
        /* Main Content */
        .main-content { flex: 1; padding: 30px; }
        .card { background: white; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); }
        .card-header { font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #f0f0f0; }
        
        /* Stats Cards */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
        .stat-card h3 { font-size: 0.9rem; opacity: 0.9; margin-bottom: 10px; }
        .stat-card .value { font-size: 2.5rem; font-weight: bold; }
        
        /* Tables */
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #f0f0f0; }
        th { background: #f8f9fa; font-weight: 600; color: #667eea; }
        tr:hover { background: #f8f9fa; }
        
        /* Buttons */
        .btn { display: inline-block; padding: 10px 20px; border-radius: 8px; text-decoration: none; cursor: pointer; border: none; font-size: 14px; transition: all 0.3s; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
        .btn-success { background: #10b981; color: white; }
        .btn-danger { background: #ef4444; color: white; }
        .btn-warning { background: #f59e0b; color: white; }
        .btn-secondary { background: #6b7280; color: white; }
        
        /* Forms */
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 500; color: #374151; }
        .form-control { width: 100%; padding: 12px; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 14px; }
        .form-control:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
        
        /* Login Page */
        .login-container { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .login-card { background: white; padding: 40px; border-radius: 12px; width: 100%; max-width: 400px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        .login-card h2 { text-align: center; margin-bottom: 30px; color: #333; }
        
        /* Alerts */
        .alert { padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .alert-success { background: #d1fae5; color: #065f46; }
        .alert-error { background: #fee2e2; color: #991b1b; }
        .alert-info { background: #dbeafe; color: #1e40af; }
        
        /* Badge */
        .badge { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
        .badge-success { background: #d1fae5; color: #065f46; }
        .badge-danger { background: #fee2e2; color: #991b1b; }
        .badge-warning { background: #fef3c7; color: #92400e; }
    </style>
"""

def render_login(error=None, csrf_token=''):
    error_html = f'<div class="alert alert-error">{error}</div>' if error else ''
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Inventario - Login</title>
    {CSS_STYLES}
</head>
<body>
<div class="login-container">
    <div class="login-card">
        <h2>🔐 Sistema de Inventario</h2>
        {error_html}
        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <div class="form-group">
                <label>Usuario</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Contraseña</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">Iniciar Sesión</button>
        </form>
    </div>
</div>
</body>
</html>
"""

def render_dashboard(user, request_path, content):
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Inventario</title>
    {CSS_STYLES}
</head>
<body>
<div class="navbar">
    <div class="navbar-content">
        <h1>📦 Sistema de Inventario</h1>
        <div class="navbar-menu">
            <span>{user['nombre_completo']} ({user['rol']})</span>
            <a href="/logout/">Cerrar Sesión</a>
        </div>
    </div>
</div>
<div class="layout">
    <div class="sidebar">
        <ul class="sidebar-menu">
            <li><a href="/" class="{'active' if request_path == '/' else ''}">📊 Dashboard</a></li>
            <li><a href="/productos/" class="{'active' if 'productos' in request_path else ''}">🏷️ Productos</a></li>
            <li><a href="/categorias/" class="{'active' if 'categorias' in request_path else ''}">📑 Categorías</a></li>
            <li><a href="/proveedores/" class="{'active' if 'proveedores' in request_path else ''}">🚚 Proveedores</a></li>
            <li><a href="/clientes/" class="{'active' if 'clientes' in request_path else ''}">👥 Clientes</a></li>
            <li><a href="/almacenes/" class="{'active' if 'almacenes' in request_path else ''}">🏭 Almacenes</a></li>
            <li><a href="/ventas/" class="{'active' if 'ventas' in request_path else ''}">💰 Ventas</a></li>
            <li><a href="/compras/" class="{'active' if 'compras' in request_path else ''}">🛒 Compras</a></li>
            <li><a href="/movimientos/" class="{'active' if 'movimientos' in request_path else ''}">📦 Movimientos</a></li>
            <li><a href="/usuarios/" class="{'active' if 'usuarios' in request_path else ''}">👤 Usuarios</a></li>
        </ul>
    </div>
    <div class="main-content">
        <div class="container">
            {content}
        </div>
    </div>
</div>
</body>
</html>
"""

# Middleware de autenticación simple
def require_auth(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

# Vistas
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            db = get_db()
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("""
                SELECT u.*, r.nombre as rol_nombre
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
                WHERE u.username = %s AND u.activo = 1
            """, (username,))
            user = cursor.fetchone()
            cursor.close()
            db.close()
            
            # Validación simple de password (en producción usar hash real)
            if user and password == 'admin123':
                request.session['user_id'] = user['id']
                request.session['username'] = user['username']
                request.session['nombre_completo'] = user['nombre_completo']
                request.session['rol'] = user['rol_nombre']
                return HttpResponseRedirect('/')
            else:
                return HttpResponse(render_login(error='Credenciales inválidas', csrf_token=get_token(request)))
        except Exception as e:
            return HttpResponse(render_login(error=f'Error: {str(e)}', csrf_token=get_token(request)))
    
    return HttpResponse(render_login(csrf_token=get_token(request)))

def logout_view(request):
    request.session.flush()
    return HttpResponseRedirect('/login/')

@require_auth
def dashboard_view(request):
    try:
        db = get_db()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
        # Estadísticas
        cursor.execute("SELECT COUNT(*) as total FROM productos")
        total_productos = cursor.fetchone()['total']
        
        cursor.execute("SELECT SUM(stock_actual * precio_venta) as valor FROM productos")
        valor_inventario = cursor.fetchone()['valor'] or 0
        
        cursor.execute("SELECT COUNT(*) as total FROM ventas WHERE estado='completada'")
        total_ventas = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM productos WHERE stock_actual < stock_minimo")
        alertas_stock = cursor.fetchone()['total']
        
        # Productos con stock bajo
        cursor.execute("""
            SELECT codigo, nombre, stock_actual, stock_minimo
            FROM productos
            WHERE stock_actual < stock_minimo
            LIMIT 10
        """)
        productos_bajo_stock = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        user = {
            'nombre_completo': request.session.get('nombre_completo'),
            'rol': request.session.get('rol')
        }
        
        content = f"""
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Productos</h3>
                <div class="value">{total_productos}</div>
            </div>
            <div class="stat-card">
                <h3>Valor Inventario</h3>
                <div class="value">${valor_inventario:,.2f}</div>
            </div>
            <div class="stat-card">
                <h3>Total Ventas</h3>
                <div class="value">{total_ventas}</div>
            </div>
            <div class="stat-card">
                <h3>Alertas Stock</h3>
                <div class="value">{alertas_stock}</div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">⚠️ Productos con Stock Bajo</div>
            <table>
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Producto</th>
                        <th>Stock Actual</th>
                        <th>Stock Mínimo</th>
                        <th>Estado</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for prod in productos_bajo_stock:
            content += f"""
                    <tr>
                        <td>{prod['codigo']}</td>
                        <td>{prod['nombre']}</td>
                        <td>{prod['stock_actual']}</td>
                        <td>{prod['stock_minimo']}</td>
                        <td><span class="badge badge-danger">Bajo</span></td>
                    </tr>
            """
        
        content += """
                </tbody>
            </table>
        </div>
        """
        
        return HttpResponse(render_dashboard(user, request.path, content))
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@require_auth
def productos_view(request):
    try:
        db = get_db()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("""
            SELECT p.*, c.nombre as categoria_nombre, pr.nombre as proveedor_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
            ORDER BY p.id DESC
            LIMIT 50
        """)
        productos = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        user = {
            'nombre_completo': request.session.get('nombre_completo'),
            'rol': request.session.get('rol')
        }
        
        content = f"""
        <div class="card">
            <div class="card-header">
                🏷️ Gestión de Productos
                <a href="/productos/nuevo/" class="btn btn-primary" style="float: right;">+ Nuevo Producto</a>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Código</th>
                        <th>Nombre</th>
                        <th>Categoría</th>
                        <th>Precio Venta</th>
                        <th>Stock</th>
                        <th>Proveedor</th>
                        <th>Estado</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for prod in productos:
            estado = '<span class="badge badge-success">Activo</span>' if prod['activo'] else '<span class="badge badge-danger">Inactivo</span>'
            stock_class = 'badge-danger' if prod['stock_actual'] < prod['stock_minimo'] else 'badge-success'
            content += f"""
                    <tr>
                        <td>{prod['codigo']}</td>
                        <td>{prod['nombre']}</td>
                        <td>{prod['categoria_nombre'] or '-'}</td>
                        <td>${prod['precio_venta']:,.2f}</td>
                        <td><span class="badge {stock_class}">{prod['stock_actual']}</span></td>
                        <td>{prod['proveedor_nombre'] or '-'}</td>
                        <td>{estado}</td>
                    </tr>
            """
        
        content += """
                </tbody>
            </table>
        </div>
        """
        
        return HttpResponse(render_dashboard(user, request.path, content))
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

# Función auxiliar para otras vistas similares
def generic_list_view(request, table_name, title, icon, columns):
    try:
        db = get_db()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 50")
        items = cursor.fetchall()
        cursor.close()
        db.close()
        
        user = {
            'nombre_completo': request.session.get('nombre_completo'),
            'rol': request.session.get('rol')
        }
        
        content = f"""
        <div class="card">
            <div class="card-header">{icon} {title}</div>
            <table>
                <thead>
                    <tr>
        """
        
        for col in columns:
            content += f"<th>{col['label']}</th>"
        
        content += """
                    </tr>
                </thead>
                <tbody>
        """
        
        for item in items:
            content += "<tr>"
            for col in columns:
                value = item.get(col['field'], '-')
                if col['field'] == 'activo':
                    value = '<span class="badge badge-success">Activo</span>' if value else '<span class="badge badge-danger">Inactivo</span>'
                content += f"<td>{value}</td>"
            content += "</tr>"
        
        content += """
                </tbody>
            </table>
        </div>
        """
        
        return HttpResponse(render_dashboard(user, request.path, content))
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@require_auth
def categorias_view(request):
    return generic_list_view(request, 'categorias', 'Gestión de Categorías', '📑',
        [{'field': 'id', 'label': 'ID'}, {'field': 'nombre', 'label': 'Nombre'}, 
         {'field': 'descripcion', 'label': 'Descripción'}, {'field': 'activo', 'label': 'Estado'}])

@require_auth
def proveedores_view(request):
    return generic_list_view(request, 'proveedores', 'Gestión de Proveedores', '🚚',
        [{'field': 'id', 'label': 'ID'}, {'field': 'nombre', 'label': 'Nombre'}, 
         {'field': 'ruc', 'label': 'RUC'}, {'field': 'telefono', 'label': 'Teléfono'},
         {'field': 'email', 'label': 'Email'}, {'field': 'activo', 'label': 'Estado'}])

@require_auth
def clientes_view(request):
    return generic_list_view(request, 'clientes', 'Gestión de Clientes', '👥',
        [{'field': 'id', 'label': 'ID'}, {'field': 'nombre', 'label': 'Nombre'}, 
         {'field': 'documento', 'label': 'Documento'}, {'field': 'telefono', 'label': 'Teléfono'},
         {'field': 'email', 'label': 'Email'}, {'field': 'activo', 'label': 'Estado'}])

@require_auth
def almacenes_view(request):
    return generic_list_view(request, 'almacenes', 'Gestión de Almacenes', '🏭',
        [{'field': 'id', 'label': 'ID'}, {'field': 'nombre', 'label': 'Nombre'}, 
         {'field': 'ubicacion', 'label': 'Ubicación'}, {'field': 'capacidad', 'label': 'Capacidad'},
         {'field': 'activo', 'label': 'Estado'}])

@require_auth
def ventas_view(request):
    try:
        db = get_db()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT v.*, c.nombre as cliente_nombre, u.nombre_completo as usuario_nombre
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN usuarios u ON v.usuario_id = u.id
            ORDER BY v.id DESC LIMIT 50
        """)
        items = cursor.fetchall()
        cursor.close()
        db.close()
        
        user = {'nombre_completo': request.session.get('nombre_completo'), 'rol': request.session.get('rol')}
        
        content = """
        <div class="card">
            <div class="card-header">💰 Gestión de Ventas</div>
            <table>
                <thead>
                    <tr><th>Factura</th><th>Cliente</th><th>Fecha</th><th>Total</th><th>Estado</th><th>Usuario</th></tr>
                </thead>
                <tbody>
        """
        
        for item in items:
            estado_class = {'pendiente': 'warning', 'completada': 'success', 'cancelada': 'danger'}.get(item['estado'], 'secondary')
            content += f"""
                <tr>
                    <td>{item['numero_factura']}</td>
                    <td>{item['cliente_nombre']}</td>
                    <td>{item['fecha']}</td>
                    <td>${item['total']:,.2f}</td>
                    <td><span class="badge badge-{estado_class}">{item['estado'].title()}</span></td>
                    <td>{item['usuario_nombre']}</td>
                </tr>
            """
        
        content += "</tbody></table></div>"
        
        return HttpResponse(render_dashboard(user, request.path, content))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@require_auth
def compras_view(request):
    try:
        db = get_db()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT c.*, p.nombre as proveedor_nombre, u.nombre_completo as usuario_nombre
            FROM compras c
            JOIN proveedores p ON c.proveedor_id = p.id
            JOIN usuarios u ON c.usuario_id = u.id
            ORDER BY c.id DESC LIMIT 50
        """)
        items = cursor.fetchall()
        cursor.close()
        db.close()
        
        user = {'nombre_completo': request.session.get('nombre_completo'), 'rol': request.session.get('rol')}
        
        content = """
        <div class="card">
            <div class="card-header">🛒 Gestión de Compras</div>
            <table>
                <thead>
                    <tr><th>Factura</th><th>Proveedor</th><th>Fecha</th><th>Total</th><th>Estado</th><th>Usuario</th></tr>
                </thead>
                <tbody>
        """
        
        for item in items:
            estado_class = {'pendiente': 'warning', 'completada': 'success', 'cancelada': 'danger'}.get(item['estado'], 'secondary')
            content += f"""
                <tr>
                    <td>{item['numero_factura']}</td>
                    <td>{item['proveedor_nombre']}</td>
                    <td>{item['fecha']}</td>
                    <td>${item['total']:,.2f}</td>
                    <td><span class="badge badge-{estado_class}">{item['estado'].title()}</span></td>
                    <td>{item['usuario_nombre']}</td>
                </tr>
            """
        
        content += "</tbody></table></div>"
        
        return HttpResponse(render_dashboard(user, request.path, content))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@require_auth
def movimientos_view(request):
    try:
        db = get_db()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT m.*, p.nombre as producto_nombre, a.nombre as almacen_nombre, u.nombre_completo as usuario_nombre
            FROM movimientos_inventario m
            JOIN productos p ON m.producto_id = p.id
            JOIN almacenes a ON m.almacen_id = a.id
            JOIN usuarios u ON m.usuario_id = u.id
            ORDER BY m.fecha DESC LIMIT 50
        """)
        items = cursor.fetchall()
        cursor.close()
        db.close()
        
        user = {'nombre_completo': request.session.get('nombre_completo'), 'rol': request.session.get('rol')}
        
        content = """
        <div class="card">
            <div class="card-header">📦 Movimientos de Inventario</div>
            <table>
                <thead>
                    <tr><th>Fecha</th><th>Producto</th><th>Almacén</th><th>Tipo</th><th>Cantidad</th><th>Usuario</th></tr>
                </thead>
                <tbody>
        """
        
        for item in items:
            tipo_class = {'entrada': 'success', 'salida': 'danger', 'ajuste': 'warning'}.get(item['tipo_movimiento'], 'secondary')
            content += f"""
                <tr>
                    <td>{item['fecha']}</td>
                    <td>{item['producto_nombre']}</td>
                    <td>{item['almacen_nombre']}</td>
                    <td><span class="badge badge-{tipo_class}">{item['tipo_movimiento'].title()}</span></td>
                    <td>{item['cantidad']}</td>
                    <td>{item['usuario_nombre']}</td>
                </tr>
            """
        
        content += "</tbody></table></div>"
        
        return HttpResponse(render_dashboard(user, request.path, content))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

@require_auth
def usuarios_view(request):
    return generic_list_view(request, 'usuarios', 'Gestión de Usuarios', '👤',
        [{'field': 'id', 'label': 'ID'}, {'field': 'username', 'label': 'Usuario'}, 
         {'field': 'nombre_completo', 'label': 'Nombre'}, {'field': 'email', 'label': 'Email'},
         {'field': 'activo', 'label': 'Estado'}])

# URLs
urlpatterns = [
    path('', dashboard_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('productos/', productos_view),
    path('categorias/', categorias_view),
    path('proveedores/', proveedores_view),
    path('clientes/', clientes_view),
    path('almacenes/', almacenes_view),
    path('ventas/', ventas_view),
    path('compras/', compras_view),
    path('movimientos/', movimientos_view),
    path('usuarios/', usuarios_view),
]

# Iniciar servidor
if __name__ == '__main__':
    import django
    django.setup()
    from django.core.management import execute_from_command_line
    execute_from_command_line(['', 'runserver', '0.0.0.0:8081'])