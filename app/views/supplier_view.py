from django.http import HttpResponse
from django.middleware.csrf import get_token
from app.views.layout import Layout

class SupplierView:
    @staticmethod
    def index(user, suppliers, total, request):
        """Vista de lista de proveedores"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
        rows = ""
        if suppliers:
            for idx, supplier in enumerate(suppliers, 1):
                rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{supplier['nombre']}</td>
                    <td>{supplier.get('ruc', 'N/A')}</td>
                    <td>{supplier.get('telefono', 'N/A')}</td>
                    <td>{supplier.get('email', 'N/A')}</td>
                    <td>
                        <a href="/proveedores/{supplier['id']}/editar/" class="btn btn-warning">Editar</a>
                        <form method="POST" action="/proveedores/{supplier['id']}/eliminar/" style="display: inline;">
                            {csrf_token}
                            <button type="submit" class="btn btn-danger" 
                                    onclick="return confirm('¿Estás seguro de eliminar este proveedor?')">
                                Eliminar
                            </button>
                        </form>
                    </td>
                        </form>
                    </td>
                </tr>
                """
            
            table_content = f"""
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Nombre</th>
                        <th>RUC</th>
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
                <div style="font-size: 4rem; margin-bottom: 20px;">🚚</div>
                <h3>No hay proveedores registrados</h3>
                <p>Comienza agregando tu primer proveedor</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Gestión de Proveedores</span>
                <a href="/proveedores/crear/" class="btn btn-primary">+ Nuevo Proveedor</a>
            </div>
            {table_content}
        </div>
        """
        
        return Layout.render('Proveedores', user, 'proveedores', content)
    
    @staticmethod
    def create(user, request, error=None):
        """Vista de formulario para crear proveedor"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
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
                <span>Crear Nuevo Proveedor</span>
                <a href="/proveedores/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/proveedores/crear/" style="padding: 20px;">
                {csrf_token}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                        <input type="text" name="nombre" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">RUC</label>
                        <input type="text" name="ruc" maxlength="20"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Teléfono</label>
                        <input type="text" name="telefono" maxlength="20"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email</label>
                        <input type="email" name="email" maxlength="100"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Dirección</label>
                    <textarea name="direccion" rows="3"
                              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; resize: vertical;"></textarea>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: flex-end;">
                    <a href="/proveedores/" class="btn" style="background: #6b7280; color: white;">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Guardar Proveedor</button>
                </div>
            </form>
        </div>
        """
        
        return Layout.render('Nuevo Proveedor', user, 'proveedores', content)
    
    @staticmethod
    def edit(user, supplier, request, error=None):
        """Vista de formulario para editar proveedor"""
        
        from django.middleware.csrf import get_token
        csrf_token = f'<input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">'
        
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
                <span>Editar Proveedor</span>
                <a href="/proveedores/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/proveedores/{supplier['id']}/editar/" style="padding: 20px;">
                {csrf_token}
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                        <input type="text" name="nombre" value="{supplier['nombre']}" required
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">RUC</label>
                        <input type="text" name="ruc" value="{supplier.get('ruc', '')}" maxlength="20"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Teléfono</label>
                        <input type="text" name="telefono" value="{supplier.get('telefono', '')}" maxlength="20"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email</label>
                        <input type="email" name="email" value="{supplier.get('email', '')}" maxlength="100"
                               style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Dirección</label>
                    <textarea name="direccion" rows="3"
                              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; resize: vertical;">{supplier.get('direccion', '')}</textarea>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: flex-end;">
                    <a href="/proveedores/" class="btn" style="background: #6b7280; color: white;">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Actualizar Proveedor</button>
                </div>
            </form>
        </div>
        """
        
        return Layout.render('Editar Proveedor', user, 'proveedores', content)
