from app.models.user import User
from app.models.sale import Sale
from app.models.client import Client
from app.models.product import Product
from app.views.sale_view import SaleView
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from datetime import date

class SaleController:
    @staticmethod
    def index(request):
        """Muestra el listado de ventas"""
        # Verificar si el usuario está autenticado
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')
        
        # Obtener el usuario
        user = User.get_by_id(user_id)
        if not user:
            return redirect('/login/')
        
        # Obtener todas las ventas
        sales = Sale.get_all()
        
        # Renderizar la vista
        return HttpResponse(SaleView.index(user, sales))
    
    @staticmethod
    @ensure_csrf_cookie
    def create(request):
        """Crear una nueva venta"""
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
            clients = Client.get_all()
            products = Product.get_all()
            return HttpResponse(SaleView.create(user, clients, products, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                details_json = request.POST.get('details', '[]')
                details = json.loads(details_json)
                
                if not details:
                    clients = Client.get_all()
                    products = Product.get_all()
                    return HttpResponse(SaleView.create(user, clients, products, request, error='Debe agregar al menos un producto'))
                
                # Calcular total
                total = sum(float(d['subtotal']) for d in details)
                
                # Generar número de factura
                from datetime import datetime
                numero_factura = f"F-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                data = {
                    'numero_factura': numero_factura,
                    'cliente_id': request.POST.get('cliente_id'),
                    'usuario_id': user_id,
                    'fecha': request.POST.get('fecha', str(date.today())),
                    'total': total,
                    'estado': request.POST.get('estado', 'completada'),
                    'tipo_pago': request.POST.get('tipo_pago', 'efectivo'),
                    'notas': request.POST.get('notas', '')
                }
                
                # Validaciones
                if not data['cliente_id']:
                    clients = Client.get_all()
                    products = Product.get_all()
                    return HttpResponse(SaleView.create(user, clients, products, request, error='Debe seleccionar un cliente'))
                
                # Crear la venta
                Sale.create(data, details)
                
                # Redireccionar a la lista
                return HttpResponseRedirect('/ventas/')
                
            except Exception as e:
                clients = Client.get_all()
                products = Product.get_all()
                return HttpResponse(SaleView.create(user, clients, products, request, error=f'Error al crear venta: {str(e)}'))
    
    @staticmethod
    @ensure_csrf_cookie
    def edit(request, sale_id):
        """Editar una venta existente"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Obtener la venta
        sale = Sale.get_by_id(sale_id)
        if not sale:
            return HttpResponseRedirect('/ventas/')
        
        # Obtener detalles de la venta
        details = Sale.get_details(sale_id)
        
        # Si es GET, mostrar formulario
        if request.method == 'GET':
            clients = Client.get_all()
            products = Product.get_all()
            return HttpResponse(SaleView.edit(user, sale, details, clients, products, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                # Obtener datos del formulario
                details_json = request.POST.get('details', '[]')
                new_details = json.loads(details_json)
                
                if not new_details:
                    clients = Client.get_all()
                    products = Product.get_all()
                    return HttpResponse(SaleView.edit(user, sale, details, clients, products, request, error='Debe agregar al menos un producto'))
                
                # Calcular total
                total = sum(float(d['subtotal']) for d in new_details)
                
                data = {
                    'numero_factura': request.POST.get('numero_factura'),
                    'cliente_id': request.POST.get('cliente_id'),
                    'fecha': request.POST.get('fecha'),
                    'total': total,
                    'estado': request.POST.get('estado', 'completada'),
                    'tipo_pago': request.POST.get('tipo_pago', 'efectivo'),
                    'notas': request.POST.get('notas', '')
                }
                
                # Validaciones
                if not data['cliente_id']:
                    clients = Client.get_all()
                    products = Product.get_all()
                    return HttpResponse(SaleView.edit(user, sale, details, clients, products, request, error='Debe seleccionar un cliente'))
                
                # Actualizar la venta
                Sale.update(sale_id, data, new_details)
                
                # Redireccionar a la lista
                return HttpResponseRedirect('/ventas/')
                
            except Exception as e:
                clients = Client.get_all()
                products = Product.get_all()
                return HttpResponse(SaleView.edit(user, sale, details, clients, products, request, error=f'Error al actualizar venta: {str(e)}'))
    
    @staticmethod
    def delete(request, sale_id):
        """Eliminar una venta"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Eliminar la venta
        Sale.delete(sale_id)
        
        # Redireccionar a la lista
        return HttpResponseRedirect('/ventas/')
    
    @staticmethod
    def view(request, sale_id):
        """Ver detalle de una venta"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Obtener la venta
        sale = Sale.get_by_id(sale_id)
        if not sale:
            return HttpResponseRedirect('/ventas/')
        
        # Obtener detalles de la venta
        details = Sale.get_details(sale_id)
        
        return HttpResponse(SaleView.view(user, sale, details))

