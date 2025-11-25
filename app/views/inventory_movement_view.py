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
                    'ajuste': '<span class="badge badge-info">Ajuste</span>'
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
                        <a href="/movimientos-inventario/{movement['id']}/ver/" class="btn btn-info">Ver</a>
                        <a href="/movimientos-inventario/{movement['id']}/editar/" class="btn btn-warning">Editar</a>
                        <form method="POST" action="/movimientos-inventario/{movement['id']}/eliminar/" class="d-inline">
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
            <div class="table-container">
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
            </div>
            """
        else:
            table_content = """
            <div class="empty-state">
                <i class="fas fa-exchange-alt icon-4xl"></i>
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
            <div class="alert-error">
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
                <a href="/movimientos-inventario/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/movimientos-inventario/crear/" class="p-20">
                {csrf_token}
                <div class="form-grid">
                    <div>
                        <label class="form-label">Producto *</label>
                        <select name="producto_id" required class="form-select">
                            {product_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Almacén *</label>
                        <select name="almacen_id" required class="form-select">
                            {warehouse_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Tipo de Movimiento *</label>
                        <select name="tipo_movimiento" required class="form-select">
                            <option value="">Seleccione un tipo</option>
                            <option value="entrada">Entrada</option>
                            <option value="salida">Salida</option>
                            <option value="ajuste">Ajuste</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Cantidad *</label>
                        <input type="number" name="cantidad" value="1" min="1" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Referencia</label>
                        <input type="text" name="referencia" maxlength="100" placeholder="Opcional" class="form-input">
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Motivo</label>
                    <textarea name="motivo" rows="3" placeholder="Opcional" class="form-textarea"></textarea>
                </div>
                
                <div class="form-actions-end mt-30">
                    <a href="/movimientos-inventario/" class="btn btn-secondary">Cancelar</a>
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
            <div class="alert-error">
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
                <a href="/movimientos-inventario/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/movimientos-inventario/{movement['id']}/editar/" class="p-20">
                {csrf_token}
                <div class="form-grid">
                    <div>
                        <label class="form-label">Producto *</label>
                        <select name="producto_id" required class="form-select">
                            {product_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Almacén *</label>
                        <select name="almacen_id" required class="form-select">
                            {warehouse_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Tipo de Movimiento *</label>
                        <select name="tipo_movimiento" required class="form-select">
                            {tipo_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Cantidad *</label>
                        <input type="number" name="cantidad" value="{movement['cantidad']}" min="1" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Referencia</label>
                        <input type="text" name="referencia" value="{movement.get('referencia', '')}" maxlength="100" class="form-input">
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Motivo</label>
                    <textarea name="motivo" rows="3" class="form-textarea">{movement.get('motivo', '')}</textarea>
                </div>
                
                <div class="form-actions-end mt-30">
                    <a href="/movimientos-inventario/" class="btn btn-secondary">Cancelar</a>
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
            'ajuste': '<span class="badge badge-info">Ajuste</span>'
        }.get(movement['tipo_movimiento'], movement['tipo_movimiento'])
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Detalle de Movimiento #{movement['id']}</span>
                <a href="/movimientos-inventario/" class="btn btn-secondary">← Volver</a>
            </div>
            
            <div class="p-20">
                <div class="info-grid">
                    <div class="info-box">
                        <p class="info-box-label">Producto</p>
                        <p class="info-box-value">{movement['producto_nombre']}</p>
                    </div>
                    
                    <div class="info-box">
                        <p class="info-box-label">Almacén</p>
                        <p class="info-box-value">{movement['almacen_nombre']}</p>
                    </div>
                    
                    <div class="info-box">
                        <p class="info-box-label">Tipo de Movimiento</p>
                        <p class="info-box-value">{tipo_badge}</p>
                    </div>
                    
                    <div class="info-box">
                        <p class="info-box-label">Cantidad</p>
                        <p class="info-box-value info-box-value-lg">{movement['cantidad']} unidades</p>
                    </div>
                    
                    <div class="info-box">
                        <p class="info-box-label">Referencia</p>
                        <p class="info-box-value">{movement.get('referencia', 'N/A')}</p>
                    </div>
                    
                    <div class="info-box">
                        <p class="info-box-label">Fecha</p>
                        <p class="info-box-value">{movement['fecha']}</p>
                    </div>
                    
                    <div class="info-box">
                        <p class="info-box-label">Usuario</p>
                        <p class="info-box-value">{movement['usuario_nombre']}</p>
                    </div>
                </div>
                
                {f'''
                <div class="info-box mt-20">
                    <p class="info-box-label">Motivo</p>
                    <p class="info-box-value info-box-text">{movement['motivo']}</p>
                </div>
                ''' if movement.get('motivo') else ''}
                
                <div class="mt-30 d-flex gap-10">
                    <a href="/movimientos-inventario/{movement['id']}/editar/" class="btn btn-warning">Editar Movimiento</a>
                    <a href="/movimientos-inventario/" class="btn btn-secondary">Volver al Listado</a>
                </div>
            </div>
        </div>
        """
        
        return Layout.render('Ver Movimiento', user, 'movimientos-inventario', content)
