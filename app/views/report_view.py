from django.http import HttpResponse
from app.views.layout import Layout

class ReportView:
    """Vista de Reportes"""
    
    @staticmethod
    def index(user, data):
        """Renderiza la página de reportes y estadísticas"""
        
        resumen = data.get('resumen', {})
        ventas_mes = data.get('ventas_mes', [])
        productos_top = data.get('productos_top', [])
        ventas_estado = data.get('ventas_estado', [])
        clientes_top = data.get('clientes_top', [])
        stock_bajo = data.get('stock_bajo', [])
        
        # Generar tarjetas de resumen
        resumen_html = f"""
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Ventas Completadas</h3>
                <div class="value">{resumen.get('total_ventas_completadas', 0)}</div>
            </div>
            <div class="stat-card">
                <h3>Ingresos Totales</h3>
                <div class="value">${resumen.get('ingresos_totales', 0):,.2f}</div>
            </div>
            <div class="stat-card">
                <h3>Ingresos Mes Actual</h3>
                <div class="value">${resumen.get('ingresos_mes_actual', 0):,.2f}</div>
            </div>
            <div class="stat-card">
                <h3>Clientes Activos</h3>
                <div class="value">{resumen.get('total_clientes_activos', 0)}</div>
            </div>
        </div>
        """
        
        # Generar tabla de productos más vendidos
        productos_rows = ""
        if productos_top:
            for idx, producto in enumerate(productos_top, 1):
                productos_rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{producto['nombre']}</td>
                    <td>{producto['total_vendido']}</td>
                    <td>${producto['ingresos_totales']:,.2f}</td>
                </tr>
                """
        else:
            productos_rows = """
            <tr><td colspan="4" class="empty-state">No hay datos disponibles</td></tr>
            """
        
        # Generar tabla de clientes frecuentes
        clientes_rows = ""
        if clientes_top:
            for idx, cliente in enumerate(clientes_top, 1):
                clientes_rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{cliente['nombre']}</td>
                    <td>{cliente['documento'] or 'N/A'}</td>
                    <td>{cliente['total_compras']}</td>
                    <td>${cliente['monto_total']:,.2f}</td>
                </tr>
                """
        else:
            clientes_rows = """
            <tr><td colspan="5" class="empty-state">No hay datos disponibles</td></tr>
            """
        
        # Generar tabla de ventas por estado
        estado_rows = ""
        if ventas_estado:
            estado_badges = {
                'pendiente': '<span class="badge badge-warning">Pendiente</span>',
                'completada': '<span class="badge badge-success">Completada</span>',
                'cancelada': '<span class="badge" style="background: #fee2e2; color: #991b1b;">Cancelada</span>'
            }
            for estado in ventas_estado:
                badge = estado_badges.get(estado['estado'], estado['estado'])
                estado_rows += f"""
                <tr>
                    <td>{badge}</td>
                    <td>{estado['cantidad']}</td>
                    <td>${estado['monto_total']:,.2f}</td>
                </tr>
                """
        else:
            estado_rows = """
            <tr><td colspan="3" class="empty-state">No hay datos disponibles</td></tr>
            """
        
        # Generar tabla de stock bajo
        stock_rows = ""
        if stock_bajo:
            for producto in stock_bajo:
                alerta_class = 'style="color: #ef4444; font-weight: bold;"' if producto['stock'] < 5 else ''
                stock_rows += f"""
                <tr>
                    <td>{producto['nombre']}</td>
                    <td>{producto['categoria'] or 'Sin categoría'}</td>
                    <td {alerta_class}>{producto['stock']}</td>
                </tr>
                """
        else:
            stock_rows = """
            <tr><td colspan="3" class="empty-state">Todos los productos tienen stock suficiente</td></tr>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Resumen General</span>
            </div>
            {resumen_html}
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px;">
            <div class="card">
                <div class="card-header">Top 5 Productos Más Vendidos</div>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Producto</th>
                            <th>Cantidad</th>
                            <th>Ingresos</th>
                        </tr>
                    </thead>
                    <tbody>
                        {productos_rows}
                    </tbody>
                </table>
            </div>
            
            <div class="card">
                <div class="card-header">Ventas por Estado</div>
                <table>
                    <thead>
                        <tr>
                            <th>Estado</th>
                            <th>Cantidad</th>
                            <th>Monto Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {estado_rows}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="card" style="margin-top: 20px;">
            <div class="card-header">Top 5 Clientes Frecuentes</div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Cliente</th>
                        <th>Documento</th>
                        <th>Compras</th>
                        <th>Monto Total</th>
                    </tr>
                </thead>
                <tbody>
                    {clientes_rows}
                </tbody>
            </table>
        </div>
        
        <div class="card" style="margin-top: 20px;">
            <div class="card-header">
                <span>⚠️ Productos con Stock Bajo</span>
                <span style="font-size: 0.9rem; color: #666; font-weight: normal;">(Stock menor o igual a 10 unidades)</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Producto</th>
                        <th>Categoría</th>
                        <th>Stock Actual</th>
                    </tr>
                </thead>
                <tbody>
                    {stock_rows}
                </tbody>
            </table>
        </div>
        """
        
        return HttpResponse(Layout.render('Reportes', user, 'reportes', content))
