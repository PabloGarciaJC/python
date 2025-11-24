from django.http import HttpResponse
from app.views.layout import Layout

class RoleView:
    """Vista de Roles"""
    
    @staticmethod
    def index(user, roles):
        """Renderiza la página de listado de roles"""
        
        # Generar las filas de la tabla
        if roles:
            rows = ""
            for idx, role in enumerate(roles, 1):
                rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{role['nombre']}</td>
                    <td>{role.get('descripcion', 'Sin descripción')}</td>
                    <td>
                        <a href="/roles/{role['id']}/editar/" class="btn btn-warning" style="text-decoration: none;">Editar</a>
                        <a href="/roles/{role['id']}/eliminar/" class="btn btn-danger" style="text-decoration: none;" onclick="return confirm('¿Está seguro de eliminar este rol?');">Eliminar</a>
                    </td>
                </tr>
                """
            
            table_content = f"""
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Nombre</th>
                        <th>Descripción</th>
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
                <div style="font-size: 4rem; margin-bottom: 20px;">🔐</div>
                <h3>No hay roles registrados</h3>
                <p>Comienza agregando tu primer rol</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Roles</span>
                <a href="/roles/crear/" class="btn btn-primary">+ Nuevo Rol</a>
            </div>
            {table_content}
        </div>
        """
        
        return HttpResponse(Layout.render('Roles', user, 'roles', content))
    
    @staticmethod
    def create(user, request, error=None):
        """Vista del formulario de crear rol"""
        
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
                <span>Crear Nuevo Rol</span>
                <a href="/roles/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/roles/crear/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                    <input type="text" name="nombre" required 
                           style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Descripción</label>
                    <textarea name="descripcion" rows="4" 
                              style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;"></textarea>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Guardar Rol</button>
                    <a href="/roles/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Crear Rol', user, 'roles', content))
    
    @staticmethod
    def edit(user, role, request, error=None):
        """Vista del formulario de editar rol"""
        
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
                <span>Editar Rol</span>
                <a href="/roles/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/roles/{role['id']}/editar/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                    <input type="text" name="nombre" value="{role['nombre']}" required 
                           style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Descripción</label>
                    <textarea name="descripcion" rows="4" 
                              style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">{role.get('descripcion', '')}</textarea>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Actualizar Rol</button>
                    <a href="/roles/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Rol', user, 'roles', content))
