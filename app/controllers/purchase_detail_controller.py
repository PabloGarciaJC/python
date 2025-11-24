from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from app.models.user import User
from app.models.purchase import Purchase
from app.models.product import Product
from app.views.purchase_detail_view import PurchaseDetailView

class PurchaseDetailController:
    @staticmethod
    def index(request):
        """Mostrar lista de todos los detalles de compras"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        # Obtener todos los detalles de todas las compras
        query = """
            SELECT dc.*, 
                   p.nombre as producto_nombre,
                   c.numero_factura,
                   c.fecha as fecha_compra,
                   pr.nombre as proveedor_nombre
            FROM detalle_compras dc
            INNER JOIN productos p ON dc.producto_id = p.id
            INNER JOIN compras c ON dc.compra_id = c.id
            INNER JOIN proveedores pr ON c.proveedor_id = pr.id
            ORDER BY c.fecha DESC, dc.id DESC
        """
        from config.database import Database
        details = Database.execute_query(query)
        
        return HttpResponse(PurchaseDetailView.index(user, details, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def create(request):
        """Crear un nuevo detalle de compra"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                compra_id = request.POST.get('compra_id')
                producto_id = request.POST.get('producto_id')
                cantidad = int(request.POST.get('cantidad', 0))
                precio_unitario = float(request.POST.get('precio_unitario', 0))
                
                if not compra_id or not producto_id:
                    raise ValueError("La compra y el producto son requeridos")
                
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
                
                if precio_unitario < 0:
                    raise ValueError("El precio unitario no puede ser negativo")
                
                subtotal = cantidad * precio_unitario
                
                # Insertar el detalle
                query = """
                    INSERT INTO detalle_compras (compra_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                from config.database import Database
                Database.execute_query(query, (compra_id, producto_id, cantidad, precio_unitario, subtotal), fetch=False)
                
                # Actualizar el total de la compra
                update_query = """
                    UPDATE compras 
                    SET total = (
                        SELECT SUM(subtotal) 
                        FROM detalle_compras 
                        WHERE compra_id = %s
                    )
                    WHERE id = %s
                """
                Database.execute_query(update_query, (compra_id, compra_id), fetch=False)
                
                return HttpResponseRedirect('/detalle-compras/')
                
            except Exception as e:
                purchases = Purchase.get_all()
                products = Product.get_all()
                error_message = f"Error al crear el detalle: {str(e)}"
                return HttpResponse(PurchaseDetailView.create(user, purchases, products, request, error_message))
        
        # GET request
        purchases = Purchase.get_all()
        products = Product.get_all()
        return HttpResponse(PurchaseDetailView.create(user, purchases, products, request))
    
    @staticmethod
    @ensure_csrf_cookie
    def edit(request, detail_id):
        """Editar un detalle de compra existente"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        # Obtener el detalle
        query = """
            SELECT dc.*, c.numero_factura, p.nombre as producto_nombre
            FROM detalle_compras dc
            INNER JOIN compras c ON dc.compra_id = c.id
            INNER JOIN productos p ON dc.producto_id = p.id
            WHERE dc.id = %s
        """
        from config.database import Database
        result = Database.execute_query(query, (detail_id,))
        
        if not result:
            return HttpResponseRedirect('/detalle-compras/')
        
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
                    UPDATE detalle_compras
                    SET cantidad = %s,
                        precio_unitario = %s,
                        subtotal = %s
                    WHERE id = %s
                """
                Database.execute_query(update_query, (cantidad, precio_unitario, subtotal, detail_id), fetch=False)
                
                # Actualizar el total de la compra
                update_total_query = """
                    UPDATE compras 
                    SET total = (
                        SELECT SUM(subtotal) 
                        FROM detalle_compras 
                        WHERE compra_id = %s
                    )
                    WHERE id = %s
                """
                Database.execute_query(update_total_query, (detail['compra_id'], detail['compra_id']), fetch=False)
                
                return HttpResponseRedirect('/detalle-compras/')
                
            except Exception as e:
                products = Product.get_all()
                error_message = f"Error al actualizar el detalle: {str(e)}"
                return HttpResponse(PurchaseDetailView.edit(user, detail, products, request, error_message))
        
        # GET request
        products = Product.get_all()
        return HttpResponse(PurchaseDetailView.edit(user, detail, products, request))
    
    @staticmethod
    def delete(request, detail_id):
        """Eliminar un detalle de compra"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        if request.method == 'POST':
            try:
                # Obtener la compra_id antes de eliminar
                query = "SELECT compra_id FROM detalle_compras WHERE id = %s"
                from config.database import Database
                result = Database.execute_query(query, (detail_id,))
                
                if result:
                    compra_id = result[0]['compra_id']
                    
                    # Eliminar el detalle
                    delete_query = "DELETE FROM detalle_compras WHERE id = %s"
                    Database.execute_query(delete_query, (detail_id,), fetch=False)
                    
                    # Actualizar el total de la compra
                    update_query = """
                        UPDATE compras 
                        SET total = COALESCE((
                            SELECT SUM(subtotal) 
                            FROM detalle_compras 
                            WHERE compra_id = %s
                        ), 0)
                        WHERE id = %s
                    """
                    Database.execute_query(update_query, (compra_id, compra_id), fetch=False)
                
            except Exception as e:
                print(f"Error al eliminar detalle: {str(e)}")
        
        return HttpResponseRedirect('/detalle-compras/')
    
    @staticmethod
    def view(request, detail_id):
        """Ver detalle de una compra específica"""
        if 'user_id' not in request.session:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(request.session['user_id'])
        if not user:
            return HttpResponseRedirect('/login/')
        
        # Obtener el detalle con toda la información
        query = """
            SELECT dc.*, 
                   p.nombre as producto_nombre,
                   p.precio as producto_precio,
                   c.numero_factura,
                   c.fecha as fecha_compra,
                   c.total as compra_total,
                   c.estado as compra_estado,
                   pr.nombre as proveedor_nombre
            FROM detalle_compras dc
            INNER JOIN productos p ON dc.producto_id = p.id
            INNER JOIN compras c ON dc.compra_id = c.id
            INNER JOIN proveedores pr ON c.proveedor_id = pr.id
            WHERE dc.id = %s
        """
        from config.database import Database
        result = Database.execute_query(query, (detail_id,))
        
        if not result:
            return HttpResponseRedirect('/detalle-compras/')
        
        detail = result[0]
        return HttpResponse(PurchaseDetailView.view(user, detail))
