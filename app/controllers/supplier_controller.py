from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from app.models.user import User
from app.models.supplier import Supplier
from app.views.supplier_view import SupplierView
from app.middleware.auth_middleware import AuthMiddleware

class SupplierController:
    @staticmethod
    def index(request):
        """Mostrar lista de proveedores"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        suppliers = Supplier.get_all()
        total = Supplier.count()
        return HttpResponse(SupplierView.index(user, suppliers, total, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def create(request):
        """Crear un nuevo proveedor"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                nombre = request.POST.get('nombre', '').strip()
                ruc = request.POST.get('ruc', '').strip()
                telefono = request.POST.get('telefono', '').strip()
                email = request.POST.get('email', '').strip()
                direccion = request.POST.get('direccion', '').strip()
                
                if not nombre:
                    raise ValueError("El nombre es requerido")
                
                data = {
                    'nombre': nombre,
                    'ruc': ruc,
                    'telefono': telefono,
                    'email': email,
                    'direccion': direccion
                }
                
                Supplier.create(data)
                return HttpResponseRedirect('/proveedores/')
                
            except Exception as e:
                error_message = f"Error al crear el proveedor: {str(e)}"
                return HttpResponse(SupplierView.create(user, request, error_message))
        
        return HttpResponse(SupplierView.create(user, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def edit(request, supplier_id):
        """Editar un proveedor existente"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        supplier = Supplier.get_by_id(supplier_id)
        if not supplier:
            return HttpResponseRedirect('/proveedores/')
        
        if request.method == 'POST':
            try:
                nombre = request.POST.get('nombre', '').strip()
                ruc = request.POST.get('ruc', '').strip()
                telefono = request.POST.get('telefono', '').strip()
                email = request.POST.get('email', '').strip()
                direccion = request.POST.get('direccion', '').strip()
                
                if not nombre:
                    raise ValueError("El nombre es requerido")
                
                data = {
                    'nombre': nombre,
                    'ruc': ruc,
                    'telefono': telefono,
                    'email': email,
                    'direccion': direccion
                }
                
                Supplier.update(supplier_id, data)
                return HttpResponseRedirect('/proveedores/')
                
            except Exception as e:
                error_message = f"Error al actualizar el proveedor: {str(e)}"
                return HttpResponse(SupplierView.edit(user, supplier, request, error_message))
        
        return HttpResponse(SupplierView.edit(user, supplier, request))
    
    @staticmethod
    def delete(request, supplier_id):
        """Eliminar lógicamente un proveedor"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                Supplier.delete(supplier_id)
            except Exception as e:
                pass
        
        return HttpResponseRedirect('/proveedores/')
