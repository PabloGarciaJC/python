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
                        <a href="/clientes/{client['id']}/editar/" class="btn btn-warning" style="text-decoration: none;">Editar</a>
                        <a href="/clientes/{client['id']}/eliminar/" class="btn btn-danger" style="text-decoration: none;" onclick="return confirm('¿Está seguro de eliminar este cliente?');">Eliminar</a>
                    </td>
                </tr>
                """
            
            table_content = f"""
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
            """
        else:
            table_content = """
            <div class="empty-state">
                <div style="font-size: 4rem; margin-bottom: 20px;">👥</div>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nuevo Cliente</span>
                <a href="/clientes/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/clientes/crear/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre Completo *</label>
                        <input type="text" name="nombre" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Documento (DNI/RUC)</label>
                        <input type="text" name="documento" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Teléfono</label>
                        <input type="text" name="telefono" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email</label>
                        <input type="email" name="email" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Dirección</label>
                    <textarea name="direccion" rows="3" 
                              style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;"></textarea>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Guardar Cliente</button>
                    <a href="/clientes/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Cliente</span>
                <a href="/clientes/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/clientes/{client['id']}/editar/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre Completo *</label>
                        <input type="text" name="nombre" value="{client['nombre']}" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Documento (DNI/RUC)</label>
                        <input type="text" name="documento" value="{client.get('documento', '')}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Teléfono</label>
                        <input type="text" name="telefono" value="{client.get('telefono', '')}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email</label>
                        <input type="email" name="email" value="{client.get('email', '')}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Dirección</label>
                    <textarea name="direccion" rows="3" 
                              style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">{client.get('direccion', '')}</textarea>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Actualizar Cliente</button>
                    <a href="/clientes/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Cliente', user, 'clientes', content))
