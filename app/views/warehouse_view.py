from django.http import HttpResponse
from app.views.layout import Layout

class WarehouseView:
    """Vista de Almacenes"""
    
    @staticmethod
    def index(user, warehouses):
        """Renderiza la página de listado de almacenes"""
        
        # Generar las filas de la tabla
        if warehouses:
            rows = ""
            for idx, warehouse in enumerate(warehouses, 1):
                rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{warehouse['nombre']}</td>
                    <td>{warehouse.get('ubicacion', 'N/A')}</td>
                    <td>{warehouse.get('capacidad', 0):,}</td>
                    <td>
                        <a href="/almacenes/{warehouse['id']}/editar/" class="btn btn-warning no-underline">Editar</a>
                        <a href="/almacenes/{warehouse['id']}/eliminar/" class="btn btn-danger no-underline" onclick="return confirm('¿Está seguro de eliminar este almacén?');">Eliminar</a>
                    </td>
                </tr>
                """
            
            table_content = f"""
            <div class="table-container">
                <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Nombre</th>
                        <th>Ubicación</th>
                        <th>Capacidad</th>
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
                <i class="fas fa-warehouse icon-4xl"></i>
                <h3>No hay almacenes registrados</h3>
                <p>Comienza agregando tu primer almacén</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Almacenes</span>
                <a href="/almacenes/crear/" class="btn btn-primary">+ Nuevo Almacén</a>
            </div>
            {table_content}
        </div>
        """
        
        return HttpResponse(Layout.render('Almacenes', user, 'almacenes', content))
    
    @staticmethod
    def create(user, request, error=None):
        """Vista del formulario de crear almacén"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Mensaje de error si existe
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
                <span>Crear Nuevo Almacén</span>
                <a href="/almacenes/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/almacenes/crear/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Nombre *</label>
                        <input type="text" name="nombre" required 
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Ubicación</label>
                        <input type="text" name="ubicacion" 
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Capacidad</label>
                        <input type="number" name="capacidad" value="0" min="0" 
                               class="form-input">
                    </div>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Guardar Almacén</button>
                    <a href="/almacenes/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Crear Almacén', user, 'almacenes', content))
    
    @staticmethod
    def edit(user, warehouse, request, error=None):
        """Vista del formulario de editar almacén"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Mensaje de error si existe
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
                <span>Editar Almacén</span>
                <a href="/almacenes/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/almacenes/{warehouse['id']}/editar/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Nombre *</label>
                        <input type="text" name="nombre" value="{warehouse['nombre']}" required 
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Ubicación</label>
                        <input type="text" name="ubicacion" value="{warehouse.get('ubicacion', '')}" 
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Capacidad</label>
                        <input type="number" name="capacidad" value="{warehouse.get('capacidad', 0)}" min="0" 
                               class="form-input">
                    </div>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Actualizar Almacén</button>
                    <a href="/almacenes/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Almacén', user, 'almacenes', content))
