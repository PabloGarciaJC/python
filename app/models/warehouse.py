from config.database import Database

class Warehouse:
    """Modelo de Almacén"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los almacenes activos"""
        query = """
            SELECT id, nombre, ubicacion, capacidad
            FROM pablogarciajcbd.almacenes
            WHERE activo = 1
            ORDER BY nombre
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(warehouse_id):
        """Obtiene un almacén por su ID"""
        query = """
            SELECT id, nombre, ubicacion, capacidad
            FROM pablogarciajcbd.almacenes
            WHERE id = %s AND activo = 1
        """
        result = Database.execute_query(query, (warehouse_id,))
        return result[0] if result else None
    
    @staticmethod
    def count():
        """Cuenta el total de almacenes activos"""
        query = "SELECT COUNT(*) as total FROM pablogarciajcbd.almacenes WHERE activo = 1"
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def create(data):
        """Crea un nuevo almacén"""
        query = """
            INSERT INTO pablogarciajcbd.almacenes 
            (nombre, ubicacion, capacidad, activo)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            data['nombre'],
            data.get('ubicacion', ''),
            data.get('capacidad', 0),
            data.get('activo', 1)
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def update(warehouse_id, data):
        """Actualiza un almacén existente"""
        query = """
            UPDATE pablogarciajcbd.almacenes 
            SET nombre = %s,
                ubicacion = %s,
                capacidad = %s,
                activo = %s
            WHERE id = %s
        """
        params = (
            data['nombre'],
            data.get('ubicacion', ''),
            data.get('capacidad', 0),
            data.get('activo', 1),
            warehouse_id
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def delete(warehouse_id):
        """Elimina un almacén (soft delete cambiando activo a 0)"""
        query = "UPDATE pablogarciajcbd.almacenes SET activo = 0 WHERE id = %s"
        return Database.execute_query(query, (warehouse_id,), fetch=False)
