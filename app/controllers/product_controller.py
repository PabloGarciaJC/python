from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.views.product_view import ProductView

class ProductController:
    """Controlador de Productos"""
    
    @staticmethod
    def index(request):
        """Lista de productos"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Obtener productos
        products = Product.get_all()
        
        return HttpResponse(ProductView.index(user, request.path, products))
    
    @staticmethod
    @ensure_csrf_cookie
    def create(request):
        """Crear un nuevo producto"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Si es GET, mostrar formulario
        if request.method == 'GET':
            categories = Category.get_all()
            return HttpResponse(ProductView.create(user, categories, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                data = {
                    'codigo': request.POST.get('codigo'),
                    'nombre': request.POST.get('nombre'),
                    'descripcion': request.POST.get('descripcion'),
                    'categoria_id': request.POST.get('categoria_id'),
                    'precio_compra': request.POST.get('precio_compra'),
                    'precio_venta': request.POST.get('precio_venta'),
                    'stock_minimo': request.POST.get('stock_minimo', 10),
                    'stock_actual': request.POST.get('stock_actual', 0),
                    'activo': 1
                }
                
                # Validaciones básicas
                if not data['codigo'] or not data['nombre']:
                    categories = Category.get_all()
                    return HttpResponse(ProductView.create(user, categories, request, error='Código y nombre son obligatorios'))
                
                # Crear el producto
                Product.create(data)
                
                # Redireccionar a la lista
                return HttpResponseRedirect('/productos/')
                
            except Exception as e:
                categories = Category.get_all()
                return HttpResponse(ProductView.create(user, categories, request, error=f'Error al crear producto: {str(e)}'))
    
    @staticmethod
    @ensure_csrf_cookie
    def edit(request, product_id):
        """Editar un producto existente"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Obtener el producto
        product = Product.get_by_id(product_id)
        if not product:
            return HttpResponseRedirect('/productos/')
        
        # Si es GET, mostrar formulario
        if request.method == 'GET':
            categories = Category.get_all()
            return HttpResponse(ProductView.edit(user, product, categories, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                data = {
                    'codigo': request.POST.get('codigo'),
                    'nombre': request.POST.get('nombre'),
                    'descripcion': request.POST.get('descripcion'),
                    'categoria_id': request.POST.get('categoria_id'),
                    'precio_compra': request.POST.get('precio_compra'),
                    'precio_venta': request.POST.get('precio_venta'),
                    'stock_minimo': request.POST.get('stock_minimo', 10),
                    'stock_actual': request.POST.get('stock_actual', 0),
                    'activo': 1
                }
                
                # Validaciones básicas
                if not data['codigo'] or not data['nombre']:
                    categories = Category.get_all()
                    return HttpResponse(ProductView.edit(user, product, categories, request, error='Código y nombre son obligatorios'))
                
                # Actualizar el producto
                Product.update(product_id, data)
                
                # Redireccionar a la lista
                return HttpResponseRedirect('/productos/')
                
            except Exception as e:
                categories = Category.get_all()
                return HttpResponse(ProductView.edit(user, product, categories, request, error=f'Error al actualizar producto: {str(e)}'))
    
    @staticmethod
    def delete(request, product_id):
        """Eliminar un producto"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Eliminar el producto (soft delete)
        Product.delete(product_id)
        
        # Redireccionar a la lista
        return HttpResponseRedirect('/productos/')
