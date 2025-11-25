class Layout:
    """Layouts y componentes compartidos"""
    
    @staticmethod
    def get_styles():
        """Carga los estilos CSS desde archivo externo"""
        return '''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="stylesheet" href="/static/css/main.css">
        <link rel="stylesheet" href="/static/css/forms.css">
        <link rel="stylesheet" href="/static/css/dashboard.css">
        '''
    
    @staticmethod
    def navbar(user):
        """Componente de Navbar"""
        return f"""
        <div class="navbar">
            <div class="navbar-content">
                <h1>Sistema de Gestión de Inventario</h1>
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
            {'url': '/documentacion/', 'label': 'Documentación', 'key': 'documentacion'},
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
            <title>{title} - Sistema de Gestión de Inventario</title>
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
