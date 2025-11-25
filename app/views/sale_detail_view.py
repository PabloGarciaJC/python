from django.http import HttpResponse
from app.views.layout import Layout

class SaleDetailView:
    @staticmethod
    def index(user, details, request):
        """Vista de lista de detalles de ventas"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
        # Tabla de detalles
        rows = ""
        if details:
            for idx, detail in enumerate(details, 1):
                rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{detail.get('numero_factura', 'N/A')}</td>
                    <td>{detail['cliente_nombre']}</td>
                    <td>{detail['fecha_venta']}</td>
                    <td>{detail['producto_nombre']}</td>
                    <td>{detail['cantidad']}</td>
                    <td>S/ {detail['precio_unitario']:.2f}</td>
                    <td>S/ {detail['subtotal']:.2f}</td>
                    <td>
                        <a href="/detalle-ventas/{detail['id']}/ver/" class="btn btn-info">Ver</a>
                        <a href="/detalle-ventas/{detail['id']}/editar/" class="btn btn-warning">Editar</a>
                        <form method="POST" action="/detalle-ventas/{detail['id']}/eliminar/" class="d-inline">
                            {csrf_token}
                            <button type="submit" class="btn btn-danger" 
                                    onclick="return confirm('¿Estás seguro de eliminar este detalle?')">
                                Eliminar
                            </button>
                        </form>
                    </td>
                </tr>
                """
            
            table_content = f"""
            <div class="table-container">
                <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>N° Factura</th>
                        <th>Cliente</th>
                        <th>Fecha</th>
                        <th>Producto</th>
                        <th>Cantidad</th>
                        <th>Precio Unit.</th>
                        <th>Subtotal</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
                </table>
            </div>
            """
        else:
            table_content = """
            <div class="empty-state">
                <i class="fas fa-file-invoice icon-4xl"></i>
                <h3>No hay detalles de ventas registrados</h3>
                <p>Comienza agregando el primer detalle</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Detalles de Ventas</span>
                <a href="/detalle-ventas/crear/" class="btn btn-primary">+ Nuevo Detalle</a>
            </div>
            {table_content}
        </div>
        """
        
        return Layout.render('Detalles de Ventas', user, 'detalle-ventas', content)
    
    @staticmethod
    def create(user, sales, products, request, error=None):
        """Vista de formulario para crear detalle de venta"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        # Select de ventas
        sale_options = '<option value="">Seleccione una venta</option>'
        for sale in sales:
            sale_options += f'<option value="{sale["id"]}">{sale.get("numero_factura", "Sin factura")} - {sale["cliente_nombre"]} ({sale["fecha"]})</option>'
        
        # Select de productos
        product_options = '<option value="">Seleccione un producto</option>'
        for product in products:
            product_options += f'<option value="{product["id"]}" data-price="{product["precio_venta"]}">{product["nombre"]} - S/ {product["precio_venta"]:.2f}</option>'
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nuevo Detalle de Venta</span>
                <a href="/detalle-ventas/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/detalle-ventas/crear/" class="p-20" id="detailForm">
                {csrf_token}
                <div class="form-grid">
                    <div>
                        <label class="form-label">Venta *</label>
                        <select name="venta_id" required
                                class="form-select">
                            {sale_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Producto *</label>
                        <select name="producto_id" id="producto" required
                                class="form-select">
                            {product_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Cantidad *</label>
                        <input type="number" name="cantidad" id="cantidad" value="1" min="1" required
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Precio Unitario *</label>
                        <input type="number" name="precio_unitario" id="precio_unitario" step="0.01" min="0" required
                               class="form-input">
                    </div>
                </div>
                
                <div class="total-summary">
                    <p>
                        Subtotal: S/ <span id="subtotal">0.00</span>
                    </p>
                </div>
                
                <div class="form-actions-end mt-30">
                    <a href="/detalle-ventas/" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Guardar Detalle</button>
                </div>
            </form>
        </div>
        
        <script src="/static/js/detail-calculator.js"></script>
        """
        
        return Layout.render('Nuevo Detalle de Venta', user, 'detalle-ventas', content)
    
    @staticmethod
    def edit(user, detail, products, request, error=None):
        """Vista de formulario para editar detalle de venta"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        # Select de productos
        product_options = ""
        for product in products:
            selected = 'selected' if product['id'] == detail['producto_id'] else ''
            product_options += f'<option value="{product["id"]}" data-price="{product["precio_venta"]}" {selected}>{product["nombre"]} - S/ {product["precio_venta"]:.2f}</option>'
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Detalle de Venta</span>
                <a href="/detalle-ventas/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/detalle-ventas/{detail['id']}/editar/" class="p-20" id="detailForm">
                {csrf_token}
                <div class="form-grid">
                    <div>
                        <label class="form-label">Venta</label>
                        <input type="text" value="{detail.get('numero_factura', 'Sin factura')}" disabled
                               class="form-input-disabled">
                        <small class="form-hint">La venta no se puede cambiar</small>
                    </div>
                    
                    <div>
                        <label class="form-label">Producto *</label>
                        <select name="producto_id" id="producto" required
                                class="form-select">
                            {product_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Cantidad *</label>
                        <input type="number" name="cantidad" id="cantidad" value="{detail['cantidad']}" min="1" required
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Precio Unitario *</label>
                        <input type="number" name="precio_unitario" id="precio_unitario" value="{detail['precio_unitario']}" step="0.01" min="0" required
                               class="form-input">
                    </div>
                </div>
                
                <div class="total-summary">
                    <p>
                        Subtotal: S/ <span id="subtotal">{detail['subtotal']:.2f}</span>
                    </p>
                </div>
                
                <div class="form-actions-end mt-30">
                    <a href="/detalle-ventas/" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Actualizar Detalle</button>
                </div>
            </form>
        </div>
        
        <script src="/static/js/detail-calculator.js"></script>
        """
        
        return Layout.render('Editar Detalle de Venta', user, 'detalle-ventas', content)
    
    @staticmethod
    def view(user, detail):
        """Vista de detalle específico de venta"""
        
        estado_badge = {
            'pendiente': '<span class="badge badge-warning">Pendiente</span>',
            'completada': '<span class="badge badge-success">Completada</span>',
            'cancelada': '<span class="badge badge-cancelada">Cancelada</span>'
        }.get(detail.get('venta_estado', ''), detail.get('venta_estado', ''))
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Detalle de Venta #{detail['id']}</span>
                <a href="/detalle-ventas/" class="btn btn-secondary">← Volver</a>
            </div>
            
            <div class="p-20">
                <div class="detail-info-section">
                    <h3>Información de la Venta</h3>
                    <div class="info-grid">
                        <div>
                            <p class="info-box-label">N° Factura</p>
                            <p class="info-box-value">{detail.get('numero_factura', 'Sin factura')}</p>
                        </div>
                        <div>
                            <p class="info-box-label">Cliente</p>
                            <p class="info-box-value">{detail['cliente_nombre']}</p>
                            <p class="form-hint">{detail.get('cliente_documento', '')}</p>
                        </div>
                        <div>
                            <p class="info-box-label">Fecha</p>
                            <p class="info-box-value">{detail['fecha_venta']}</p>
                        </div>
                        <div>
                            <p class="info-box-label">Tipo de Pago</p>
                            <p class="info-box-value">{detail.get('tipo_pago', 'N/A').capitalize()}</p>
                        </div>
                        <div>
                            <p class="info-box-label">Estado</p>
                            <p class="info-box-value">{estado_badge}</p>
                        </div>
                        <div>
                            <p class="info-box-label">Total Venta</p>
                            <p class="info-box-value text-success-lg">S/ {detail['venta_total']:.2f}</p>
                        </div>
                    </div>
                </div>
                
                <h3>Detalle del Producto</h3>
                <div class="info-grid">
                    <div class="info-box-white">
                        <p class="info-box-label">Producto</p>
                        <p class="info-box-value">{detail['producto_nombre']}</p>
                    </div>
                    
                    <div class="info-box-white">
                        <p class="info-box-label">Cantidad</p>
                        <p class="info-box-value">{detail['cantidad']} unidades</p>
                    </div>
                    
                    <div class="info-box-white">
                        <p class="info-box-label">Precio Unitario</p>
                        <p class="info-box-value">S/ {detail['precio_unitario']:.2f}</p>
                    </div>
                    
                    <div class="info-box-white">
                        <p class="info-box-label">Subtotal</p>
                        <p class="info-box-value text-success-lg">S/ {detail['subtotal']:.2f}</p>
                    </div>
                </div>
                
                <div class="mt-30 d-flex gap-10">
                    <a href="/detalle-ventas/{detail['id']}/editar/" class="btn btn-warning">Editar Detalle</a>
                    <a href="/detalle-ventas/" class="btn btn-secondary">Volver al Listado</a>
                </div>
            </div>
        </div>
        """
        
        return Layout.render('Ver Detalle de Venta', user, 'detalle-ventas', content)
