class AuthView:
    """Vista de Autenticación"""
    
    @staticmethod
    def login(error=None, csrf_token=''):
        """Vista de login"""
        error_html = f'<div class="alert alert-error">{error}</div>' if error else ''
        
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión - Sistema de Inventario</title>
    <link rel="stylesheet" href="/static/css/auth.css">
</head>
<body>
<!-- Spinner -->
<div id="spinner" class="spinner"></div>

<div class="auth-container">
    <div class="auth-card">
            <!-- Usuarios de Prueba -->
        <div class="test-users-section">
            <h3 class="test-users-title">⚡ Acceso Rápido</h3>
            <p class="test-users-subtitle">Usuarios ficticios para realizar pruebas</p>
            <div class="test-users-grid">
                <div class="user-card" data-username="admin" data-password="admin123">
                    <div class="user-card-role">Administrador</div>
                    <div class="user-card-username">admin</div>
                    <a href="#" class="user-card-action select-user">Seleccionar aquí</a>
                </div>
                <div class="user-card" data-username="jperez" data-password="vendedor123">
                    <div class="user-card-role">Vendedor</div>
                    <div class="user-card-username">jperez</div>
                    <a href="#" class="user-card-action select-user">Seleccionar aquí</a>
                </div>
                <div class="user-card" data-username="mgonzalez" data-password="almacen123">
                    <div class="user-card-role">Almacenero</div>
                    <div class="user-card-username">mgonzalez</div>
                    <a href="#" class="user-card-action select-user">Seleccionar aquí</a>
                </div>
            </div>
        </div>
        <h2>🔐 Iniciar Sesión</h2>
        <p>Bienvenido al Sistema de Inventario</p>
        {error_html}
        <form method="POST" id="login-form">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <div class="form-group">
                <label>Usuario</label>
                <input type="text" name="username" id="username-input" class="form-control" required autofocus>
            </div>
            <div class="form-group">
                <label>Contraseña</label>
                <input type="password" name="password" id="password-input" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Iniciar Sesión</button>
        </form>
        

        
        <div class="auth-footer">
            <p>¿No tienes cuenta? <a href="/register/">Regístrate aquí</a></p>
        </div>
    </div>
</div>

<script src="/static/js/auth.js"></script>
</body>
</html>
"""
    
    @staticmethod
    def register(errors=None, csrf_token='', form_data=None):
        """Vista de registro"""
        form_data = form_data or {}
        errors_html = ''
        
        if errors:
            errors_list = ''.join([f'<li>{error}</li>' for error in errors])
            errors_html = f'<div class="alert alert-error"><ul>{errors_list}</ul></div>'
        
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro - Sistema de Inventario</title>
    <link rel="stylesheet" href="/static/css/auth.css">
</head>
<body>
<div class="auth-container">
    <div class="auth-card">
        <h2>📝 Crear Cuenta</h2>
        <p>Regístrate para acceder al sistema</p>
        {errors_html}
        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <div class="form-group">
                <label>Nombre Completo</label>
                <input type="text" name="nombre_completo" class="form-control" value="{form_data.get('nombre_completo', '')}" required autofocus>
            </div>
            <div class="form-group">
                <label>Usuario</label>
                <input type="text" name="username" class="form-control" value="{form_data.get('username', '')}" required>
            </div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" name="email" class="form-control" value="{form_data.get('email', '')}" required>
            </div>
            <div class="form-group">
                <label>Contraseña</label>
                <input type="password" name="password" class="form-control" required>
                <small style="color: #666; font-size: 12px;">Mínimo 6 caracteres</small>
            </div>
            <div class="form-group">
                <label>Confirmar Contraseña</label>
                <input type="password" name="password_confirm" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Crear Cuenta</button>
        </form>
        <div class="auth-footer">
            <p>¿Ya tienes cuenta? <a href="/login/">Inicia sesión aquí</a></p>
        </div>
    </div>
</div>
</body>
</html>
"""
