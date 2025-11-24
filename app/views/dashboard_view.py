from django.http import HttpResponse
from app.views.layout import Layout

class DashboardView:
    """Vista del Dashboard"""
    
    @staticmethod
    def index(user, request_path, stats, productos_bajo_stock, ultimas_ventas, ultimas_compras):
        """Vista principal del dashboard mejorada"""
        
        # Tarjetas de estadísticas principales
        main_stats = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px;">
            <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="margin: 0; opacity: 0.9; font-size: 14px;">Productos</p>
                        <h2 style="margin: 10px 0 0 0; font-size: 32px; font-weight: 700;">{stats['total_productos']}</h2>
                    </div>
                    <div style="font-size: 40px; opacity: 0.3;">📦</div>
                </div>
            </div>
            
            <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="margin: 0; opacity: 0.9; font-size: 14px;">Ventas del Mes</p>
                        <h2 style="margin: 10px 0 0 0; font-size: 32px; font-weight: 700;">${stats['ventas_mes']:,.2f}</h2>
                    </div>
                    <div style="font-size: 40px; opacity: 0.3;">💰</div>
                </div>
            </div>
            
            <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="margin: 0; opacity: 0.9; font-size: 14px;">Compras del Mes</p>
                        <h2 style="margin: 10px 0 0 0; font-size: 32px; font-weight: 700;">${stats['compras_mes']:,.2f}</h2>
                    </div>
                    <div style="font-size: 40px; opacity: 0.3;">🛒</div>
                </div>
            </div>
            
            <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="margin: 0; opacity: 0.9; font-size: 14px;">Clientes</p>
                        <h2 style="margin: 10px 0 0 0; font-size: 32px; font-weight: 700;">{stats['total_clientes']}</h2>
                    </div>
                    <div style="font-size: 40px; opacity: 0.3;">👥</div>
                </div>
            </div>
        </div>
        """
        
        # Tarjetas de estadísticas secundarias
        secondary_stats = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px;">
            <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #8b5cf6; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <p style="margin: 0; color: #6b7280; font-size: 13px;">Categorías</p>
                <h3 style="margin: 8px 0 0 0; font-size: 24px; font-weight: 700; color: #111827;">{stats['total_categorias']}</h3>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #ec4899; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <p style="margin: 0; color: #6b7280; font-size: 13px;">Proveedores</p>
                <h3 style="margin: 8px 0 0 0; font-size: 24px; font-weight: 700; color: #111827;">{stats['total_proveedores']}</h3>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <p style="margin: 0; color: #6b7280; font-size: 13px;">Almacenes</p>
                <h3 style="margin: 8px 0 0 0; font-size: 24px; font-weight: 700; color: #111827;">{stats['total_almacenes']}</h3>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #10b981; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <p style="margin: 0; color: #6b7280; font-size: 13px;">Total Ventas</p>
                <h3 style="margin: 8px 0 0 0; font-size: 24px; font-weight: 700; color: #111827;">{stats['total_ventas']}</h3>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #f59e0b; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <p style="margin: 0; color: #6b7280; font-size: 13px;">Total Compras</p>
                <h3 style="margin: 8px 0 0 0; font-size: 24px; font-weight: 700; color: #111827;">{stats['total_compras']}</h3>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 10px; border-left: 4px solid #06b6d4; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <p style="margin: 0; color: #6b7280; font-size: 13px;">Movimientos Inventario</p>
                <h3 style="margin: 8px 0 0 0; font-size: 24px; font-weight: 700; color: #111827;">{stats['total_movimientos']}</h3>
            </div>
        </div>
        """
        
        # Productos con stock bajo
        stock_rows = ""
        if productos_bajo_stock:
            for producto in productos_bajo_stock:
                color = "#ef4444" if producto['stock_actual'] < 5 else "#f59e0b"
                stock_rows += f"""
                <tr>
                    <td>{producto['nombre']}</td>
                    <td>{producto.get('categoria', 'N/A')}</td>
                    <td>
                        <span style="padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; background: {color}; color: white;">
                            {producto['stock_actual']} unidades
                        </span>
                    </td>
                    <td>
                        <a href="/productos/{producto['id']}/editar/" class="btn" style="background: #3b82f6; color: white; padding: 6px 12px; font-size: 13px;">
                            Ver Producto
                        </a>
                    </td>
                </tr>
                """
        else:
            stock_rows = '<tr><td colspan="4" style="text-align: center; padding: 30px; color: #6b7280;">✅ Todos los productos tienen stock suficiente</td></tr>'
        
        productos_stock_section = f"""
        <div class="card" style="margin-bottom: 30px;">
            <div class="card-header">
                <span>⚠️ Productos con Stock Bajo</span>
                <a href="/productos/" class="btn" style="background: #6b7280; color: white;">Ver Todos</a>
            </div>
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
                        <a href="/ventas/{venta['id']}/ver/" class="btn" style="background: #3b82f6; color: white; padding: 6px 12px; font-size: 13px;">
                            Ver
                        </a>
                    </td>
                </tr>
                """
        else:
            ventas_rows = '<tr><td colspan="6" style="text-align: center; padding: 30px; color: #6b7280;">📊 No hay ventas registradas</td></tr>'
        
        ultimas_ventas_section = f"""
        <div class="card" style="margin-bottom: 30px;">
            <div class="card-header">
                <span>💳 Últimas Ventas</span>
                <a href="/ventas/" class="btn btn-primary">Ver Todas</a>
            </div>
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
                        <a href="/compras/{compra['id']}/ver/" class="btn" style="background: #3b82f6; color: white; padding: 6px 12px; font-size: 13px;">
                            Ver
                        </a>
                    </td>
                </tr>
                """
        else:
            compras_rows = '<tr><td colspan="6" style="text-align: center; padding: 30px; color: #6b7280;">📦 No hay compras registradas</td></tr>'
        
        ultimas_compras_section = f"""
        <div class="card">
            <div class="card-header">
                <span>🛍️ Últimas Compras</span>
                <a href="/compras/" class="btn btn-primary">Ver Todas</a>
            </div>
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
        """
        
        # Bienvenida personalizada
        welcome_card = f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="margin: 0 0 10px 0; font-size: 28px;">¡Bienvenido, {user['nombre_completo']}! 👋</h1>
            <p style="margin: 0; opacity: 0.9; font-size: 16px;">Rol: {user['rol']} | Dashboard del Sistema de Gestión</p>
        </div>
        """
        
        content = welcome_card + main_stats + secondary_stats + productos_stock_section + ultimas_ventas_section + ultimas_compras_section
        
        return HttpResponse(Layout.render('Dashboard', user, 'dashboard', content))
