from config.database import Database

class Report:
    """Modelo para generación de reportes y estadísticas"""
    
    @staticmethod
    def ventas_por_mes():
        """Obtiene las ventas totales por mes del año actual"""
        query = """
            SELECT 
                MONTH(fecha) as mes,
                MONTHNAME(fecha) as nombre_mes,
                COUNT(*) as total_ventas,
                SUM(total) as monto_total
            FROM pablogarciajcbd.ventas
            WHERE YEAR(fecha) = YEAR(CURRENT_DATE())
            AND estado = 'completada'
            GROUP BY MONTH(fecha), MONTHNAME(fecha)
            ORDER BY mes
        """
        return Database.execute_query(query)
    
    @staticmethod
    def productos_mas_vendidos(limit=10):
        """Obtiene los productos más vendidos"""
        query = """
            SELECT 
                p.nombre,
                SUM(dv.cantidad) as total_vendido,
                SUM(dv.subtotal) as ingresos_totales
            FROM pablogarciajcbd.detalle_ventas dv
            INNER JOIN pablogarciajcbd.productos p ON dv.producto_id = p.id
            INNER JOIN pablogarciajcbd.ventas v ON dv.venta_id = v.id
            WHERE v.estado = 'completada'
            GROUP BY p.id, p.nombre
            ORDER BY total_vendido DESC
            LIMIT %s
        """
        return Database.execute_query(query, (limit,))
    
    @staticmethod
    def ventas_por_estado():
        """Obtiene el resumen de ventas por estado"""
        query = """
            SELECT 
                estado,
                COUNT(*) as cantidad,
                SUM(total) as monto_total
            FROM pablogarciajcbd.ventas
            GROUP BY estado
        """
        return Database.execute_query(query)
    
    @staticmethod
    def clientes_frecuentes(limit=10):
        """Obtiene los clientes con más compras"""
        query = """
            SELECT 
                c.nombre,
                c.documento,
                COUNT(v.id) as total_compras,
                SUM(v.total) as monto_total
            FROM pablogarciajcbd.clientes c
            INNER JOIN pablogarciajcbd.ventas v ON c.id = v.cliente_id
            WHERE v.estado = 'completada'
            GROUP BY c.id, c.nombre, c.documento
            ORDER BY total_compras DESC
            LIMIT %s
        """
        return Database.execute_query(query, (limit,))
    
    @staticmethod
    def inventario_bajo_stock(minimo=10):
        """Obtiene productos con stock bajo"""
        query = """
            SELECT 
                p.nombre,
                p.stock_actual as stock,
                c.nombre as categoria
            FROM pablogarciajcbd.productos p
            LEFT JOIN pablogarciajcbd.categorias c ON p.categoria_id = c.id
            WHERE p.stock_actual <= %s
            ORDER BY p.stock_actual ASC
        """
        return Database.execute_query(query, (minimo,))
    
    @staticmethod
    def resumen_general():
        """Obtiene un resumen general del sistema"""
        query = """
            SELECT 
                (SELECT COUNT(*) FROM pablogarciajcbd.ventas WHERE estado = 'completada') as total_ventas_completadas,
                (SELECT COUNT(*) FROM pablogarciajcbd.productos) as total_productos,
                (SELECT COUNT(*) FROM pablogarciajcbd.clientes WHERE activo = 1) as total_clientes_activos,
                (SELECT COALESCE(SUM(total), 0) FROM pablogarciajcbd.ventas WHERE estado = 'completada') as ingresos_totales,
                (SELECT COALESCE(SUM(total), 0) FROM pablogarciajcbd.ventas 
                 WHERE estado = 'completada' 
                 AND MONTH(fecha) = MONTH(CURRENT_DATE())
                 AND YEAR(fecha) = YEAR(CURRENT_DATE())) as ingresos_mes_actual
        """
        result = Database.execute_query(query)
        return result[0] if result else {}
