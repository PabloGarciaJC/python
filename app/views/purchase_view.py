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
                    'cancelada': '<span style="padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; background: #fee2e2; color: #991b1b;">Cancelada</span>'
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
                        <a href="/compras/{purchase['id']}/ver/" class="btn" style="background: #3b82f6; color: white; padding: 8px 15px; font-size: 13px;">Ver</a>
                        <a href="/compras/{purchase['id']}/editar/" class="btn btn-warning">Editar</a>
                        <form method="POST" action="/compras/{purchase['id']}/eliminar/" style="display: inline;">
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
            """
        else:
            table_content = """
            <div class="empty-state">
                <div style="font-size: 4rem; margin-bottom: 20px;">🛒</div>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
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
                <a href="/compras/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/compras/crear/" id="purchaseForm" style="padding: 20px;">
                {csrf_token}
                <input type="hidden" name="details" id="detailsInput" value="[]">
                    
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">N° Factura</label>
                        <input type="text" name="numero_factura" placeholder="Opcional"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Proveedor *</label>
                        <select name="proveedor_id" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {suppliers_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Fecha *</label>
                        <input type="date" name="fecha" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Estado</label>
                        <select name="estado"
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            <option value="pendiente">Pendiente</option>
                            <option value="completada">Completada</option>
                            <option value="cancelada">Cancelada</option>
                        </select>
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Notas</label>
                    <textarea name="notas" rows="2"
                              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; resize: vertical;"></textarea>
                </div>
                
                <hr style="margin: 30px 0; border: none; border-top: 2px solid #f0f0f0;">
                
                <h3 style="margin-bottom: 20px; color: #333;">Productos</h3>
                
                <div style="display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 10px; margin-bottom: 20px; align-items: end;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Producto</label>
                        <select id="productSelect"
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {products_options}
                        </select>
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Cantidad</label>
                        <input type="number" id="quantityInput" min="1" value="1"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Precio Unitario</label>
                        <input type="number" id="priceInput" min="0" step="0.01" value="0"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    <div>
                        <button type="button" class="btn btn-success" id="addProductBtn">+ Agregar</button>
                    </div>
                </div>
                
                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <thead>
                        <tr style="background: #f8f9fa;">
                            <th style="padding: 15px; text-align: left; border-bottom: 1px solid #f0f0f0; color: #667eea; font-weight: 600;">Producto</th>
                            <th style="padding: 15px; text-align: left; border-bottom: 1px solid #f0f0f0; color: #667eea; font-weight: 600; width: 100px;">Cantidad</th>
                            <th style="padding: 15px; text-align: left; border-bottom: 1px solid #f0f0f0; color: #667eea; font-weight: 600; width: 120px;">P. Unitario</th>
                            <th style="padding: 15px; text-align: left; border-bottom: 1px solid #f0f0f0; color: #667eea; font-weight: 600; width: 120px;">Subtotal</th>
                            <th style="padding: 15px; text-align: left; border-bottom: 1px solid #f0f0f0; color: #667eea; font-weight: 600; width: 80px;">Acción</th>
                        </tr>
                    </thead>
                    <tbody id="productsTableBody">
                        <tr id="emptyRow">
                            <td colspan="5" style="padding: 40px; text-align: center; color: #6b7280;">
                                No hay productos agregados
                            </td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr style="background: #f8f9fa; font-weight: 600;">
                            <td colspan="3" style="padding: 15px; text-align: right; border-top: 1px solid #f0f0f0;">TOTAL:</td>
                            <td id="totalAmount" style="padding: 15px; border-top: 1px solid #f0f0f0;">S/ 0.00</td>
                            <td style="border-top: 1px solid #f0f0f0;"></td>
                        </tr>
                    </tfoot>
                </table>
                
                <input type="hidden" name="total" id="totalInput" value="0">
                
                <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: flex-end;">
                    <a href="/compras/" class="btn" style="background: #6b7280; color: white;">Cancelar</a>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
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
