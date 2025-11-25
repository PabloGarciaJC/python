import hashlib
from config.database import Database

class User:
    """Modelo de Usuario"""
    
    @staticmethod
    def authenticate(username, password):
        """Autentica un usuario por username o email"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = """
            SELECT u.*, r.nombre as rol
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.id
            WHERE (u.username = %s OR u.email = %s) AND u.password = %s
        """
        users = Database.execute_query(query, (username, username, password_hash))
        return users[0] if users else None
    
    @staticmethod
    def create(username, email, password, nombre_completo):
        """Crea un nuevo usuario"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = """
            INSERT INTO usuarios (username, email, password, nombre_completo, rol_id, activo)
            VALUES (%s, %s, %s, %s, %s, 1)
        """
        # Rol 2 = Cliente por defecto
        user_id = Database.execute_query(
            query, 
            (username, email, password_hash, nombre_completo, 2),
            fetch=False
        )
        return user_id
    
    @staticmethod
    def exists(username=None, email=None):
        """Verifica si un usuario o email ya existe"""
        if username:
            result = Database.execute_query(
                "SELECT COUNT(*) as count FROM usuarios WHERE username = %s",
                (username,)
            )
            return result[0]['count'] > 0
        
        if email:
            result = Database.execute_query(
                "SELECT COUNT(*) as count FROM usuarios WHERE email = %s",
                (email,)
            )
            return result[0]['count'] > 0
        
        return False
    
    @staticmethod
    def get_by_id(user_id):
        """Obtiene un usuario por ID"""
        query = """
            SELECT u.*, r.nombre as rol
            FROM usuarios u
            JOIN roles r ON u.rol_id = r.id
            WHERE u.id = %s
        """
        users = Database.execute_query(query, (user_id,))
        return users[0] if users else None
