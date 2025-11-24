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
                        <a href="/almacenes/{warehouse['id']}/editar/" class="btn btn-warning" style="text-decoration: none;">Editar</a>
                        <a href="/almacenes/{warehouse['id']}/eliminar/" class="btn btn-danger" style="text-decoration: none;" onclick="return confirm('¿Está seguro de eliminar este almacén?');">Eliminar</a>
                    </td>
                </tr>
                """
            
            table_content = f"""
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
            """
        else:
            table_content = """
            <div class="empty-state">
                <div style="font-size: 4rem; margin-bottom: 20px;">🏢</div>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nuevo Almacén</span>
                <a href="/almacenes/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/almacenes/crear/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                        <input type="text" name="nombre" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Ubicación</label>
                        <input type="text" name="ubicacion" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Capacidad</label>
                        <input type="number" name="capacidad" value="0" min="0" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Guardar Almacén</button>
                    <a href="/almacenes/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Almacén</span>
                <a href="/almacenes/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/almacenes/{warehouse['id']}/editar/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                        <input type="text" name="nombre" value="{warehouse['nombre']}" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Ubicación</label>
                        <input type="text" name="ubicacion" value="{warehouse.get('ubicacion', '')}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Capacidad</label>
                        <input type="number" name="capacidad" value="{warehouse.get('capacidad', 0)}" min="0" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Actualizar Almacén</button>
                    <a href="/almacenes/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Almacén', user, 'almacenes', content))
