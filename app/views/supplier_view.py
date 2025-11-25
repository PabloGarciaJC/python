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
                        <form method="POST" action="/proveedores/{supplier['id']}/eliminar/" class="d-inline">
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
            <div class="table-container">
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
            </div>
            """
        else:
            table_content = """
            <div class="empty-state">
                <i class="fas fa-truck icon-4xl"></i>
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
            <div class="alert-error">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nuevo Proveedor</span>
                <a href="/proveedores/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/proveedores/crear/" class="p-20">
                {csrf_token}
                <div class="form-grid">
                    <div>
                        <label class="form-label">Nombre *</label>
                        <input type="text" name="nombre" required
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">RUC</label>
                        <input type="text" name="ruc" maxlength="20"
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Teléfono</label>
                        <input type="text" name="telefono" maxlength="20"
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Email</label>
                        <input type="email" name="email" maxlength="100"
                               class="form-input">
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Dirección</label>
                    <textarea name="direccion" rows="3"
                              class="form-textarea"></textarea>
                </div>
                
                <div class="form-actions-end mt-30">
                    <a href="/proveedores/" class="btn btn-secondary">Cancelar</a>
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
            <div class="alert-error">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Proveedor</span>
                <a href="/proveedores/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/proveedores/{supplier['id']}/editar/" class="p-20">
                {csrf_token}
                <div class="form-grid">
                    <div>
                        <label class="form-label">Nombre *</label>
                        <input type="text" name="nombre" value="{supplier['nombre']}" required
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">RUC</label>
                        <input type="text" name="ruc" value="{supplier.get('ruc', '')}" maxlength="20"
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Teléfono</label>
                        <input type="text" name="telefono" value="{supplier.get('telefono', '')}" maxlength="20"
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Email</label>
                        <input type="email" name="email" value="{supplier.get('email', '')}" maxlength="100"
                               class="form-input">
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Dirección</label>
                    <textarea name="direccion" rows="3"
                              class="form-textarea">{supplier.get('direccion', '')}</textarea>
                </div>
                
                <div class="form-actions-end mt-30">
                    <a href="/proveedores/" class="btn btn-secondary">Cancelar</a>
                    <button type="submit" class="btn btn-primary">Actualizar Proveedor</button>
                </div>
            </form>
        </div>
        """
        
        return Layout.render('Editar Proveedor', user, 'proveedores', content)
