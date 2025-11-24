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
    
    @staticmethod
    def count():
        """Cuenta el total de clientes activos"""
        query = "SELECT COUNT(*) as total FROM pablogarciajcbd.clientes WHERE activo = 1"
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def create(data):
        """Crea un nuevo cliente"""
        query = """
            INSERT INTO pablogarciajcbd.clientes 
            (nombre, documento, telefono, email, direccion, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data['nombre'],
            data.get('documento', ''),
            data.get('telefono', ''),
            data.get('email', ''),
            data.get('direccion', ''),
            data.get('activo', 1)
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def update(client_id, data):
        """Actualiza un cliente existente"""
        query = """
            UPDATE pablogarciajcbd.clientes 
            SET nombre = %s,
                documento = %s,
                telefono = %s,
                email = %s,
                direccion = %s,
                activo = %s
            WHERE id = %s
        """
        params = (
            data['nombre'],
            data.get('documento', ''),
            data.get('telefono', ''),
            data.get('email', ''),
            data.get('direccion', ''),
            data.get('activo', 1),
            client_id
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def delete(client_id):
        """Elimina un cliente (soft delete cambiando activo a 0)"""
        query = "UPDATE pablogarciajcbd.clientes SET activo = 0 WHERE id = %s"
        return Database.execute_query(query, (client_id,), fetch=False)

