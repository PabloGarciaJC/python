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
                        <a href="/roles/{role['id']}/editar/" class="btn btn-warning no-underline">Editar</a>
                        <a href="/roles/{role['id']}/eliminar/" class="btn btn-danger no-underline" onclick="return confirm('¿Está seguro de eliminar este rol?');">Eliminar</a>
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
                        <th>Descripción</th>
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
                <i class="fas fa-user-shield icon-4xl"></i>
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
            <div class="alert-error">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nuevo Rol</span>
                <a href="/roles/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/roles/crear/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-field">
                    <label class="form-label">Nombre *</label>
                    <input type="text" name="nombre" required 
                           class="form-input">
                </div>
                
                <div class="form-field">
                    <label class="form-label">Descripción</label>
                    <textarea name="descripcion" rows="4" 
                              class="form-textarea"></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Guardar Rol</button>
                    <a href="/roles/" class="btn btn-secondary no-underline">Cancelar</a>
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
            <div class="alert-error">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Rol</span>
                <a href="/roles/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/roles/{role['id']}/editar/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-field">
                    <label class="form-label">Nombre *</label>
                    <input type="text" name="nombre" value="{role['nombre']}" required 
                           class="form-input">
                </div>
                
                <div class="form-field">
                    <label class="form-label">Descripción</label>
                    <textarea name="descripcion" rows="4" 
                              class="form-textarea">{role.get('descripcion', '')}</textarea>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Actualizar Rol</button>
                    <a href="/roles/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Rol', user, 'roles', content))
