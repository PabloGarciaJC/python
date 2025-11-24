class AuthView:
    """Vista de Autenticación"""
    
    @staticmethod
    def _get_styles():
        """Estilos CSS compartidos"""
        return """
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
            
            /* Login/Register Container */
            .auth-container { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .auth-card { background: white; padding: 40px; border-radius: 12px; width: 100%; max-width: 450px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
            .auth-card h2 { text-align: center; margin-bottom: 10px; color: #333; }
            .auth-card p { text-align: center; margin-bottom: 30px; color: #666; font-size: 14px; }
            
            /* Forms */
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 8px; font-weight: 500; color: #374151; }
            .form-control { width: 100%; padding: 12px; border: 1px solid #e5e7eb; border-radius: 8px; font-size: 14px; }
            .form-control:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1); }
            
            /* Buttons */
            .btn { display: inline-block; padding: 12px 20px; border-radius: 8px; text-decoration: none; cursor: pointer; border: none; font-size: 14px; transition: all 0.3s; font-weight: 500; }
            .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 100%; }
            .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); }
            .btn-secondary { background: #6b7280; color: white; width: 100%; margin-top: 10px; }
            .btn-secondary:hover { background: #4b5563; }
            
            /* Alerts */
            .alert { padding: 12px 15px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; }
            .alert-error { background: #fee2e2; color: #991b1b; border-left: 4px solid #dc2626; }
            .alert-error ul { margin: 5px 0 0 20px; }
            
            /* Links */
            .auth-footer { text-align: center; margin-top: 20px; }
            .auth-footer a { color: #667eea; text-decoration: none; font-weight: 500; }
            .auth-footer a:hover { text-decoration: underline; }
        </style>
        """
    
    @staticmethod
    def login(error=None, csrf_token=''):
        """Vista de login"""
        error_html = f'<div class="alert alert-error">{error}</div>' if error else ''
        styles = AuthView._get_styles()
        
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión - Sistema de Inventario</title>
    {styles}
</head>
<body>
<div class="auth-container">
    <div class="auth-card">
        <h2>🔐 Iniciar Sesión</h2>
        <p>Bienvenido al Sistema de Inventario</p>
        {error_html}
        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <div class="form-group">
                <label>Usuario</label>
                <input type="text" name="username" class="form-control" required autofocus>
            </div>
            <div class="form-group">
                <label>Contraseña</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Iniciar Sesión</button>
        </form>
        <div class="auth-footer">
            <p>¿No tienes cuenta? <a href="/register/">Regístrate aquí</a></p>
        </div>
    </div>
</div>
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
        
        styles = AuthView._get_styles()
        
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro - Sistema de Inventario</title>
    {styles}
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
