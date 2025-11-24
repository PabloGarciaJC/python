from config.database import Database

class Category:
    @staticmethod
    def get_all():
        """Obtiene todas las categorías"""
        query = """
            SELECT id, nombre, descripcion 
            FROM pablogarciajcbd.categorias 
            WHERE activo = 1
            ORDER BY nombre
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(category_id):
        """Obtiene una categoría por su ID"""
        query = """
            SELECT id, nombre, descripcion 
            FROM pablogarciajcbd.categorias 
            WHERE id = %s AND activo = 1
        """
        result = Database.execute_query(query, (category_id,))
        return result[0] if result else None
    
    @staticmethod
    def count():
        """Cuenta el total de categorías"""
        query = "SELECT COUNT(*) as total FROM pablogarciajcbd.categorias WHERE activo = 1"
        result = Database.execute_query(query)
        return result[0]['total'] if result else 0
    
    @staticmethod
    def create(data):
        """Crea una nueva categoría"""
        query = """
            INSERT INTO pablogarciajcbd.categorias (nombre, descripcion, activo)
            VALUES (%s, %s, %s)
        """
        params = (
            data['nombre'],
            data.get('descripcion', ''),
            data.get('activo', 1)
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def update(category_id, data):
        """Actualiza una categoría existente"""
        query = """
            UPDATE pablogarciajcbd.categorias 
            SET nombre = %s, 
                descripcion = %s, 
                activo = %s
            WHERE id = %s
        """
        params = (
            data['nombre'],
            data.get('descripcion', ''),
            data.get('activo', 1),
            category_id
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def delete(category_id):
        """Elimina una categoría (soft delete cambiando activo a 0)"""
        query = "UPDATE pablogarciajcbd.categorias SET activo = 0 WHERE id = %s"
        return Database.execute_query(query, (category_id,), fetch=False)

