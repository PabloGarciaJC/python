from django.http import HttpResponse
from django.middleware.csrf import get_token
from app.views.layout import Layout

class PurchaseView:
    @staticmethod
    def index(user, purchases, request):
        """Vista de lista de compras"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
        # Tabla de compras
        rows = ""
        if purchases:
            for idx, purchase in enumerate(purchases, 1):
                estado_badge = {
                    'pendiente': '<span class="badge badge-warning">Pendiente</span>',
                    'completada': '<span class="badge badge-success">Completada</span>',
                    'cancelada': '<span class="badge badge-cancelada">Cancelada</span>'
                }.get(purchase['estado'], purchase['estado'])
                
                rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{purchase.get('numero_factura', 'N/A')}</td>
                    <td>{purchase['proveedor_nombre']}</td>
                    <td>{purchase['fecha']}</td>
                    <td>S/ {purchase['total']:.2f}</td>
                    <td>{estado_badge}</td>
                    <td>{purchase['usuario_nombre']}</td>
                    <td>
                        <a href="/compras/{purchase['id']}/ver/" class="btn btn-info btn-sm">Ver</a>
                        <a href="/compras/{purchase['id']}/editar/" class="btn btn-warning">Editar</a>
                        <form method="POST" action="/compras/{purchase['id']}/eliminar/" class="d-inline">
                            {csrf_token}
                            <button type="submit" class="btn btn-danger" 
                                    onclick="return confirm('¿Estás seguro de eliminar esta compra?')">
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
                        <th>Proveedor</th>
                        <th>Fecha</th>
                        <th>Total</th>
                        <th>Estado</th>
                        <th>Usuario</th>
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
                <h3>No hay compras registradas</h3>
                <p>Comienza agregando tu primera compra</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Compras</span>
                <a href="/compras/crear/" class="btn btn-primary">+ Nueva Compra</a>
            </div>
            {table_content}
        </div>
        """
        
        return Layout.render('Compras', user, 'compras', content)
    
    @staticmethod
    def create(user, suppliers, products, request, error=None):
        """Vista de formulario para crear compra"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        # Select de proveedores
        suppliers_options = '<option value="">Seleccione un proveedor</option>'
        for supplier in suppliers:
            suppliers_options += f'<option value="{supplier["id"]}">{supplier["nombre"]}</option>'
        
        # Select de productos
        products_options = '<option value="">Seleccione un producto</option>'
        for product in products:
            products_options += f'<option value="{product["id"]}" data-price="{product["precio_venta"]}">{product["nombre"]} - S/ {product["precio_venta"]:.2f}</option>'
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Nueva Compra</span>
                <a href="/compras/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/compras/crear/" id="purchaseForm" class="p-20">
                {csrf_token}
                <input type="hidden" name="details" id="detailsInput" value="[]">
                    
                <div class="form-grid">
                    <div>
                        <label class="form-label">N° Factura</label>
                        <input type="text" name="numero_factura" placeholder="Opcional" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Proveedor *</label>
                        <select name="proveedor_id" required class="form-select">
                            {suppliers_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Fecha *</label>
                        <input type="date" name="fecha" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Estado</label>
                        <select name="estado" class="form-select">
                            <option value="pendiente">Pendiente</option>
                            <option value="completada">Completada</option>
                            <option value="cancelada">Cancelada</option>
                        </select>
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Notas</label>
                    <textarea name="notas" rows="2" class="form-textarea"></textarea>
                </div>
                
                <hr class="form-divider">
                
                <h3 class="mb-20">Productos</h3>
                
                <div class="purchase-product-grid">
                    <div>
                        <label class="form-label">Producto</label>
                        <select id="productSelect" class="form-select">
                            {products_options}
                        </select>
                    </div>
                    <div>
                        <label class="form-label">Cantidad</label>
                        <input type="number" id="quantityInput" min="1" value="1" class="form-input">
                    </div>
                    <div>
                        <label class="form-label">Precio Unitario</label>
                        <input type="number" id="priceInput" min="0" step="0.01" value="0" class="form-input">
                    </div>
                    <div>
                        <button type="button" class="btn btn-success" id="addProductBtn">+ Agregar</button>
                    </div>
                </div>
                
                <table class="mt-20">
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th class="col-w-100">Cantidad</th>
                            <th class="col-w-120">P. Unitario</th>
                            <th class="col-w-120">Subtotal</th>
                            <th class="col-w-80">Acción</th>
                        </tr>
                    </thead>
                    <tbody id="productsTableBody">
                        <tr id="emptyRow">
                            <td colspan="5" class="empty-message-cell">
                                No hay productos agregados
                            </td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="3" class="text-right">TOTAL:</td>
                            <td id="totalAmount">S/ 0.00</td>
                            <td></td>
                        </tr>
                    </tfoot>
                </table>
                
                <input type="hidden" name="total" id="totalInput" value="0">
                
                <div class="form-actions-end mt-30">
                    <a href="/compras/" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Guardar Compra</button>
                </div>
            </form>
        </div>
        
        <script src="/static/js/purchase-manager.js"></script>
        """
        
        return Layout.render('Nueva Compra', user, 'compras', content)
    
    @staticmethod
    def edit(user, purchase, suppliers, products, details, request, error=None):
        """Vista de formulario para editar compra"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        # Select de proveedores
        suppliers_options = ''
        for supplier in suppliers:
            selected = 'selected' if supplier['id'] == purchase['proveedor_id'] else ''
            suppliers_options += f'<option value="{supplier["id"]}" {selected}>{supplier["nombre"]}</option>'
        
        # Select de productos
        products_options = '<option value="">Seleccione un producto</option>'
        for product in products:
            products_options += f'<option value="{product["id"]}" data-price="{product["precio_venta"]}">{product["nombre"]} - S/ {product["precio_venta"]:.2f}</option>'
        
        # Estados
        estados = ['pendiente', 'completada', 'cancelada']
        estado_options = ''
        for estado in estados:
            selected = 'selected' if estado == purchase['estado'] else ''
            estado_options += f'<option value="{estado}" {selected}>{estado.capitalize()}</option>'
        
        # Detalles iniciales en JavaScript
        details_json = '[]'
        if details:
            import json
            details_data = []
            for detail in details:
                details_data.append({
                    'producto_id': detail['producto_id'],
                    'producto_nombre': detail['producto_nombre'],
                    'cantidad': detail['cantidad'],
                    'precio_unitario': float(detail['precio_unitario']),
                    'subtotal': float(detail['subtotal'])
                })
            details_json = json.dumps(details_data)
        
        content = f"""
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="h3 mb-0">Editar Compra #{purchase['id']}</h1>
            <a href="/compras/" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Volver
            </a>
        </div>
        
        {error_html}
        
        <div class="card shadow-sm">
            <div class="card-body">
                <form method="POST" id="purchaseForm">
                    {csrf_token}
                    <input type="hidden" name="details" id="detailsInput" value="">
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">N° Factura</label>
                            <input type="text" class="form-control" name="numero_factura" value="{purchase.get('numero_factura', '')}">
                        </div>
                        
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Proveedor <span class="text-danger">*</span></label>
                            <select class="form-select" name="proveedor_id" required>
                                {suppliers_options}
                            </select>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Fecha <span class="text-danger">*</span></label>
                            <input type="date" class="form-control" name="fecha" value="{purchase['fecha']}" required>
                        </div>
                        
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Estado</label>
                            <select class="form-select" name="estado">
                                {estado_options}
                            </select>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Notas</label>
                        <textarea class="form-control" name="notas" rows="2">{purchase.get('notas', '')}</textarea>
                    </div>
                    
                    <hr class="my-4">
                    
                    <h5 class="mb-3">Productos</h5>
                    
                    <div class="row mb-3">
                        <div class="col-md-5">
                            <label class="form-label">Producto</label>
                            <select class="form-select" id="productSelect">
                                {products_options}
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Cantidad</label>
                            <input type="number" class="form-control" id="quantityInput" min="1" value="1">
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Precio Unitario</label>
                            <input type="number" class="form-control" id="priceInput" min="0" step="0.01" value="0">
                        </div>
                        <div class="col-md-1 d-flex align-items-end">
                            <button type="button" class="btn btn-success w-100" id="addProductBtn">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-bordered" id="productsTable">
                            <thead class="table-light">
                                <tr>
                                    <th>Producto</th>
                                    <th width="100">Cantidad</th>
                                    <th width="120">P. Unitario</th>
                                    <th width="120">Subtotal</th>
                                    <th width="80">Acción</th>
                                </tr>
                            </thead>
                            <tbody id="productsTableBody">
                                <tr id="emptyRow">
                                    <td colspan="5" class="text-center text-muted">
                                        No hay productos agregados
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr class="table-light fw-bold">
                                    <td colspan="3" class="text-end">TOTAL:</td>
                                    <td id="totalAmount">S/ 0.00</td>
                                    <td></td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>
                    
                    <input type="hidden" name="total" id="totalInput" value="0">
                    
                    <div class="d-flex justify-content-end gap-2 mt-4">
                        <a href="/compras/" class="btn btn-secondary">Cancelar</a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i> Actualizar Compra
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <script src="/static/js/purchase-manager.js"></script>
        <script>
        // Cargar detalles existentes
        const existingDetails = {details_json};
        document.addEventListener('DOMContentLoaded', function() {{
            loadExistingDetails(existingDetails);
        }});
        </script>
        """
        
        return Layout.render('Editar Compra', user, 'compras', content)
    
    @staticmethod
    def view(user, purchase, details):
        """Vista de detalle de una compra"""
        
        estado_class = {
            'pendiente': 'warning',
            'completada': 'success',
            'cancelada': 'danger'
        }.get(purchase['estado'], 'secondary')
        
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
            <h1 class="h3 mb-0">Detalle de Compra #{purchase['id']}</h1>
            <div>
                <a href="/compras/{purchase['id']}/editar/" class="btn btn-warning">
                    <i class="fas fa-edit"></i> Editar
                </a>
                <a href="/compras/" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Volver
                </a>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Información de la Compra</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-2">
                            <strong>N° Factura:</strong> {purchase.get('numero_factura', 'N/A')}
                        </div>
                        <div class="mb-2">
                            <strong>Proveedor:</strong> {purchase['proveedor_nombre']}
                        </div>
                        <div class="mb-2">
                            <strong>Fecha:</strong> {purchase['fecha']}
                        </div>
                        <div class="mb-2">
                            <strong>Estado:</strong> 
                            <span class="badge bg-{estado_class}">{purchase['estado']}</span>
                        </div>
                        <div class="mb-2">
                            <strong>Usuario:</strong> {purchase['usuario_nombre']}
                        </div>
                        <div class="mb-2">
                            <strong>Notas:</strong> {purchase.get('notas', 'Sin notas')}
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
                            <span class="h3 mb-0 text-success">S/ {purchase['total']:.2f}</span>
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
        
        return Layout.render('Detalle de Compra', user, 'compras', content)
