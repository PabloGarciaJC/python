from django.http import HttpResponse
from app.views.layout import Layout

class CategoryView:
    """Vista de Categorías"""
    
    @staticmethod
    def index(user, categories):
        """Renderiza la página de listado de categorías"""
        
        # Generar las filas de la tabla
        if categories:
            rows = ""
            for idx, category in enumerate(categories, 1):
                rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{category['nombre']}</td>
                    <td>{category['descripcion'] or 'Sin descripción'}</td>
                    <td>
                        <a href="/categorias/{category['id']}/editar/" class="btn btn-warning no-underline">Editar</a>
                        <a href="/categorias/{category['id']}/eliminar/" class="btn btn-danger no-underline" onclick="return confirm('¿Está seguro de eliminar esta categoría?');">Eliminar</a>
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
                <div class="icon-4xl"><i class="fas fa-folder"></i></div>
                <h3>No hay categorías registradas</h3>
                <p>Comienza agregando tu primera categoría</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Categorías</span>
                <a href="/categorias/crear/" class="btn btn-primary">+ Nueva Categoría</a>
            </div>
            {table_content}
        </div>
        """
        
        return HttpResponse(Layout.render('Categorías', user, 'categorias', content))
    
    @staticmethod
    def create(user, request, error=None):
        """Vista del formulario de crear categoría"""
        
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
                <span>Crear Nueva Categoría</span>
                <a href="/categorias/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/categorias/crear/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="mb-20">
                    <label class="form-label">Nombre *</label>
                    <input type="text" name="nombre" required class="form-input">
                </div>
                
                <div class="mb-20">
                    <label class="form-label">Descripción</label>
                    <textarea name="descripcion" rows="4" class="form-textarea"></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Guardar Categoría</button>
                    <a href="/categorias/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Crear Categoría', user, 'categorias', content))
    
    @staticmethod
    def edit(user, category, request, error=None):
        """Vista del formulario de editar categoría"""
        
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
                <span>Editar Categoría</span>
                <a href="/categorias/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/categorias/{category['id']}/editar/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="mb-20">
                    <label class="form-label">Nombre *</label>
                    <input type="text" name="nombre" value="{category['nombre']}" required class="form-input">
                </div>
                
                <div class="mb-20">
                    <label class="form-label">Descripción</label>
                    <textarea name="descripcion" rows="4" class="form-textarea">{category.get('descripcion', '')}</textarea>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Actualizar Categoría</button>
                    <a href="/categorias/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Categoría', user, 'categorias', content))

