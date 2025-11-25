from django.http import HttpResponse
from app.views.layout import Layout

class ProductView:
    """Vista de Productos"""
    
    @staticmethod
    def index(user, request_path, products):
        """Vista de lista de productos"""
        
        # Generar filas de la tabla
        if products:
            rows = ''
            for product in products:
                rows += f"""
                <tr>
                    <td>{product['id']}</td>
                    <td>{product['nombre']}</td>
                    <td>{product.get('categoria', 'Sin categoría')}</td>
                    <td>${product['precio_venta']}</td>
                    <td>{product['stock_actual']}</td>
                    <td>
                        <a href="/productos/{product['id']}/editar/" class="btn btn-warning no-underline">Editar</a>
                        <a href="/productos/{product['id']}/eliminar/" class="btn btn-danger no-underline" onclick="return confirm('¿Está seguro de eliminar este producto?');">Eliminar</a>
                    </td>
                </tr>
                """
            
            table_content = f"""
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Categoría</th>
                            <th>Precio</th>
                            <th>Stock</th>
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
                <div class="icon-4xl"><i class="fas fa-box"></i></div>
                <h3>No hay productos registrados</h3>
                <p>Comienza agregando tu primer producto</p>
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Productos</span>
                <a href="/productos/crear/" class="btn btn-primary">+ Nuevo Producto</a>
            </div>
            {table_content}
        </div>
        """
        
        return HttpResponse(Layout.render('Productos', user, 'productos', content))
    
    @staticmethod
    def create(user, categories, request, error=None):
        """Vista del formulario de crear producto"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Generar opciones de categorías
        category_options = ""
        for category in categories:
            category_options += f'<option value="{category["id"]}">{category["nombre"]}</option>'
        
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
                <span>Crear Nuevo Producto</span>
                <a href="/productos/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/productos/crear/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <div class="form-grid">
                    <div>
                        <label class="form-label">Código *</label>
                        <input type="text" name="codigo" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Nombre *</label>
                        <input type="text" name="nombre" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Categoría *</label>
                        <select name="categoria_id" required class="form-select">
                            <option value="">Seleccione una categoría</option>
                            {category_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Precio Compra *</label>
                        <input type="number" name="precio_compra" step="0.01" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Precio Venta *</label>
                        <input type="number" name="precio_venta" step="0.01" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Stock Actual</label>
                        <input type="number" name="stock_actual" value="0" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Stock Mínimo</label>
                        <input type="number" name="stock_minimo" value="10" class="form-input">
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Descripción</label>
                    <textarea name="descripcion" rows="4" class="form-textarea"></textarea>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Guardar Producto</button>
                    <a href="/productos/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Crear Producto', user, 'productos', content))
    
    @staticmethod
    def edit(user, product, categories, request, error=None):
        """Vista del formulario de editar producto"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Generar opciones de categorías
        category_options = ""
        for category in categories:
            selected = 'selected' if category['id'] == product.get('categoria_id') else ''
            category_options += f'<option value="{category["id"]}" {selected}>{category["nombre"]}</option>'
        
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
                <span>Editar Producto</span>
                <a href="/productos/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/productos/{product['id']}/editar/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <div class="form-grid">
                    <div>
                        <label class="form-label">Código *</label>
                        <input type="text" name="codigo" value="{product['codigo']}" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Nombre *</label>
                        <input type="text" name="nombre" value="{product['nombre']}" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Categoría *</label>
                        <select name="categoria_id" required class="form-select">
                            <option value="">Seleccione una categoría</option>
                            {category_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Precio Compra *</label>
                        <input type="number" name="precio_compra" value="{product['precio_compra']}" step="0.01" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Precio Venta *</label>
                        <input type="number" name="precio_venta" value="{product['precio_venta']}" step="0.01" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Stock Actual</label>
                        <input type="number" name="stock_actual" value="{product['stock_actual']}" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Stock Mínimo</label>
                        <input type="number" name="stock_minimo" value="{product.get('stock_minimo', 10)}" class="form-input">
                    </div>
                </div>
                
                <div class="mt-20">
                    <label class="form-label">Descripción</label>
                    <textarea name="descripcion" rows="4" class="form-textarea">{product.get('descripcion', '')}</textarea>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Actualizar Producto</button>
                    <a href="/productos/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Producto', user, 'productos', content))

