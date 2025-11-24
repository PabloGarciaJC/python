from config.database import Database

class Role:
    """Modelo de Rol"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los roles"""
        query = """
            SELECT id, nombre, descripcion, created_at
            FROM pablogarciajcbd.roles
            ORDER BY nombre
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(role_id):
        """Obtiene un rol por su ID"""
        query = """
            SELECT id, nombre, descripcion
            FROM pablogarciajcbd.roles
            WHERE id = %s
        """
        result = Database.execute_query(query, (role_id,))
        return result[0] if result else None
    
    @staticmethod
    def count():
        """Cuenta el total de roles"""
        query = "SELECT COUNT(*) as total FROM pablogarciajcbd.roles"
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def create(data):
        """Crea un nuevo rol"""
        query = """
            INSERT INTO pablogarciajcbd.roles (nombre, descripcion)
            VALUES (%s, %s)
        """
        params = (
            data['nombre'],
            data.get('descripcion', '')
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def update(role_id, data):
        """Actualiza un rol existente"""
        query = """
            UPDATE pablogarciajcbd.roles 
            SET nombre = %s,
                descripcion = %s
            WHERE id = %s
        """
        params = (
            data['nombre'],
            data.get('descripcion', ''),
            role_id
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def delete(role_id):
        """Elimina un rol (hard delete)"""
        query = "DELETE FROM pablogarciajcbd.roles WHERE id = %s"
        return Database.execute_query(query, (role_id,), fetch=False)
