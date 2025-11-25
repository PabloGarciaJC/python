from app.models.user import User
from app.models.category import Category
from app.views.category_view import CategoryView
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from app.middleware.auth_middleware import AuthMiddleware

class CategoryController:
    @staticmethod
    def index(request):
        """Muestra el listado de categorías"""
        # Verificar si el usuario está autenticado
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')
        
        # Obtener el usuario
        user = User.get_by_id(user_id)
        if not user:
            return redirect('/login/')
        
        # Obtener todas las categorías
        categories = Category.get_all()
        
        # Renderizar la vista
        return CategoryView.index(user, categories)
    
    @staticmethod
    @ensure_csrf_cookie
    @AuthMiddleware.require_active_user
    def create(request):
        """Crear una nueva categoría"""
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
            return HttpResponse(CategoryView.create(user, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                data = {
                    'nombre': request.POST.get('nombre'),
                    'descripcion': request.POST.get('descripcion'),
                    'activo': 1
                }
                
                # Validaciones básicas
                if not data['nombre']:
                    return HttpResponse(CategoryView.create(user, request, error='El nombre es obligatorio'))
                
                # Crear la categoría
                Category.create(data)
                
                # Redireccionar a la lista
                return HttpResponseRedirect('/categorias/')
                
            except Exception as e:
                return HttpResponse(CategoryView.create(user, request, error=f'Error al crear categoría: {str(e)}'))
    
    @staticmethod
    @ensure_csrf_cookie
    @AuthMiddleware.require_active_user
    def edit(request, category_id):
        """Editar una categoría existente"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Obtener la categoría
        category = Category.get_by_id(category_id)
        if not category:
            return HttpResponseRedirect('/categorias/')
        
        # Si es GET, mostrar formulario
        if request.method == 'GET':
            return HttpResponse(CategoryView.edit(user, category, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                data = {
                    'nombre': request.POST.get('nombre'),
                    'descripcion': request.POST.get('descripcion'),
                    'activo': 1
                }
                
                # Validaciones básicas
                if not data['nombre']:
                    return HttpResponse(CategoryView.edit(user, category, request, error='El nombre es obligatorio'))
                
                # Actualizar la categoría
                Category.update(category_id, data)
                
                # Redireccionar a la lista
                return HttpResponseRedirect('/categorias/')
                
            except Exception as e:
                return HttpResponse(CategoryView.edit(user, category, request, error=f'Error al actualizar categoría: {str(e)}'))
    
    @staticmethod
    @AuthMiddleware.require_active_user
    def delete(request, category_id):
        """Eliminar una categoría"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Eliminar la categoría (soft delete)
        Category.delete(category_id)
        
        # Redireccionar a la lista
        return HttpResponseRedirect('/categorias/')

