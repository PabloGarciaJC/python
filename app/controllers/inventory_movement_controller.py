from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from app.models.user import User
from app.models.inventory_movement import InventoryMovement
from app.models.product import Product
from app.models.warehouse import Warehouse
from app.views.inventory_movement_view import InventoryMovementView

class InventoryMovementController:
    @staticmethod
    def index(request):
        """Mostrar lista de movimientos de inventario"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        movements = InventoryMovement.get_all()
        return HttpResponse(InventoryMovementView.index(user, movements, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def create(request):
        """Crear un nuevo movimiento de inventario"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                producto_id = request.POST.get('producto_id')
                almacen_id = request.POST.get('almacen_id')
                tipo_movimiento = request.POST.get('tipo_movimiento')
                cantidad = int(request.POST.get('cantidad', 0))
                referencia = request.POST.get('referencia', '').strip()
                motivo = request.POST.get('motivo', '').strip()
                
                if not producto_id or not almacen_id or not tipo_movimiento:
                    raise ValueError("El producto, almacén y tipo de movimiento son requeridos")
                
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
                
                data = {
                    'producto_id': producto_id,
                    'almacen_id': almacen_id,
                    'tipo_movimiento': tipo_movimiento,
                    'cantidad': cantidad,
                    'usuario_id': request.session['user_id'],
                    'referencia': referencia,
                    'motivo': motivo
                }
                
                InventoryMovement.create(data)
                return HttpResponseRedirect('/movimientos-inventario/')
                
            except Exception as e:
                products = Product.get_all()
                warehouses = Warehouse.get_all()
                error_message = f"Error al crear el movimiento: {str(e)}"
                return HttpResponse(InventoryMovementView.create(user, products, warehouses, request, error_message))
        
        # GET request
        products = Product.get_all()
        warehouses = Warehouse.get_all()
        return HttpResponse(InventoryMovementView.create(user, products, warehouses, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def edit(request, movement_id):
        """Editar un movimiento de inventario existente"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        movement = InventoryMovement.get_by_id(movement_id)
        if not movement:
            return HttpResponseRedirect('/movimientos-inventario/')
        
        if request.method == 'POST':
            try:
                producto_id = request.POST.get('producto_id')
                almacen_id = request.POST.get('almacen_id')
                tipo_movimiento = request.POST.get('tipo_movimiento')
                cantidad = int(request.POST.get('cantidad', 0))
                referencia = request.POST.get('referencia', '').strip()
                motivo = request.POST.get('motivo', '').strip()
                
                if not producto_id or not almacen_id or not tipo_movimiento:
                    raise ValueError("El producto, almacén y tipo de movimiento son requeridos")
                
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
                
                data = {
                    'producto_id': producto_id,
                    'almacen_id': almacen_id,
                    'tipo_movimiento': tipo_movimiento,
                    'cantidad': cantidad,
                    'referencia': referencia,
                    'motivo': motivo
                }
                
                InventoryMovement.update(movement_id, data)
                return HttpResponseRedirect('/movimientos-inventario/')
                
            except Exception as e:
                products = Product.get_all()
                warehouses = Warehouse.get_all()
                error_message = f"Error al actualizar el movimiento: {str(e)}"
                return HttpResponse(InventoryMovementView.edit(user, movement, products, warehouses, request, error_message))
        
        # GET request
        products = Product.get_all()
        warehouses = Warehouse.get_all()
        return HttpResponse(InventoryMovementView.edit(user, movement, products, warehouses, request))
    
    @staticmethod
    def delete(request, movement_id):
        """Eliminar un movimiento de inventario"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                InventoryMovement.delete(movement_id)
            except Exception as e:
                print(f"Error al eliminar movimiento: {str(e)}")
        
        return HttpResponseRedirect('/movimientos-inventario/')
    
    @staticmethod
    def view(request, movement_id):
        """Ver detalle de un movimiento específico"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        movement = InventoryMovement.get_by_id(movement_id)
        if not movement:
            return HttpResponseRedirect('/movimientos-inventario/')
        
        return HttpResponse(InventoryMovementView.view(user, movement))
