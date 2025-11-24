from config.database import Database

class Purchase:
    @staticmethod
    def get_all(limit=None):
        """Obtener todas las compras con información del proveedor y usuario"""
        query = """
            SELECT c.*, 
                   p.nombre as proveedor_nombre,
                   u.username as usuario_nombre
            FROM compras c
            INNER JOIN proveedores p ON c.proveedor_id = p.id
            INNER JOIN usuarios u ON c.usuario_id = u.id
            ORDER BY c.fecha DESC, c.id DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(purchase_id):
        """Obtener una compra por ID con información del proveedor y usuario"""
        query = """
            SELECT c.*, 
                   p.nombre as proveedor_nombre,
                   u.username as usuario_nombre
            FROM compras c
            INNER JOIN proveedores p ON c.proveedor_id = p.id
            INNER JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.id = %s
        """
        result = Database.execute_query(query, (purchase_id,))
        return result[0] if result else None
    
    @staticmethod
    def count():
        """Contar total de compras"""
        query = "SELECT COUNT(*) as total FROM compras"
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def create(data, details):
        """Crear una nueva compra con sus detalles"""
        # Insertar la compra
        query = """
            INSERT INTO compras (numero_factura, proveedor_id, usuario_id, fecha, total, estado, notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        purchase_id = Database.execute_query(
            query,
            (
                data['numero_factura'],
                data['proveedor_id'],
                data['usuario_id'],
                data['fecha'],
                data['total'],
                data.get('estado', 'pendiente'),
                data.get('notas', '')
            ),
            fetch=False
        )
        
        # Insertar los detalles de la compra
        if purchase_id and details:
            detail_query = """
                INSERT INTO detalle_compras (compra_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            for detail in details:
                Database.execute_query(
                    detail_query,
                    (
                        purchase_id,
                        detail['producto_id'],
                        detail['cantidad'],
                        detail['precio_unitario'],
                        detail['subtotal']
                    ),
                    fetch=False
                )
        
        return purchase_id
    
    @staticmethod
    def update(purchase_id, data):
        """Actualizar una compra"""
        query = """
            UPDATE compras
            SET numero_factura = %s,
                proveedor_id = %s,
                fecha = %s,
                total = %s,
                estado = %s,
                notas = %s
            WHERE id = %s
        """
        return Database.execute_query(
            query,
            (
                data['numero_factura'],
                data['proveedor_id'],
                data['fecha'],
                data['total'],
                data['estado'],
                data.get('notas', ''),
                purchase_id
            ),
            fetch=False
        )
    
    @staticmethod
    def delete(purchase_id):
        """Eliminar una compra y sus detalles"""
        # Primero eliminar los detalles
        detail_query = "DELETE FROM detalle_compras WHERE compra_id = %s"
        Database.execute_query(detail_query, (purchase_id,), fetch=False)
        
        # Luego eliminar la compra
        query = "DELETE FROM compras WHERE id = %s"
        return Database.execute_query(query, (purchase_id,), fetch=False)
    
    @staticmethod
    def get_details(purchase_id):
        """Obtener los detalles de una compra"""
        query = """
            SELECT dc.*, p.nombre as producto_nombre
            FROM detalle_compras dc
            INNER JOIN productos p ON dc.producto_id = p.id
            WHERE dc.compra_id = %s
            ORDER BY dc.id
        """
        return Database.execute_query(query, (purchase_id,))
    
    @staticmethod
    def update_details(purchase_id, details):
        """Actualizar los detalles de una compra"""
        # Eliminar detalles existentes
        delete_query = "DELETE FROM detalle_compras WHERE compra_id = %s"
        Database.execute_query(delete_query, (purchase_id,), fetch=False)
        
        # Insertar nuevos detalles
        if details:
            insert_query = """
                INSERT INTO detalle_compras (compra_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            for detail in details:
                Database.execute_query(
                    insert_query,
                    (
                        purchase_id,
                        detail['producto_id'],
                        detail['cantidad'],
                        detail['precio_unitario'],
                        detail['subtotal']
                    ),
                    fetch=False
                )
        return True
    
    @staticmethod
    def total_compras_mes():
        """Calcula el total de compras del mes actual"""
        query = """
            SELECT COALESCE(SUM(total), 0) as total
            FROM compras
            WHERE MONTH(fecha) = MONTH(CURRENT_DATE())
            AND YEAR(fecha) = YEAR(CURRENT_DATE())
        """
        result = Database.execute_query(query, fetch=True)
        return result[0]['total'] if result else 0
