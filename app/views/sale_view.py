from django.http import HttpResponse
from app.views.layout import Layout

class SaleView:
    """Vista de Ventas"""
    
    @staticmethod
    def index(user, sales):
        """Renderiza la página de listado de ventas"""
        
        # Mapeo de estados a badges
        estado_badges = {
            'pendiente': '<span class="badge badge-warning">Pendiente</span>',
            'completada': '<span class="badge badge-success">Completada</span>',
            'cancelada': '<span class="badge badge-cancelada">Cancelada</span>'
        }
        
        # Generar las filas de la tabla
        if sales:
            rows = ""
            for sale in sales:
                badge = estado_badges.get(sale['estado'], sale['estado'])
                rows += f"""
                <tr>
                    <td>{sale['numero_factura']}</td>
                    <td>{sale['fecha']}</td>
                    <td>{sale['cliente_nombre']}</td>
                    <td>{sale['cliente_documento'] or 'N/A'}</td>
                    <td>${sale['total']:.2f}</td>
                    <td>{badge}</td>
                    <td>{sale['tipo_pago'].capitalize()}</td>
                    <td>
                        <a href="/ventas/{sale['id']}/editar/" class="btn btn-warning no-underline">Editar</a>
                        <a href="/ventas/{sale['id']}/eliminar/" class="btn btn-danger no-underline" onclick="return confirm('¿Está seguro de eliminar esta venta?');">Eliminar</a>
                    </td>
                </tr>
                """
            
            table_content = f"""
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Factura</th>
                            <th>Fecha</th>
                            <th>Cliente</th>
                            <th>Documento</th>
                            <th>Total</th>
                            <th>Estado</th>
                            <th>Tipo Pago</th>
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
                <div class="icon-4xl"><i class="fas fa-shopping-cart"></i></div>
                <h3>No hay ventas registradas</h3>
                <p>Comienza registrando tu primera venta</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Ventas</span>
                <a href="/ventas/crear/" class="btn btn-primary">+ Nueva Venta</a>
            </div>
            {table_content}
        </div>
        """
        
        return HttpResponse(Layout.render('Ventas', user, 'ventas', content))
    
    @staticmethod
    def create(user, clients, products, request, error=None):
        """Vista del formulario de crear venta"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Generar opciones de clientes
        client_options = '<option value="">Seleccione un cliente</option>'
        for client in clients:
            client_options += f'<option value="{client["id"]}">{client["nombre"]} - {client.get("documento", "S/N")}</option>'
        
        # Generar opciones de productos para el selector
        product_options = '<option value="">Seleccione un producto</option>'
        products_json = []
        for product in products:
            product_options += f'<option value="{product["id"]}">{product["nombre"]} - ${product["precio_venta"]}</option>'
            products_json.append({
                'id': product['id'],
                'nombre': product['nombre'],
                'precio': float(product['precio_venta']),
                'stock': product['stock_actual']
            })
        
        # Mensaje de error si existe
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        # Fecha actual
        from datetime import date
        fecha_actual = date.today().strftime('%Y-%m-%d')
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nueva Venta</span>
                <a href="/ventas/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/ventas/crear/" id="saleForm" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="hidden" name="details" id="details">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Cliente *</label>
                        <select name="cliente_id" required class="form-select">
                            {client_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Fecha *</label>
                        <input type="date" name="fecha" value="{fecha_actual}" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Tipo de Pago</label>
                        <select name="tipo_pago" class="form-select">
                            <option value="efectivo">Efectivo</option>
                            <option value="tarjeta">Tarjeta</option>
                            <option value="transferencia">Transferencia</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Estado</label>
                        <select name="estado" class="form-select">
                            <option value="completada">Completada</option>
                            <option value="pendiente">Pendiente</option>
                        </select>
                    </div>
                </div>
                
                <div class="mb-20">
                    <label class="form-label">Notas</label>
                    <textarea name="notas" rows="2" class="form-textarea"></textarea>
                </div>
                
                <hr class="form-divider">
                
                <h3 class="mb-15">Productos</h3>
                <div class="product-input-grid">
                    <select id="productSelect" class="form-select">
                        {product_options}
                    </select>
                    <input type="number" id="quantityInput" placeholder="Cantidad" min="1" value="1" class="form-input">
                    <button type="button" onclick="addProduct()" class="btn btn-primary">Agregar</button>
                </div>
                
                <table id="productsTable" class="d-none mb-20">
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Precio</th>
                            <th>Cantidad</th>
                            <th>Subtotal</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody id="productsBody"></tbody>
                    <tfoot>
                        <tr>
                            <td colspan="3" class="text-right">TOTAL:</td>
                            <td colspan="2" class="text-success" id="totalAmount">$0.00</td>
                        </tr>
                    </tfoot>
                </table>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Guardar Venta</button>
                    <a href="/ventas/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        
        <script src="/static/js/product-manager.js"></script>
        <script>
            // Inicializar el gestor de productos con los datos del servidor
            const products = {str(products_json).replace("'", '"')};
            manager = new ProductManager(products);
        </script>
        """
        
        return HttpResponse(Layout.render('Crear Venta', user, 'ventas', content))
    
    @staticmethod
    def edit(user, sale, details, clients, products, request, error=None):
        """Vista del formulario de editar venta"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Generar opciones de clientes
        client_options = '<option value="">Seleccione un cliente</option>'
        for client in clients:
            selected = 'selected' if client['id'] == sale.get('cliente_id') else ''
            client_options += f'<option value="{client["id"]}" {selected}>{client["nombre"]} - {client.get("documento", "S/N")}</option>'
        
        # Generar opciones de productos
        product_options = '<option value="">Seleccione un producto</option>'
        products_json = []
        for product in products:
            product_options += f'<option value="{product["id"]}">{product["nombre"]} - ${product["precio_venta"]}</option>'
            products_json.append({
                'id': product['id'],
                'nombre': product['nombre'],
                'precio': float(product['precio_venta']),
                'stock': product['stock_actual']
            })
        
        # Preparar detalles existentes
        existing_details = []
        for detail in details:
            existing_details.append({
                'producto_id': detail['producto_id'],
                'nombre': detail['producto_nombre'],
                'precio_unitario': float(detail['precio_unitario']),
                'cantidad': detail['cantidad'],
                'subtotal': float(detail['subtotal'])
            })
        
        # Mensaje de error
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Venta - {sale['numero_factura']}</span>
                <a href="/ventas/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/ventas/{sale['id']}/editar/" id="saleForm" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="hidden" name="details" id="details">
                <input type="hidden" name="numero_factura" value="{sale['numero_factura']}">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Cliente *</label>
                        <select name="cliente_id" required class="form-select">
                            {client_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Fecha *</label>
                        <input type="date" name="fecha" value="{sale['fecha']}" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Tipo de Pago</label>
                        <select name="tipo_pago" class="form-select">
                            <option value="efectivo" {'selected' if sale.get('tipo_pago') == 'efectivo' else ''}>Efectivo</option>
                            <option value="tarjeta" {'selected' if sale.get('tipo_pago') == 'tarjeta' else ''}>Tarjeta</option>
                            <option value="transferencia" {'selected' if sale.get('tipo_pago') == 'transferencia' else ''}>Transferencia</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Estado</label>
                        <select name="estado" class="form-select">
                            <option value="completada" {'selected' if sale.get('estado') == 'completada' else ''}>Completada</option>
                            <option value="pendiente" {'selected' if sale.get('estado') == 'pendiente' else ''}>Pendiente</option>
                            <option value="cancelada" {'selected' if sale.get('estado') == 'cancelada' else ''}>Cancelada</option>
                        </select>
                    </div>
                </div>
                
                <div class="mb-20">
                    <label class="form-label">Notas</label>
                    <textarea name="notas" rows="2" class="form-textarea">{sale.get('notas', '')}</textarea>
                </div>
                
                <hr class="form-divider">
                
                <h3 class="mb-15">Productos</h3>
                <div class="product-input-grid">
                    <select id="productSelect" class="form-select">
                        {product_options}
                    </select>
                    <input type="number" id="quantityInput" placeholder="Cantidad" min="1" value="1" class="form-input">
                    <button type="button" onclick="addProduct()" class="btn btn-primary">Agregar</button>
                </div>
                
                <table id="productsTable">
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Precio</th>
                            <th>Cantidad</th>
                            <th>Subtotal</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody id="productsBody"></tbody>
                    <tfoot>
                        <tr>
                            <td colspan="3" class="text-right">TOTAL:</td>
                            <td colspan="2" class="text-success" id="totalAmount">$0.00</td>
                        </tr>
                    </tfoot>
                </table>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Actualizar Venta</button>
                    <a href="/ventas/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        
        <script src="/static/js/product-manager.js"></script>
        <script>
            // Inicializar el gestor de productos con los datos del servidor
            const products = {str(products_json).replace("'", '"')};
            const existingDetails = {str(existing_details).replace("'", '"')};
            manager = new ProductManager(products, existingDetails);
            manager.render();
        </script>
        """
        
        return HttpResponse(Layout.render('Editar Venta', user, 'ventas', content))
    
    @staticmethod
    def view(user, sale, details):
        """Vista de detalle de una venta"""
        from django.middleware.csrf import get_token
        
        estado_class = {
            'pendiente': 'warning',
            'completada': 'success',
            'cancelada': 'danger'
        }.get(sale['estado'], 'secondary')
        
        # Detalles de productos
        details_rows = ""
        if details:
            for idx, detail in enumerate(details, 1):
                details_rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{detail['producto_nombre']}</td>
                    <td>{detail['cantidad']}</td>
                    <td>S/ {detail['precio_unitario']:.2f}</td>
                    <td>S/ {detail['subtotal']:.2f}</td>
                </tr>
                """
        else:
            details_rows = '<tr><td colspan="5" class="text-center text-muted">Sin productos</td></tr>'
        
        content = f"""
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="h3 mb-0">Detalle de Venta #{sale['id']}</h1>
            <div>
                <a href="/ventas/{sale['id']}/editar/" class="btn btn-warning">
                    <i class="fas fa-edit"></i> Editar
                </a>
                <a href="/ventas/" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Volver
                </a>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Información de la Venta</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-2">
                            <strong>N° Factura:</strong> {sale.get('numero_factura', 'N/A')}
                        </div>
                        <div class="mb-2">
                            <strong>Cliente:</strong> {sale['cliente_nombre']}
                        </div>
                        <div class="mb-2">
                            <strong>Fecha:</strong> {sale['fecha']}
                        </div>
                        <div class="mb-2">
                            <strong>Estado:</strong> 
                            <span class="badge bg-{estado_class}">{sale['estado']}</span>
                        </div>
                        <div class="mb-2">
                            <strong>Tipo de Pago:</strong> {sale.get('tipo_pago', 'N/A')}
                        </div>
                        <div class="mb-2">
                            <strong>Usuario:</strong> {sale['usuario_nombre']}
                        </div>
                        <div class="mb-2">
                            <strong>Notas:</strong> {sale.get('notas', 'Sin notas')}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">Totales</h5>
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                            <span class="h4 mb-0">Total:</span>
                            <span class="h3 mb-0 text-success">S/ {sale['total']:.2f}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card shadow-sm">
            <div class="card-header bg-light">
                <h5 class="mb-0">Productos</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-bordered">
                        <thead class="table-light">
                            <tr>
                                <th width="50">#</th>
                                <th>Producto</th>
                                <th width="100">Cantidad</th>
                                <th width="120">P. Unitario</th>
                                <th width="120">Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            {details_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        """
        
        from app.views.layout import Layout
        return Layout.render(user, content, 'ventas', 'Detalle de Venta')

