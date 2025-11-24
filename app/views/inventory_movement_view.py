from django.http import HttpResponse
from app.views.layout import Layout

class InventoryMovementView:
    @staticmethod
    def index(user, movements, request):
        """Vista de lista de movimientos de inventario"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
        # Tabla de movimientos
        rows = ""
        if movements:
            for idx, movement in enumerate(movements, 1):
                tipo_badge = {
                    'entrada': '<span class="badge badge-success">Entrada</span>',
                    'salida': '<span class="badge badge-warning">Salida</span>',
                    'ajuste': '<span style="padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; background: #dbeafe; color: #1e40af;">Ajuste</span>'
                }.get(movement['tipo_movimiento'], movement['tipo_movimiento'])
                
                rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{movement['producto_nombre']}</td>
                    <td>{movement['almacen_nombre']}</td>
                    <td>{tipo_badge}</td>
                    <td>{movement['cantidad']}</td>
                    <td>{movement.get('referencia', 'N/A')}</td>
                    <td>{movement['fecha']}</td>
                    <td>{movement['usuario_nombre']}</td>
                    <td>
                        <a href="/movimientos-inventario/{movement['id']}/ver/" class="btn" style="background: #3b82f6; color: white; padding: 8px 15px; font-size: 13px;">Ver</a>
                        <a href="/movimientos-inventario/{movement['id']}/editar/" class="btn btn-warning">Editar</a>
                        <form method="POST" action="/movimientos-inventario/{movement['id']}/eliminar/" style="display: inline;">
                            {csrf_token}
                            <button type="submit" class="btn btn-danger" 
                                    onclick="return confirm('¿Estás seguro de eliminar este movimiento?')">
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
                        <th>Producto</th>
                        <th>Almacén</th>
                        <th>Tipo</th>
                        <th>Cantidad</th>
                        <th>Referencia</th>
                        <th>Fecha</th>
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
                <div style="font-size: 4rem; margin-bottom: 20px;">📦</div>
                <h3>No hay movimientos de inventario registrados</h3>
                <p>Comienza registrando el primer movimiento</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Movimientos de Inventario</span>
                <a href="/movimientos-inventario/crear/" class="btn btn-primary">+ Nuevo Movimiento</a>
            </div>
            {table_content}
        </div>
        """
        
        return Layout.render('Movimientos de Inventario', user, 'movimientos-inventario', content)
    
    @staticmethod
    def create(user, products, warehouses, request, error=None):
        """Vista de formulario para crear movimiento de inventario"""
        
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
        product_options = '<option value="">Seleccione un producto</option>'
        for product in products:
            product_options += f'<option value="{product["id"]}">{product["nombre"]}</option>'
        
        # Select de almacenes
        warehouse_options = '<option value="">Seleccione un almacén</option>'
        for warehouse in warehouses:
            warehouse_options += f'<option value="{warehouse["id"]}">{warehouse["nombre"]}</option>'
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Registrar Nuevo Movimiento de Inventario</span>
                <a href="/movimientos-inventario/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/movimientos-inventario/crear/" style="padding: 20px;">
                {csrf_token}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Producto *</label>
                        <select name="producto_id" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {product_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Almacén *</label>
                        <select name="almacen_id" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {warehouse_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Tipo de Movimiento *</label>
                        <select name="tipo_movimiento" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            <option value="">Seleccione un tipo</option>
                            <option value="entrada">Entrada</option>
                            <option value="salida">Salida</option>
                            <option value="ajuste">Ajuste</option>
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Cantidad *</label>
                        <input type="number" name="cantidad" value="1" min="1" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Referencia</label>
                        <input type="text" name="referencia" maxlength="100" placeholder="Opcional"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Motivo</label>
                    <textarea name="motivo" rows="3" placeholder="Opcional"
                              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; resize: vertical;"></textarea>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: flex-end;">
                    <a href="/movimientos-inventario/" class="btn" style="background: #6b7280; color: white;">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Registrar Movimiento</button>
                </div>
            </form>
        </div>
        """
        
        return Layout.render('Nuevo Movimiento', user, 'movimientos-inventario', content)
    
    @staticmethod
    def edit(user, movement, products, warehouses, request, error=None):
        """Vista de formulario para editar movimiento de inventario"""
        
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
            selected = 'selected' if product['id'] == movement['producto_id'] else ''
            product_options += f'<option value="{product["id"]}" {selected}>{product["nombre"]}</option>'
        
        # Select de almacenes
        warehouse_options = ""
        for warehouse in warehouses:
            selected = 'selected' if warehouse['id'] == movement['almacen_id'] else ''
            warehouse_options += f'<option value="{warehouse["id"]}" {selected}>{warehouse["nombre"]}</option>'
        
        # Select de tipo de movimiento
        tipos = [
            {'value': 'entrada', 'label': 'Entrada'},
            {'value': 'salida', 'label': 'Salida'},
            {'value': 'ajuste', 'label': 'Ajuste'}
        ]
        tipo_options = ""
        for tipo in tipos:
            selected = 'selected' if tipo['value'] == movement['tipo_movimiento'] else ''
            tipo_options += f'<option value="{tipo["value"]}" {selected}>{tipo["label"]}</option>'
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Movimiento de Inventario</span>
                <a href="/movimientos-inventario/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/movimientos-inventario/{movement['id']}/editar/" style="padding: 20px;">
                {csrf_token}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Producto *</label>
                        <select name="producto_id" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {product_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Almacén *</label>
                        <select name="almacen_id" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {warehouse_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Tipo de Movimiento *</label>
                        <select name="tipo_movimiento" required
                                style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                            {tipo_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Cantidad *</label>
                        <input type="number" name="cantidad" value="{movement['cantidad']}" min="1" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Referencia</label>
                        <input type="text" name="referencia" value="{movement.get('referencia', '')}" maxlength="100"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Motivo</label>
                    <textarea name="motivo" rows="3"
                              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; resize: vertical;">{movement.get('motivo', '')}</textarea>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: flex-end;">
                    <a href="/movimientos-inventario/" class="btn" style="background: #6b7280; color: white;">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Actualizar Movimiento</button>
                </div>
            </form>
        </div>
        """
        
        return Layout.render('Editar Movimiento', user, 'movimientos-inventario', content)
    
    @staticmethod
    def view(user, movement):
        """Vista de detalle de movimiento de inventario"""
        
        tipo_badge = {
            'entrada': '<span class="badge badge-success">Entrada</span>',
            'salida': '<span class="badge badge-warning">Salida</span>',
            'ajuste': '<span style="padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; background: #dbeafe; color: #1e40af;">Ajuste</span>'
        }.get(movement['tipo_movimiento'], movement['tipo_movimiento'])
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Detalle de Movimiento #{movement['id']}</span>
                <a href="/movimientos-inventario/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            
            <div style="padding: 20px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Producto</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827; font-size: 16px;">{movement['producto_nombre']}</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Almacén</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827; font-size: 16px;">{movement['almacen_nombre']}</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Tipo de Movimiento</p>
                        <p style="margin: 5px 0 0 0;">{tipo_badge}</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Cantidad</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827; font-size: 18px;">{movement['cantidad']} unidades</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Referencia</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827;">{movement.get('referencia', 'N/A')}</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Fecha</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827;">{movement['fecha']}</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
                        <p style="margin: 0; color: #6b7280; font-size: 13px;">Usuario</p>
                        <p style="margin: 5px 0 0 0; font-weight: 600; color: #111827;">{movement['usuario_nombre']}</p>
                    </div>
                </div>
                
                {f'''
                <div style="margin-top: 20px; background: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
                    <p style="margin: 0; color: #6b7280; font-size: 13px;">Motivo</p>
                    <p style="margin: 5px 0 0 0; color: #111827; line-height: 1.6;">{movement['motivo']}</p>
                </div>
                ''' if movement.get('motivo') else ''}
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <a href="/movimientos-inventario/{movement['id']}/editar/" class="btn btn-warning">Editar Movimiento</a>
                    <a href="/movimientos-inventario/" class="btn" style="background: #6b7280; color: white;">Volver al Listado</a>
                </div>
            </div>
        </div>
        """
        
        return Layout.render('Ver Movimiento', user, 'movimientos-inventario', content)
