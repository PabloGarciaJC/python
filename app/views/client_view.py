from django.http import HttpResponse
from app.views.layout import Layout

class ClientView:
    """Vista de Clientes"""
    
    @staticmethod
    def index(user, clients):
        """Renderiza la página de listado de clientes"""
        
        # Generar las filas de la tabla
        if clients:
            rows = ""
            for idx, client in enumerate(clients, 1):
                rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{client['nombre']}</td>
                    <td>{client.get('documento', 'N/A')}</td>
                    <td>{client.get('telefono', 'N/A')}</td>
                    <td>{client.get('email', 'N/A')}</td>
                    <td>
                        <a href="/clientes/{client['id']}/editar/" class="btn btn-warning no-underline">Editar</a>
                        <a href="/clientes/{client['id']}/eliminar/" class="btn btn-danger no-underline" onclick="return confirm('¿Está seguro de eliminar este cliente?');">Eliminar</a>
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
                        <th>Documento</th>
                        <th>Teléfono</th>
                        <th>Email</th>
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
                <div class="icon-4xl"><i class="fas fa-users"></i></div>
                <h3>No hay clientes registrados</h3>
                <p>Comienza agregando tu primer cliente</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Clientes</span>
                <a href="/clientes/crear/" class="btn btn-primary">+ Nuevo Cliente</a>
            </div>
            {table_content}
        </div>
        """
        
        return HttpResponse(Layout.render('Clientes', user, 'clientes', content))
    
    @staticmethod
    def create(user, request, error=None):
        """Vista del formulario de crear cliente"""
        
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
                <span>Crear Nuevo Cliente</span>
                <a href="/clientes/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/clientes/crear/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Nombre Completo *</label>
                        <input type="text" name="nombre" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Documento (DNI/RUC)</label>
                        <input type="text" name="documento" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Teléfono</label>
                        <input type="text" name="telefono" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Email</label>
                        <input type="email" name="email" class="form-input">
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Dirección</label>
                    <textarea name="direccion" rows="3" class="form-textarea"></textarea>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Guardar Cliente</button>
                    <a href="/clientes/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Crear Cliente', user, 'clientes', content))
    
    @staticmethod
    def edit(user, client, request, error=None):
        """Vista del formulario de editar cliente"""
        
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
                <span>Editar Cliente</span>
                <a href="/clientes/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/clientes/{client['id']}/editar/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Nombre Completo *</label>
                        <input type="text" name="nombre" value="{client['nombre']}" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Documento (DNI/RUC)</label>
                        <input type="text" name="documento" value="{client.get('documento', '')}" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Teléfono</label>
                        <input type="text" name="telefono" value="{client.get('telefono', '')}" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Email</label>
                        <input type="email" name="email" value="{client.get('email', '')}" class="form-input">
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Dirección</label>
                    <textarea name="direccion" rows="3" class="form-textarea">{client.get('direccion', '')}</textarea>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Actualizar Cliente</button>
                    <a href="/clientes/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Cliente', user, 'clientes', content))
