from django.http import HttpResponse, HttpResponseRedirect
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.sale import Sale
from app.models.purchase import Purchase
from app.models.client import Client
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse
from app.models.inventory_movement import InventoryMovement
from app.views.dashboard_view import DashboardView

class DashboardController:
    """Controlador del Dashboard"""
    
    @staticmethod
    def index(request):
        """Muestra el dashboard"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        # Obtener datos del usuario
        user = User.get_by_id(user_id)
        
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Obtener estadísticas principales
        stats = {
            'total_productos': Product.count(),
            'total_categorias': Category.count(),
            'total_clientes': Client.count(),
            'total_proveedores': Supplier.count(),
            'total_almacenes': Warehouse.count(),
            'ventas_mes': Sale.total_ventas_mes(),
            'compras_mes': Purchase.total_compras_mes(),
            'total_ventas': Sale.count(),
            'total_compras': Purchase.count(),
            'total_movimientos': InventoryMovement.count()
        }
        
        # Obtener productos con stock bajo (menos de 10 unidades)
        productos_bajo_stock = Product.get_low_stock(limit=10)
        
        # Obtener últimas ventas
        ultimas_ventas = Sale.get_all(limit=5)
        
        # Obtener últimas compras
        ultimas_compras = Purchase.get_all(limit=5)
        
        # Renderizar dashboard
        return HttpResponse(DashboardView.index(
            user, 
            request.path, 
            stats, 
            productos_bajo_stock,
            ultimas_ventas,
            ultimas_compras
        ))
