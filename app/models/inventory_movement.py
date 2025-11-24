from config.database import Database

class InventoryMovement:
    @staticmethod
    def get_all():
        """Obtener todos los movimientos de inventario"""
        query = """
            SELECT mi.*, 
                   p.nombre as producto_nombre,
                   a.nombre as almacen_nombre,
                   u.username as usuario_nombre
            FROM movimientos_inventario mi
            INNER JOIN productos p ON mi.producto_id = p.id
            INNER JOIN almacenes a ON mi.almacen_id = a.id
            INNER JOIN usuarios u ON mi.usuario_id = u.id
            ORDER BY mi.fecha DESC, mi.id DESC
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(movement_id):
        """Obtener un movimiento por ID"""
        query = """
            SELECT mi.*, 
                   p.nombre as producto_nombre,
                   a.nombre as almacen_nombre,
                   u.username as usuario_nombre
            FROM movimientos_inventario mi
            INNER JOIN productos p ON mi.producto_id = p.id
            INNER JOIN almacenes a ON mi.almacen_id = a.id
            INNER JOIN usuarios u ON mi.usuario_id = u.id
            WHERE mi.id = %s
        """
        result = Database.execute_query(query, (movement_id,))
        return result[0] if result else None
    
    @staticmethod
    def count():
        """Contar total de movimientos"""
        query = "SELECT COUNT(*) as total FROM movimientos_inventario"
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def create(data):
        """Crear un nuevo movimiento de inventario"""
        query = """
            INSERT INTO movimientos_inventario 
            (producto_id, almacen_id, tipo_movimiento, cantidad, usuario_id, referencia, motivo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return Database.execute_query(
            query,
            (
                data['producto_id'],
                data['almacen_id'],
                data['tipo_movimiento'],
                data['cantidad'],
                data['usuario_id'],
                data.get('referencia', ''),
                data.get('motivo', '')
            ),
            fetch=False
        )
    
    @staticmethod
    def update(movement_id, data):
        """Actualizar un movimiento de inventario"""
        query = """
            UPDATE movimientos_inventario
            SET producto_id = %s,
                almacen_id = %s,
                tipo_movimiento = %s,
                cantidad = %s,
                referencia = %s,
                motivo = %s
            WHERE id = %s
        """
        return Database.execute_query(
            query,
            (
                data['producto_id'],
                data['almacen_id'],
                data['tipo_movimiento'],
                data['cantidad'],
                data.get('referencia', ''),
                data.get('motivo', ''),
                movement_id
            ),
            fetch=False
        )
    
    @staticmethod
    def delete(movement_id):
        """Eliminar un movimiento de inventario"""
        query = "DELETE FROM movimientos_inventario WHERE id = %s"
        return Database.execute_query(query, (movement_id,), fetch=False)
    
    @staticmethod
    def get_by_product(product_id):
        """Obtener movimientos por producto"""
        query = """
            SELECT mi.*, 
                   a.nombre as almacen_nombre,
                   u.username as usuario_nombre
            FROM movimientos_inventario mi
            INNER JOIN almacenes a ON mi.almacen_id = a.id
            INNER JOIN usuarios u ON mi.usuario_id = u.id
            WHERE mi.producto_id = %s
            ORDER BY mi.fecha DESC
        """
        return Database.execute_query(query, (product_id,))
    
    @staticmethod
    def get_by_warehouse(warehouse_id):
        """Obtener movimientos por almacén"""
        query = """
            SELECT mi.*, 
                   p.nombre as producto_nombre,
                   u.username as usuario_nombre
            FROM movimientos_inventario mi
            INNER JOIN productos p ON mi.producto_id = p.id
            INNER JOIN usuarios u ON mi.usuario_id = u.id
            WHERE mi.almacen_id = %s
            ORDER BY mi.fecha DESC
        """
        return Database.execute_query(query, (warehouse_id,))
