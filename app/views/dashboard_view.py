from django.http import HttpResponse
from app.views.layout import Layout

class DashboardView:
    """Vista del Dashboard"""
    
    @staticmethod
    def index(user, request_path, stats, productos_bajo_stock, ultimas_ventas, ultimas_compras):
        """Vista principal del dashboard mejorada"""
        
        # Tarjetas de estadísticas principales
        main_stats = f"""
        <div class="stats-primary-grid">
            <div class="stat-card-primary bg-gradient-purple">
                <div class="stat-card-content">
                    <div class="stat-card-info">
                        <p>Productos</p>
                        <h2>{stats['total_productos']}</h2>
                    </div>
                    <div class="stat-card-icon"><i class="fas fa-box"></i></div>
                </div>
            </div>
            
            <div class="stat-card-primary bg-gradient-pink">
                <div class="stat-card-content">
                    <div class="stat-card-info">
                        <p>Ventas del Mes</p>
                        <h2>${stats['ventas_mes']:,.2f}</h2>
                    </div>
                    <div class="stat-card-icon"><i class="fas fa-dollar-sign"></i></div>
                </div>
            </div>
            
            <div class="stat-card-primary bg-gradient-cyan">
                <div class="stat-card-content">
                    <div class="stat-card-info">
                        <p>Compras del Mes</p>
                        <h2>${stats['compras_mes']:,.2f}</h2>
                    </div>
                    <div class="stat-card-icon"><i class="fas fa-shopping-cart"></i></div>
                </div>
            </div>
            
            <div class="stat-card-primary bg-gradient-green">
                <div class="stat-card-content">
                    <div class="stat-card-info">
                        <p>Clientes</p>
                        <h2>{stats['total_clientes']}</h2>
                    </div>
                    <div class="stat-card-icon"><i class="fas fa-users"></i></div>
                </div>
            </div>
        </div>
        """
        
        # Tarjetas de estadísticas secundarias
        secondary_stats = f"""
        <div class="stats-secondary-grid">
            <div class="stat-card-secondary border-purple">
                <p>Categorías</p>
                <h3>{stats['total_categorias']}</h3>
            </div>
            
            <div class="stat-card-secondary border-pink">
                <p>Proveedores</p>
                <h3>{stats['total_proveedores']}</h3>
            </div>
            
            <div class="stat-card-secondary border-blue">
                <p>Almacenes</p>
                <h3>{stats['total_almacenes']}</h3>
            </div>
            
            <div class="stat-card-secondary border-green">
                <p>Total Ventas</p>
                <h3>{stats['total_ventas']}</h3>
            </div>
            
            <div class="stat-card-secondary border-orange">
                <p>Total Compras</p>
                <h3>{stats['total_compras']}</h3>
            </div>
            
            <div class="stat-card-secondary border-cyan">
                <p>Movimientos Inventario</p>
                <h3>{stats['total_movimientos']}</h3>
            </div>
        </div>
        """
        
        # Productos con stock bajo
        stock_rows = ""
        if productos_bajo_stock:
            for producto in productos_bajo_stock:
                badge_class = "stock-danger" if producto['stock_actual'] < 5 else "stock-warning"
                stock_rows += f"""
                <tr>
                    <td>{producto['nombre']}</td>
                    <td>{producto.get('categoria', 'N/A')}</td>
                    <td>
                        <span class="stock-badge {badge_class}">
                            {producto['stock_actual']} unidades
                        </span>
                    </td>
                    <td>
                        <a href="/productos/{producto['id']}/editar/" class="btn btn-info btn-sm">
                            Ver Producto
                        </a>
                    </td>
                </tr>
                """
        else:
            stock_rows = '<tr><td colspan="4" class="empty-message"><i class="fas fa-check-circle"></i> Todos los productos tienen stock suficiente</td></tr>'
        
        productos_stock_section = f"""
        <div class="card mb-30">
            <div class="card-header">
                <span><i class="fas fa-exclamation-triangle"></i> Productos con Stock Bajo</span>
                <a href="/productos/" class="btn btn-secondary">Ver Todos</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Categoría</th>
                            <th>Stock Actual</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stock_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        # Últimas ventas
        ventas_rows = ""
        if ultimas_ventas:
            for venta in ultimas_ventas:
                estado_badge = {
                    'pendiente': '<span class="badge badge-warning">Pendiente</span>',
                    'completada': '<span class="badge badge-success">Completada</span>',
                    'cancelada': '<span class="badge badge-danger">Cancelada</span>'
                }.get(venta.get('estado', 'pendiente'), venta.get('estado', 'pendiente'))
                
                ventas_rows += f"""
                <tr>
                    <td>#{venta['id']}</td>
                    <td>{venta.get('cliente_nombre', 'N/A')}</td>
                    <td>${venta['total']:,.2f}</td>
                    <td>{estado_badge}</td>
                    <td>{venta['fecha']}</td>
                    <td>
                        <a href="/ventas/{venta['id']}/ver/" class="btn btn-info btn-sm">
                            Ver
                        </a>
                    </td>
                </tr>
                """
        else:
            ventas_rows = '<tr><td colspan="6" class="empty-message"><i class="fas fa-chart-line"></i> No hay ventas registradas</td></tr>'
        
        ultimas_ventas_section = f"""
        <div class="card mb-30">
            <div class="card-header">
                <span><i class="fas fa-credit-card"></i> Últimas Ventas</span>
                <a href="/ventas/" class="btn btn-primary">Ver Todas</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Cliente</th>
                            <th>Total</th>
                            <th>Estado</th>
                            <th>Fecha</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ventas_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        # Últimas compras
        compras_rows = ""
        if ultimas_compras:
            for compra in ultimas_compras:
                estado_badge = {
                    'pendiente': '<span class="badge badge-warning">Pendiente</span>',
                    'recibida': '<span class="badge badge-success">Recibida</span>',
                    'cancelada': '<span class="badge badge-danger">Cancelada</span>'
                }.get(compra.get('estado', 'pendiente'), compra.get('estado', 'pendiente'))
                
                compras_rows += f"""
                <tr>
                    <td>#{compra['id']}</td>
                    <td>{compra.get('proveedor_nombre', 'N/A')}</td>
                    <td>${compra['total']:,.2f}</td>
                    <td>{estado_badge}</td>
                    <td>{compra['fecha']}</td>
                    <td>
                        <a href="/compras/{compra['id']}/ver/" class="btn btn-info btn-sm">
                            Ver
                        </a>
                    </td>
                </tr>
                """
        else:
            compras_rows = '<tr><td colspan="6" class="empty-message"><i class="fas fa-shopping-cart"></i> No hay compras registradas</td></tr>'
        
        ultimas_compras_section = f"""
        <div class="card">
            <div class="card-header">
                <span><i class="fas fa-shopping-bag"></i> Últimas Compras</span>
                <a href="/compras/" class="btn btn-primary">Ver Todas</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Proveedor</th>
                            <th>Total</th>
                            <th>Estado</th>
                            <th>Fecha</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {compras_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        # Bienvenida personalizada
        welcome_card = f"""
        <div class="welcome-banner">
            <h1>Bienvenido, {user['nombre_completo']}</h1>
            <p>Rol: {user['rol']} | Dashboard del Sistema de Inventario</p>
        </div>
        """
        
        content = welcome_card + main_stats + secondary_stats + productos_stock_section + ultimas_ventas_section + ultimas_compras_section
        
        return HttpResponse(Layout.render('Dashboard', user, 'dashboard', content))
