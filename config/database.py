import os
import MySQLdb

class Database:
    """Gestión de conexiones a la base de datos"""
    
    @staticmethod
    def get_connection():
        """Obtiene una conexión a MySQL"""
        return MySQLdb.connect(
            host='mysql',
            user=os.getenv('MYSQL_USER', 'pablogarciajcuser'),
            password=os.getenv('MYSQL_PASSWORD', 'password'),
            database=os.getenv('DB_DATABASE', 'pablogarciajcbd'),
            charset='utf8mb4'
        )
    
    @staticmethod
    def execute_query(query, params=None, fetch=True):
        """Ejecuta una consulta SQL"""
        conn = Database.get_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
            return result
        finally:
            cursor.close()
            conn.close()
