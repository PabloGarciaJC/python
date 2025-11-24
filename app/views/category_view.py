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
                        <a href="/categorias/{category['id']}/editar/" class="btn btn-warning" style="text-decoration: none;">Editar</a>
                        <a href="/categorias/{category['id']}/eliminar/" class="btn btn-danger" style="text-decoration: none;" onclick="return confirm('¿Está seguro de eliminar esta categoría?');">Eliminar</a>
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
                <div style="font-size: 4rem; margin-bottom: 20px;">📑</div>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nueva Categoría</span>
                <a href="/categorias/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/categorias/crear/" style="padding: 20px;">
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
                    <button type="submit" class="btn btn-primary">Guardar Categoría</button>
                    <a href="/categorias/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Categoría</span>
                <a href="/categorias/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/categorias/{category['id']}/editar/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                    <input type="text" name="nombre" value="{category['nombre']}" required 
                           style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Descripción</label>
                    <textarea name="descripcion" rows="4" 
                              style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">{category.get('descripcion', '')}</textarea>
                </div>
                
                <div style="display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Actualizar Categoría</button>
                    <a href="/categorias/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Categoría', user, 'categorias', content))

