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
                        <a href="/detalle-ventas/{detail['id']}/ver/" class="btn" style="background: #3b82f6; color: white; padding: 8px 15px; font-size: 13px;">Ver</a>
                        <a href="/detalle-ventas/{detail['id']}/editar/" class="btn btn-warning">Editar</a>
                        <form method="POST" action="/detalle-ventas/{detail['id']}/eliminar/" style="display: inline;">
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
            """
        else:
            table_content = """
            <div class="empty-state">
                <div style="font-size: 4rem; margin-bottom: 20px;">📝</div>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
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
                <a href="/detalle-ventas/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/detalle-ventas/crear/" style="padding: 20px;" id="detailForm">
                {csrf_token}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Venta *</label>
                        <select name="venta_id" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {sale_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Producto *</label>
                        <select name="producto_id" id="producto" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {product_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Cantidad *</label>
                        <input type="number" name="cantidad" id="cantidad" value="1" min="1" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Precio Unitario *</label>
                        <input type="number" name="precio_unitario" id="precio_unitario" step="0.01" min="0" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background: #f3f4f6; border-radius: 8px;">
                    <p style="margin: 0; font-size: 18px; font-weight: 600;">
                        Subtotal: S/ <span id="subtotal">0.00</span>
                    </p>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: flex-end;">
                    <a href="/detalle-ventas/" class="btn" style="background: #6b7280; color: white;">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Guardar Detalle</button>
                </div>
            </form>
        </div>
        
        <script>
            const productoSelect = document.getElementById('producto');
            const cantidadInput = document.getElementById('cantidad');
            const precioInput = document.getElementById('precio_unitario');
            const subtotalSpan = document.getElementById('subtotal');
            
            productoSelect.addEventListener('change', function() {{
                const selectedOption = this.options[this.selectedIndex];
                const price = selectedOption.getAttribute('data-price');
                if (price) {{
                    precioInput.value = parseFloat(price).toFixed(2);
                    calcularSubtotal();
                }}
            }});
            
            cantidadInput.addEventListener('input', calcularSubtotal);
            precioInput.addEventListener('input', calcularSubtotal);
            
            function calcularSubtotal() {{
                const cantidad = parseFloat(cantidadInput.value) || 0;
                const precio = parseFloat(precioInput.value) || 0;
                const subtotal = cantidad * precio;
                subtotalSpan.textContent = subtotal.toFixed(2);
            }}
        </script>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
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
                <a href="/detalle-ventas/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/detalle-ventas/{detail['id']}/editar/" style="padding: 20px;" id="detailForm">
                {csrf_token}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Venta</label>
                        <input type="text" value="{detail.get('numero_factura', 'Sin factura')}" disabled
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; background: #f5f5f5;">
                        <small style="color: #666;">La venta no se puede cambiar</small>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Producto *</label>
                        <select name="producto_id" id="producto" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {product_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Cantidad *</label>
                        <input type="number" name="cantidad" id="cantidad" value="{detail['cantidad']}" min="1" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Precio Unitario *</label>
                        <input type="number" name="precio_unitario" id="precio_unitario" value="{detail['precio_unitario']}" step="0.01" min="0" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px; padding: 15px; background: #f3f4f6; border-radius: 8px;">
                    <p style="margin: 0; font-size: 18px; font-weight: 600;">
                        Subtotal: S/ <span id="subtotal">{detail['subtotal']:.2f}</span>
                    </p>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: flex-end;">
                    <a href="/detalle-ventas/" class="btn" style="background: #6b7280; color: white;">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Actualizar Detalle</button>
                </div>
            </form>
        </div>
        
        <script>
            const productoSelect = document.getElementById('producto');
            const cantidadInput = document.getElementById('cantidad');
            const precioInput = document.getElementById('precio_unitario');
            const subtotalSpan = document.getElementById('subtotal');
            
            productoSelect.addEventListener('change', function() {{
                const selectedOption = this.options[this.selectedIndex];
                const price = selectedOption.getAttribute('data-price');
                if (price) {{
                    precioInput.value = parseFloat(price).toFixed(2);
                    calcularSubtotal();
                }}
            }});
            
            cantidadInput.addEventListener('input', calcularSubtotal);
            precioInput.addEventListener('input', calcularSubtotal);
            
            function calcularSubtotal() {{
                const cantidad = parseFloat(cantidadInput.value) || 0;
                const precio = parseFloat(precioInput.value) || 0;
                const subtotal = cantidad * precio;
                subtotalSpan.textContent = subtotal.toFixed(2);
            }}
        </script>
        """
        
        return Layout.render('Editar Detalle de Venta', user, 'detalle-ventas', content)
    
    @staticmethod
    def view(user, detail):
        """Vista de detalle específico de venta"""
        
        estado_badge = {
            'pendiente': '<span class="badge badge-warning">Pendiente</span>',
            'completada': '<span class="badge badge-success">Completada</span>',
            'cancelada': '<span style="padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; background: #fee2e2; color: #991b1b;">Cancelada</span>'
        }.get(detail.get('venta_estado', ''), detail.get('venta_estado', ''))
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Detalle de Venta #{detail['id']}</span>
                <a href="/detalle-ventas/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            
            <div style="padding: 20px;">
                <div style="background: #f9fafb; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                    <h3 style="margin: 0 0 15px 0; color: #111827; font-size: 18px;">Información de la Venta</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">N° Factura</p>
                            <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827;">{detail.get('numero_factura', 'Sin factura')}</p>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">Cliente</p>
                            <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827;">{detail['cliente_nombre']}</p>
                            <p style="margin: 2px 0 0 0; font-size: 12px; color: #6b7280;">{detail.get('cliente_documento', '')}</p>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">Fecha</p>
                            <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827;">{detail['fecha_venta']}</p>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">Tipo de Pago</p>
                            <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827;">{detail.get('tipo_pago', 'N/A').capitalize()}</p>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">Estado</p>
                            <p style="margin: 5px 0 0 0;">{estado_badge}</p>
                        </div>
                        <div>
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">Total Venta</p>
                            <p style="margin: 5px 0 0 0; font-weight: 600; color: #059669; font-size: 18px;">S/ {detail['venta_total']:.2f}</p>
                        </div>
                    </div>
                </div>
                
                <h3 style="margin: 0 0 15px 0; color: #111827; font-size: 18px;">Detalle del Producto</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                    <div style="background: white; padding: 15px; border: 1px solid #e5e7eb; border-radius: 8px;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Producto</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827; font-size: 16px;">{detail['producto_nombre']}</p>
                    </div>
                    
                    <div style="background: white; padding: 15px; border: 1px solid #e5e7eb; border-radius: 8px;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Cantidad</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827; font-size: 16px;">{detail['cantidad']} unidades</p>
                    </div>
                    
                    <div style="background: white; padding: 15px; border: 1px solid #e5e7eb; border-radius: 8px;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Precio Unitario</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827; font-size: 16px;">S/ {detail['precio_unitario']:.2f}</p>
                    </div>
                    
                    <div style="background: white; padding: 15px; border: 1px solid #e5e7eb; border-radius: 8px;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Subtotal</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #059669; font-size: 18px;">S/ {detail['subtotal']:.2f}</p>
                    </div>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <a href="/detalle-ventas/{detail['id']}/editar/" class="btn btn-warning">Editar Detalle</a>
                    <a href="/detalle-ventas/" class="btn" style="background: #6b7280; color: white;">Volver al Listado</a>
                </div>
            </div>
        </div>
        """
        
        return Layout.render('Ver Detalle de Venta', user, 'detalle-ventas', content)
