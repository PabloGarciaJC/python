from config.database import Database

class Client:
    """Modelo de Cliente"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los clientes activos"""
        query = """
            SELECT id, nombre, documento, telefono, email, direccion
            FROM pablogarciajcbd.clientes
            WHERE activo = 1
            ORDER BY nombre
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(client_id):
        """Obtiene un cliente por su ID"""
        query = """
            SELECT id, nombre, documento, telefono, email, direccion
            FROM pablogarciajcbd.clientes
            WHERE id = %s AND activo = 1
        """
        result = Database.execute_query(query, (client_id,))
        return result[0] if result else None
