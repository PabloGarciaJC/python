from config.database import Database

class Product:
    """Modelo de Producto"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los productos activos"""
        query = """
            SELECT p.*, c.nombre as categoria
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.activo = 1
            ORDER BY p.id DESC
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_by_id(product_id):
        """Obtiene un producto por ID"""
        query = """
            SELECT p.*, c.nombre as categoria
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = %s
        """
        products = Database.execute_query(query, (product_id,))
        return products[0] if products else None
    
    @staticmethod
    def count():
        """Cuenta el total de productos"""
        result = Database.execute_query("SELECT COUNT(*) as count FROM productos")
        return result[0]['count'] if result else 0
    
    @staticmethod
    def create(data):
        """Crea un nuevo producto"""
        query = """
            INSERT INTO pablogarciajcbd.productos 
            (codigo, nombre, descripcion, categoria_id, precio_compra, precio_venta, 
             stock_minimo, stock_actual, proveedor_id, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data['codigo'],
            data['nombre'],
            data.get('descripcion', ''),
            data['categoria_id'],
            data['precio_compra'],
            data['precio_venta'],
            data.get('stock_minimo', 10),
            data.get('stock_actual', 0),
            data.get('proveedor_id', None),
            data.get('activo', 1)
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def update(product_id, data):
        """Actualiza un producto existente"""
        query = """
            UPDATE pablogarciajcbd.productos 
            SET codigo = %s, 
                nombre = %s, 
                descripcion = %s, 
                categoria_id = %s, 
                precio_compra = %s, 
                precio_venta = %s,
                stock_minimo = %s, 
                stock_actual = %s, 
                proveedor_id = %s, 
                activo = %s
            WHERE id = %s
        """
        params = (
            data['codigo'],
            data['nombre'],
            data.get('descripcion', ''),
            data['categoria_id'],
            data['precio_compra'],
            data['precio_venta'],
            data.get('stock_minimo', 10),
            data.get('stock_actual', 0),
            data.get('proveedor_id', None),
            data.get('activo', 1),
            product_id
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def delete(product_id):
        """Elimina un producto (soft delete cambiando activo a 0)"""
        query = "UPDATE pablogarciajcbd.productos SET activo = 0 WHERE id = %s"
        return Database.execute_query(query, (product_id,), fetch=False)
    
    @staticmethod
    def get_low_stock(limit=10):
        """Obtiene productos con stock bajo"""
        query = """
            SELECT p.id, p.nombre, p.stock_actual, c.nombre as categoria
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.stock_actual < 10 AND p.activo = 1
            ORDER BY p.stock_actual ASC
            LIMIT %s
        """
        return Database.execute_query(query, (limit,), fetch=True)
