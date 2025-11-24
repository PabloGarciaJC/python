from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from app.models.user import User
from app.models.sale import Sale
from app.models.product import Product
from app.views.sale_detail_view import SaleDetailView

class SaleDetailController:
    @staticmethod
    def index(request):
        """Mostrar lista de todos los detalles de ventas"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        # Obtener todos los detalles de todas las ventas
        query = """
            SELECT dv.*, 
                   p.nombre as producto_nombre,
                   v.numero_factura,
                   v.fecha as fecha_venta,
                   c.nombre as cliente_nombre
            FROM detalle_ventas dv
            INNER JOIN productos p ON dv.producto_id = p.id
            INNER JOIN ventas v ON dv.venta_id = v.id
            INNER JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.fecha DESC, dv.id DESC
        """
        from config.database import Database
        details = Database.execute_query(query)
        
        return HttpResponse(SaleDetailView.index(user, details, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def create(request):
        """Crear un nuevo detalle de venta"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                venta_id = request.POST.get('venta_id')
                producto_id = request.POST.get('producto_id')
                cantidad = int(request.POST.get('cantidad', 0))
                precio_unitario = float(request.POST.get('precio_unitario', 0))
                
                if not venta_id or not producto_id:
                    raise ValueError("La venta y el producto son requeridos")
                
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
                
                if precio_unitario < 0:
                    raise ValueError("El precio unitario no puede ser negativo")
                
                subtotal = cantidad * precio_unitario
                
                # Insertar el detalle
                query = """
                    INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                from config.database import Database
                Database.execute_query(query, (venta_id, producto_id, cantidad, precio_unitario, subtotal), fetch=False)
                
                # Actualizar el total de la venta
                update_query = """
                    UPDATE ventas 
                    SET total = (
                        SELECT SUM(subtotal) 
                        FROM detalle_ventas 
                        WHERE venta_id = %s
                    )
                    WHERE id = %s
                """
                Database.execute_query(update_query, (venta_id, venta_id), fetch=False)
                
                return HttpResponseRedirect('/detalle-ventas/')
                
            except Exception as e:
                sales = Sale.get_all()
                products = Product.get_all()
                error_message = f"Error al crear el detalle: {str(e)}"
                return HttpResponse(SaleDetailView.create(user, sales, products, request, error_message))
        
        # GET request
        sales = Sale.get_all()
        products = Product.get_all()
        return HttpResponse(SaleDetailView.create(user, sales, products, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def edit(request, detail_id):
        """Editar un detalle de venta existente"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        # Obtener el detalle
        query = """
            SELECT dv.*, v.numero_factura, p.nombre as producto_nombre
            FROM detalle_ventas dv
            INNER JOIN ventas v ON dv.venta_id = v.id
            INNER JOIN productos p ON dv.producto_id = p.id
            WHERE dv.id = %s
        """
        from config.database import Database
        result = Database.execute_query(query, (detail_id,))
        
        if not result:
            return HttpResponseRedirect('/detalle-ventas/')
        
        detail = result[0]
        
        if request.method == 'POST':
            try:
                cantidad = int(request.POST.get('cantidad', 0))
                precio_unitario = float(request.POST.get('precio_unitario', 0))
                
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
                
                if precio_unitario < 0:
                    raise ValueError("El precio unitario no puede ser negativo")
                
                subtotal = cantidad * precio_unitario
                
                # Actualizar el detalle
                update_query = """
                    UPDATE detalle_ventas
                    SET cantidad = %s,
                        precio_unitario = %s,
                        subtotal = %s
                    WHERE id = %s
                """
                Database.execute_query(update_query, (cantidad, precio_unitario, subtotal, detail_id), fetch=False)
                
                # Actualizar el total de la venta
                update_total_query = """
                    UPDATE ventas 
                    SET total = (
                        SELECT SUM(subtotal) 
                        FROM detalle_ventas 
                        WHERE venta_id = %s
                    )
                    WHERE id = %s
                """
                Database.execute_query(update_total_query, (detail['venta_id'], detail['venta_id']), fetch=False)
                
                return HttpResponseRedirect('/detalle-ventas/')
                
            except Exception as e:
                products = Product.get_all()
                error_message = f"Error al actualizar el detalle: {str(e)}"
                return HttpResponse(SaleDetailView.edit(user, detail, products, request, error_message))
        
        # GET request
        products = Product.get_all()
        return HttpResponse(SaleDetailView.edit(user, detail, products, request))
    
    @staticmethod
    def delete(request, detail_id):
        """Eliminar un detalle de venta"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                # Obtener la venta_id antes de eliminar
                query = "SELECT venta_id FROM detalle_ventas WHERE id = %s"
                from config.database import Database
                result = Database.execute_query(query, (detail_id,))
                
                if result:
                    venta_id = result[0]['venta_id']
                    
                    # Eliminar el detalle
                    delete_query = "DELETE FROM detalle_ventas WHERE id = %s"
                    Database.execute_query(delete_query, (detail_id,), fetch=False)
                    
                    # Actualizar el total de la venta
                    update_query = """
                        UPDATE ventas 
                        SET total = COALESCE((
                            SELECT SUM(subtotal) 
                            FROM detalle_ventas 
                            WHERE venta_id = %s
                        ), 0)
                        WHERE id = %s
                    """
                    Database.execute_query(update_query, (venta_id, venta_id), fetch=False)
                
            except Exception as e:
                print(f"Error al eliminar detalle: {str(e)}")
        
        return HttpResponseRedirect('/detalle-ventas/')
    
    @staticmethod
    def view(request, detail_id):
        """Ver detalle de una venta específica"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        # Obtener el detalle con toda la información
        query = """
            SELECT dv.*, 
                   p.nombre as producto_nombre,
                   p.precio_venta as producto_precio,
                   v.numero_factura,
                   v.fecha as fecha_venta,
                   v.total as venta_total,
                   v.estado as venta_estado,
                   v.tipo_pago,
                   c.nombre as cliente_nombre,
                   c.documento as cliente_documento
            FROM detalle_ventas dv
            INNER JOIN productos p ON dv.producto_id = p.id
            INNER JOIN ventas v ON dv.venta_id = v.id
            INNER JOIN clientes c ON v.cliente_id = c.id
            WHERE dv.id = %s
        """
        from config.database import Database
        result = Database.execute_query(query, (detail_id,))
        
        if not result:
            return HttpResponseRedirect('/detalle-ventas/')
        
        detail = result[0]
        return HttpResponse(SaleDetailView.view(user, detail))
