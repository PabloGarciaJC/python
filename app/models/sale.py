from config.database import Database

class Sale:
    """Modelo de Venta"""
    
    @staticmethod
    def get_all(limit=None):
        """Obtiene todas las ventas con información del cliente"""
        query = """
            SELECT 
                v.id,
                v.numero_factura,
                v.fecha,
                v.total,
                v.estado,
                v.tipo_pago,
                c.nombre as cliente_nombre,
                c.documento as cliente_documento,
                u.username as vendedor
            FROM pablogarciajcbd.ventas v
            INNER JOIN pablogarciajcbd.clientes c ON v.cliente_id = c.id
            INNER JOIN pablogarciajcbd.usuarios u ON v.usuario_id = u.id
            ORDER BY v.fecha DESC, v.id DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(sale_id):
        """Obtiene una venta por su ID"""
        query = """
            SELECT 
                v.*,
                c.nombre as cliente_nombre,
                c.documento as cliente_documento,
                c.telefono as cliente_telefono,
                u.username as vendedor
            FROM pablogarciajcbd.ventas v
            INNER JOIN pablogarciajcbd.clientes c ON v.cliente_id = c.id
            INNER JOIN pablogarciajcbd.usuarios u ON v.usuario_id = u.id
            WHERE v.id = %s
        """
        result = Database.execute_query(query, (sale_id,))
        return result[0] if result else None
    
    @staticmethod
    def count():
        """Cuenta el total de ventas"""
        query = "SELECT COUNT(*) as total FROM pablogarciajcbd.ventas"
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def total_ventas_mes():
        """Calcula el total de ventas del mes actual"""
        query = """
            SELECT COALESCE(SUM(total), 0) as total
            FROM pablogarciajcbd.ventas
            WHERE MONTH(fecha) = MONTH(CURRENT_DATE())
            AND YEAR(fecha) = YEAR(CURRENT_DATE())
            AND estado = 'completada'
        """
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def get_details(sale_id):
        """Obtiene los detalles de una venta"""
        query = """
            SELECT 
                dv.*,
                p.nombre as producto_nombre,
                p.codigo as producto_codigo
            FROM pablogarciajcbd.detalle_ventas dv
            INNER JOIN pablogarciajcbd.productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = %s
        """
        return Database.execute_query(query, (sale_id,))
    
    @staticmethod
    def create(data, details):
        """Crea una nueva venta con sus detalles"""
        # Insertar la venta
        query_venta = """
            INSERT INTO pablogarciajcbd.ventas 
            (numero_factura, cliente_id, usuario_id, fecha, total, estado, tipo_pago, notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params_venta = (
            data['numero_factura'],
            data['cliente_id'],
            data['usuario_id'],
            data['fecha'],
            data['total'],
            data.get('estado', 'completada'),
            data.get('tipo_pago', 'efectivo'),
            data.get('notas', '')
        )
        
        # Ejecutar y obtener el ID insertado (lastrowid)
        venta_id = Database.execute_query(query_venta, params_venta, fetch=False)
        
        # Insertar los detalles
        query_detalle = """
            INSERT INTO pablogarciajcbd.detalle_ventas 
            (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        for detail in details:
            params_detalle = (
                venta_id,
                detail['producto_id'],
                detail['cantidad'],
                detail['precio_unitario'],
                detail['subtotal']
            )
            Database.execute_query(query_detalle, params_detalle, fetch=False)
        
        return venta_id
    
    @staticmethod
    def update(sale_id, data, details):
        """Actualiza una venta existente"""
        # Actualizar la venta
        query_venta = """
            UPDATE pablogarciajcbd.ventas 
            SET numero_factura = %s,
                cliente_id = %s,
                fecha = %s,
                total = %s,
                estado = %s,
                tipo_pago = %s,
                notas = %s
            WHERE id = %s
        """
        params_venta = (
            data['numero_factura'],
            data['cliente_id'],
            data['fecha'],
            data['total'],
            data.get('estado', 'completada'),
            data.get('tipo_pago', 'efectivo'),
            data.get('notas', ''),
            sale_id
        )
        Database.execute_query(query_venta, params_venta, fetch=False)
        
        # Eliminar detalles anteriores
        query_delete = "DELETE FROM pablogarciajcbd.detalle_ventas WHERE venta_id = %s"
        Database.execute_query(query_delete, (sale_id,), fetch=False)
        
        # Insertar nuevos detalles
        query_detalle = """
            INSERT INTO pablogarciajcbd.detalle_ventas 
            (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        for detail in details:
            params_detalle = (
                sale_id,
                detail['producto_id'],
                detail['cantidad'],
                detail['precio_unitario'],
                detail['subtotal']
            )
            Database.execute_query(query_detalle, params_detalle, fetch=False)
        
        return True
    
    @staticmethod
    def delete(sale_id):
        """Elimina una venta y sus detalles"""
        # Eliminar detalles
        query_detalle = "DELETE FROM pablogarciajcbd.detalle_ventas WHERE venta_id = %s"
        Database.execute_query(query_detalle, (sale_id,), fetch=False)
        
        # Eliminar venta
        query_venta = "DELETE FROM pablogarciajcbd.ventas WHERE id = %s"
        return Database.execute_query(query_venta, (sale_id,), fetch=False)

