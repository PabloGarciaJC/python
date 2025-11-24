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
            'cancelada': '<span class="badge" style="background: #fee2e2; color: #991b1b;">Cancelada</span>'
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
                        <a href="/ventas/{sale['id']}/editar/" class="btn btn-warning" style="text-decoration: none;">Editar</a>
                        <a href="/ventas/{sale['id']}/eliminar/" class="btn btn-danger" style="text-decoration: none;" onclick="return confirm('¿Está seguro de eliminar esta venta?');">Eliminar</a>
                    </td>
                </tr>
                """
            
            table_content = f"""
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
            """
        else:
            table_content = """
            <div class="empty-state">
                <div style="font-size: 4rem; margin-bottom: 20px;">🛒</div>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
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
                <a href="/ventas/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/ventas/crear/" id="saleForm" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="hidden" name="details" id="details">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Cliente *</label>
                        <select name="cliente_id" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            {client_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Fecha *</label>
                        <input type="date" name="fecha" value="{fecha_actual}" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Tipo de Pago</label>
                        <select name="tipo_pago" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="efectivo">Efectivo</option>
                            <option value="tarjeta">Tarjeta</option>
                            <option value="transferencia">Transferencia</option>
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Estado</label>
                        <select name="estado" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="completada">Completada</option>
                            <option value="pendiente">Pendiente</option>
                        </select>
                    </div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Notas</label>
                    <textarea name="notas" rows="2" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;"></textarea>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                
                <h3 style="margin-bottom: 15px;">Productos</h3>
                <div style="display: grid; grid-template-columns: 2fr 1fr 100px; gap: 10px; margin-bottom: 15px;">
                    <select id="productSelect" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                        {product_options}
                    </select>
                    <input type="number" id="quantityInput" placeholder="Cantidad" min="1" value="1" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    <button type="button" onclick="addProduct()" class="btn btn-primary">Agregar</button>
                </div>
                
                <table id="productsTable" style="display: none; margin-bottom: 20px;">
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
                            <td colspan="3" style="text-align: right; font-weight: bold;">TOTAL:</td>
                            <td colspan="2" style="font-weight: bold; color: #10b981;" id="totalAmount">$0.00</td>
                        </tr>
                    </tfoot>
                </table>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Guardar Venta</button>
                    <a href="/ventas/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        
        <script>
            const products = {str(products_json).replace("'", '"')};
            let selectedProducts = [];
            
            function addProduct() {{
                const select = document.getElementById('productSelect');
                const quantity = parseInt(document.getElementById('quantityInput').value);
                const productId = parseInt(select.value);
                
                if (!productId || quantity <= 0) {{
                    alert('Seleccione un producto y cantidad válida');
                    return;
                }}
                
                const product = products.find(p => p.id === productId);
                if (!product) return;
                
                // Verificar si ya está agregado
                const existing = selectedProducts.find(p => p.producto_id === productId);
                if (existing) {{
                    existing.cantidad += quantity;
                    existing.subtotal = existing.cantidad * existing.precio_unitario;
                }} else {{
                    selectedProducts.push({{
                        producto_id: productId,
                        nombre: product.nombre,
                        precio_unitario: product.precio,
                        cantidad: quantity,
                        subtotal: product.precio * quantity
                    }});
                }}
                
                renderProducts();
                select.value = '';
                document.getElementById('quantityInput').value = 1;
            }}
            
            function removeProduct(index) {{
                selectedProducts.splice(index, 1);
                renderProducts();
            }}
            
            function renderProducts() {{
                const tbody = document.getElementById('productsBody');
                const table = document.getElementById('productsTable');
                
                if (selectedProducts.length === 0) {{
                    table.style.display = 'none';
                    return;
                }}
                
                table.style.display = 'table';
                tbody.innerHTML = selectedProducts.map((p, i) => `
                    <tr>
                        <td>${{p.nombre}}</td>
                        <td>$${{p.precio_unitario.toFixed(2)}}</td>
                        <td>${{p.cantidad}}</td>
                        <td>$${{p.subtotal.toFixed(2)}}</td>
                        <td><button type="button" class="btn btn-danger" onclick="removeProduct(${{i}})">X</button></td>
                    </tr>
                `).join('');
                
                const total = selectedProducts.reduce((sum, p) => sum + p.subtotal, 0);
                document.getElementById('totalAmount').textContent = `$${{total.toFixed(2)}}`;
            }}
            
            document.getElementById('saleForm').addEventListener('submit', function(e) {{
                if (selectedProducts.length === 0) {{
                    e.preventDefault();
                    alert('Debe agregar al menos un producto');
                    return;
                }}
                document.getElementById('details').value = JSON.stringify(selectedProducts);
            }});
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Venta - {sale['numero_factura']}</span>
                <a href="/ventas/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/ventas/{sale['id']}/editar/" id="saleForm" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="hidden" name="details" id="details">
                <input type="hidden" name="numero_factura" value="{sale['numero_factura']}">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Cliente *</label>
                        <select name="cliente_id" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            {client_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Fecha *</label>
                        <input type="date" name="fecha" value="{sale['fecha']}" required style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Tipo de Pago</label>
                        <select name="tipo_pago" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="efectivo" {'selected' if sale.get('tipo_pago') == 'efectivo' else ''}>Efectivo</option>
                            <option value="tarjeta" {'selected' if sale.get('tipo_pago') == 'tarjeta' else ''}>Tarjeta</option>
                            <option value="transferencia" {'selected' if sale.get('tipo_pago') == 'transferencia' else ''}>Transferencia</option>
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Estado</label>
                        <select name="estado" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="completada" {'selected' if sale.get('estado') == 'completada' else ''}>Completada</option>
                            <option value="pendiente" {'selected' if sale.get('estado') == 'pendiente' else ''}>Pendiente</option>
                            <option value="cancelada" {'selected' if sale.get('estado') == 'cancelada' else ''}>Cancelada</option>
                        </select>
                    </div>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Notas</label>
                    <textarea name="notas" rows="2" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">{sale.get('notas', '')}</textarea>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                
                <h3 style="margin-bottom: 15px;">Productos</h3>
                <div style="display: grid; grid-template-columns: 2fr 1fr 100px; gap: 10px; margin-bottom: 15px;">
                    <select id="productSelect" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                        {product_options}
                    </select>
                    <input type="number" id="quantityInput" placeholder="Cantidad" min="1" value="1" style="padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
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
                            <td colspan="3" style="text-align: right; font-weight: bold;">TOTAL:</td>
                            <td colspan="2" style="font-weight: bold; color: #10b981;" id="totalAmount">$0.00</td>
                        </tr>
                    </tfoot>
                </table>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Actualizar Venta</button>
                    <a href="/ventas/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        
        <script>
            const products = {str(products_json).replace("'", '"')};
            let selectedProducts = {str(existing_details).replace("'", '"')};
            
            function addProduct() {{
                const select = document.getElementById('productSelect');
                const quantity = parseInt(document.getElementById('quantityInput').value);
                const productId = parseInt(select.value);
                
                if (!productId || quantity <= 0) {{
                    alert('Seleccione un producto y cantidad válida');
                    return;
                }}
                
                const product = products.find(p => p.id === productId);
                if (!product) return;
                
                const existing = selectedProducts.find(p => p.producto_id === productId);
                if (existing) {{
                    existing.cantidad += quantity;
                    existing.subtotal = existing.cantidad * existing.precio_unitario;
                }} else {{
                    selectedProducts.push({{
                        producto_id: productId,
                        nombre: product.nombre,
                        precio_unitario: product.precio,
                        cantidad: quantity,
                        subtotal: product.precio * quantity
                    }});
                }}
                
                renderProducts();
                select.value = '';
                document.getElementById('quantityInput').value = 1;
            }}
            
            function removeProduct(index) {{
                selectedProducts.splice(index, 1);
                renderProducts();
            }}
            
            function renderProducts() {{
                const tbody = document.getElementById('productsBody');
                tbody.innerHTML = selectedProducts.map((p, i) => `
                    <tr>
                        <td>${{p.nombre}}</td>
                        <td>$${{p.precio_unitario.toFixed(2)}}</td>
                        <td>${{p.cantidad}}</td>
                        <td>$${{p.subtotal.toFixed(2)}}</td>
                        <td><button type="button" class="btn btn-danger" onclick="removeProduct(${{i}})">X</button></td>
                    </tr>
                `).join('');
                
                const total = selectedProducts.reduce((sum, p) => sum + p.subtotal, 0);
                document.getElementById('totalAmount').textContent = `$${{total.toFixed(2)}}`;
            }}
            
            document.getElementById('saleForm').addEventListener('submit', function(e) {{
                if (selectedProducts.length === 0) {{
                    e.preventDefault();
                    alert('Debe agregar al menos un producto');
                    return;
                }}
                document.getElementById('details').value = JSON.stringify(selectedProducts);
            }});
            
            // Renderizar productos existentes al cargar
            renderProducts();
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

