class Layout:
    """Layouts y componentes compartidos"""
    
    @staticmethod
    def get_styles():
        """Estilos CSS globales"""
        return """
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
            
            /* Navbar */
            .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .navbar-content { display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto; }
            .navbar h1 { font-size: 1.5rem; }
            .navbar-menu { display: flex; gap: 20px; align-items: center; }
            .navbar-menu a { color: white; text-decoration: none; padding: 8px 15px; border-radius: 5px; transition: background 0.3s; }
            .navbar-menu a:hover { background: rgba(255,255,255,0.2); }
            
            /* Sidebar */
            .layout { display: flex; min-height: calc(100vh - 70px); }
            .sidebar { width: 250px; background: white; padding: 20px; box-shadow: 2px 0 5px rgba(0,0,0,0.05); }
            .sidebar-menu { list-style: none; }
            .sidebar-menu li { margin: 10px 0; }
            .sidebar-menu a { display: block; padding: 12px 15px; color: #333; text-decoration: none; border-radius: 8px; transition: all 0.3s; }
            .sidebar-menu a:hover, .sidebar-menu a.active { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            
            /* Main Content */
            .main-content { flex: 1; padding: 30px; }
            .card { background: white; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); }
            .card-header { font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #f0f0f0; display: flex; justify-content: space-between; align-items: center; }
            
            /* Stats Cards */
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
            .stat-card h3 { font-size: 0.9rem; opacity: 0.9; margin-bottom: 10px; }
            .stat-card .value { font-size: 2.5rem; font-weight: bold; }
            
            /* Table */
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 15px; text-align: left; border-bottom: 1px solid #f0f0f0; }
            th { background: #f8f9fa; font-weight: 600; color: #667eea; }
            tr:hover { background: #f8f9fa; }
            
            /* Buttons */
            .btn { display: inline-block; padding: 10px 20px; border-radius: 8px; text-decoration: none; cursor: pointer; border: none; font-size: 14px; transition: all 0.3s; font-weight: 500; }
            .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
            .btn-success { background: #10b981; color: white; padding: 8px 15px; font-size: 13px; }
            .btn-warning { background: #f59e0b; color: white; padding: 8px 15px; font-size: 13px; }
            .btn-danger { background: #ef4444; color: white; padding: 8px 15px; font-size: 13px; }
            
            /* Badge */
            .badge { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
            .badge-success { background: #d1fae5; color: #065f46; }
            .badge-warning { background: #fef3c7; color: #92400e; }
            
            /* Empty State */
            .empty-state { text-align: center; padding: 40px; color: #6b7280; }
        </style>
        """
    
    @staticmethod
    def navbar(user):
        """Componente de Navbar"""
        return f"""
        <div class="navbar">
            <div class="navbar-content">
                <h1>Sistema de Gestión</h1>
                <div class="navbar-menu">
                    <span>Hola, {user['username']}</span>
                    <a href="/logout/">Cerrar Sesión</a>
                </div>
            </div>
        </div>
        """
    
    @staticmethod
    def sidebar(active_page=''):
        """Componente de Sidebar"""
        menu_items = [
            {'url': '/', 'label': 'Dashboard', 'key': 'dashboard'},
            {'url': '/productos/', 'label': 'Productos', 'key': 'productos'},
            {'url': '/categorias/', 'label': 'Categorías', 'key': 'categorias'},
            {'url': '/clientes/', 'label': 'Clientes', 'key': 'clientes'},
            {'url': '/proveedores/', 'label': 'Proveedores', 'key': 'proveedores'},
            {'url': '/almacenes/', 'label': 'Almacenes', 'key': 'almacenes'},
            {'url': '/movimientos-inventario/', 'label': 'Movimientos Inventario', 'key': 'movimientos-inventario'},
            {'url': '/roles/', 'label': 'Roles', 'key': 'roles'},
            {'url': '/ventas/', 'label': 'Ventas', 'key': 'ventas'},
            {'url': '/detalle-ventas/', 'label': 'Detalle Ventas', 'key': 'detalle-ventas'},
            {'url': '/compras/', 'label': 'Compras', 'key': 'compras'},
            {'url': '/detalle-compras/', 'label': 'Detalle Compras', 'key': 'detalle-compras'},
            {'url': '/reportes/', 'label': 'Reportes', 'key': 'reportes'},
            {'url': '/configuracion/', 'label': 'Configuración', 'key': 'configuracion'},
        ]
        
        menu_html = ""
        for item in menu_items:
            active_class = 'class="active"' if item['key'] == active_page else ''
            menu_html += f'<li><a href="{item["url"]}" {active_class}>{item["label"]}</a></li>\n'
        
        return f"""
        <div class="sidebar">
            <ul class="sidebar-menu">
                {menu_html}
            </ul>
        </div>
        """
    
    @staticmethod
    def render(title, user, active_page, content):
        """Renderiza el layout completo"""
        styles = Layout.get_styles()
        navbar = Layout.navbar(user)
        sidebar = Layout.sidebar(active_page)
        
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} - Sistema de Gestión</title>
            {styles}
        </head>
        <body>
            {navbar}
            <div class="layout">
                {sidebar}
                <div class="main-content">
                    {content}
                </div>
            </div>
        </body>
        </html>
        """
