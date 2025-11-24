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
                        <a href="/productos/{product['id']}/editar/" class="btn btn-warning" style="text-decoration: none;">Editar</a>
                        <a href="/productos/{product['id']}/eliminar/" class="btn btn-danger" style="text-decoration: none;" onclick="return confirm('¿Está seguro de eliminar este producto?');">Eliminar</a>
                    </td>
                </tr>
                """
            
            table_content = f"""
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
            """
        else:
            table_content = """
            <div class="empty-state">
                <div style="font-size: 4rem; margin-bottom: 20px;">📦</div>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nuevo Producto</span>
                <a href="/productos/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/productos/crear/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Código *</label>
                        <input type="text" name="codigo" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                        <input type="text" name="nombre" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Categoría *</label>
                        <select name="categoria_id" required 
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="">Seleccione una categoría</option>
                            {category_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Precio Compra *</label>
                        <input type="number" name="precio_compra" step="0.01" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Precio Venta *</label>
                        <input type="number" name="precio_venta" step="0.01" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Stock Actual</label>
                        <input type="number" name="stock_actual" value="0" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Stock Mínimo</label>
                        <input type="number" name="stock_minimo" value="10" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Descripción</label>
                    <textarea name="descripcion" rows="4" 
                              style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;"></textarea>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Guardar Producto</button>
                    <a href="/productos/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Producto</span>
                <a href="/productos/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/productos/{product['id']}/editar/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Código *</label>
                        <input type="text" name="codigo" value="{product['codigo']}" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre *</label>
                        <input type="text" name="nombre" value="{product['nombre']}" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Categoría *</label>
                        <select name="categoria_id" required 
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="">Seleccione una categoría</option>
                            {category_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Precio Compra *</label>
                        <input type="number" name="precio_compra" value="{product['precio_compra']}" step="0.01" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Precio Venta *</label>
                        <input type="number" name="precio_venta" value="{product['precio_venta']}" step="0.01" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Stock Actual</label>
                        <input type="number" name="stock_actual" value="{product['stock_actual']}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Stock Mínimo</label>
                        <input type="number" name="stock_minimo" value="{product.get('stock_minimo', 10)}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                </div>
                
                <div style="margin-top: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Descripción</label>
                    <textarea name="descripcion" rows="4" 
                              style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">{product.get('descripcion', '')}</textarea>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Actualizar Producto</button>
                    <a href="/productos/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Producto', user, 'productos', content))

