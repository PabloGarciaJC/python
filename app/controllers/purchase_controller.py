from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from app.models.user import User
from app.models.purchase import Purchase
from app.models.supplier import Supplier
from app.models.product import Product
from app.views.purchase_view import PurchaseView
import json

class PurchaseController:
    @staticmethod
    def index(request):
        """Mostrar lista de compras"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        purchases = Purchase.get_all()
        from django.http import HttpResponse
        return HttpResponse(PurchaseView.index(user, purchases, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def create(request):
        """Crear una nueva compra"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                # Obtener datos de la compra
                numero_factura = request.POST.get('numero_factura', '')
                proveedor_id = request.POST.get('proveedor_id')
                fecha = request.POST.get('fecha')
                total = float(request.POST.get('total', 0))
                estado = request.POST.get('estado', 'pendiente')
                notas = request.POST.get('notas', '')
                
                # Obtener detalles de productos (JSON)
                details_json = request.POST.get('details', '[]')
                details = json.loads(details_json)
                
                if not proveedor_id or not fecha or not details:
                    raise ValueError("Faltan datos requeridos")
                
                # Crear la compra
                purchase_data = {
                    'numero_factura': numero_factura,
                    'proveedor_id': int(proveedor_id),
                    'usuario_id': request.session['user_id'],
                    'fecha': fecha,
                    'total': total,
                    'estado': estado,
                    'notas': notas
                }
                
                Purchase.create(purchase_data, details)
                return HttpResponseRedirect('/compras/')
                
            except Exception as e:
                suppliers = Supplier.get_all()
                products = Product.get_all()
                error_message = f"Error al crear la compra: {str(e)}"
                from django.http import HttpResponse
                return HttpResponse(PurchaseView.create(user, suppliers, products, request, error_message))
        
        # GET request
        suppliers = Supplier.get_all()
        products = Product.get_all()
        from django.http import HttpResponse
        return HttpResponse(PurchaseView.create(user, suppliers, products, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def edit(request, purchase_id):
        """Editar una compra existente"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        purchase = Purchase.get_by_id(purchase_id)
        if not purchase:
            return HttpResponseRedirect('/compras/')
        
        if request.method == 'POST':
            try:
                # Obtener datos de la compra
                numero_factura = request.POST.get('numero_factura', '')
                proveedor_id = request.POST.get('proveedor_id')
                fecha = request.POST.get('fecha')
                total = float(request.POST.get('total', 0))
                estado = request.POST.get('estado', 'pendiente')
                notas = request.POST.get('notas', '')
                
                # Obtener detalles de productos (JSON)
                details_json = request.POST.get('details', '[]')
                details = json.loads(details_json)
                
                if not proveedor_id or not fecha:
                    raise ValueError("Faltan datos requeridos")
                
                # Actualizar la compra
                purchase_data = {
                    'numero_factura': numero_factura,
                    'proveedor_id': int(proveedor_id),
                    'fecha': fecha,
                    'total': total,
                    'estado': estado,
                    'notas': notas
                }
                
                Purchase.update(purchase_id, purchase_data)
                
                # Actualizar detalles
                if details:
                    Purchase.update_details(purchase_id, details)
                
                return HttpResponseRedirect('/compras/')
                
            except Exception as e:
                suppliers = Supplier.get_all()
                products = Product.get_all()
                details = Purchase.get_details(purchase_id)
                error_message = f"Error al actualizar la compra: {str(e)}"
                from django.http import HttpResponse
                return HttpResponse(PurchaseView.edit(user, purchase, suppliers, products, details, request, error_message))
        
        # GET request
        suppliers = Supplier.get_all()
        products = Product.get_all()
        details = Purchase.get_details(purchase_id)
        from django.http import HttpResponse
        return HttpResponse(PurchaseView.edit(user, purchase, suppliers, products, details, request))
    
    @staticmethod
    def delete(request, purchase_id):
        """Eliminar una compra"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                Purchase.delete(purchase_id)
            except Exception as e:
                pass
        
        return HttpResponseRedirect('/compras/')
    
    @staticmethod
    def view(request, purchase_id):
        """Ver detalle de una compra"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        purchase = Purchase.get_by_id(purchase_id)
        if not purchase:
            return HttpResponseRedirect('/compras/')
        
        details = Purchase.get_details(purchase_id)
        from django.http import HttpResponse
        return HttpResponse(PurchaseView.view(user, purchase, details))
