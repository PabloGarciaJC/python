from config.database import Database

class Supplier:
    @staticmethod
    def get_all():
        """Obtener todos los proveedores activos"""
        query = "SELECT * FROM proveedores WHERE activo = 1 ORDER BY nombre"
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(supplier_id):
        """Obtener un proveedor por ID"""
        query = "SELECT * FROM proveedores WHERE id = %s AND activo = 1"
        result = Database.execute_query(query, (supplier_id,))
        return result[0] if result else None
    
    @staticmethod
    def count():
        """Contar total de proveedores activos"""
        query = "SELECT COUNT(*) as total FROM proveedores WHERE activo = 1"
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def create(data):
        """Crear un nuevo proveedor"""
        query = """
            INSERT INTO proveedores (nombre, ruc, telefono, email, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """
        return Database.execute_query(
            query,
            (
                data['nombre'],
                data.get('ruc', ''),
                data.get('telefono', ''),
                data.get('email', ''),
                data.get('direccion', '')
            ),
            fetch=False
        )
    
    @staticmethod
    def update(supplier_id, data):
        """Actualizar un proveedor"""
        query = """
            UPDATE proveedores
            SET nombre = %s,
                ruc = %s,
                telefono = %s,
                email = %s,
                direccion = %s
            WHERE id = %s
        """
        return Database.execute_query(
            query,
            (
                data['nombre'],
                data.get('ruc', ''),
                data.get('telefono', ''),
                data.get('email', ''),
                data.get('direccion', ''),
                supplier_id
            ),
            fetch=False
        )
    
    @staticmethod
    def delete(supplier_id):
        """Eliminar lógicamente un proveedor"""
        query = "UPDATE proveedores SET activo = 0 WHERE id = %s"
        return Database.execute_query(query, (supplier_id,), fetch=False)
