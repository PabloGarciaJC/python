from django.http import HttpResponse
from app.views.layout import Layout

class ConfigView:
    """Vista de Configuración"""
    
    @staticmethod
    def index(user, data):
        """Renderiza la página de configuración del sistema"""
        
        user_info = data.get('user_info', {})
        system_stats = data.get('system_stats', {})
        all_users = data.get('all_users', [])
        database_info = data.get('database_info', [])
        
        # Sección de información del usuario
        user_section = f"""
        <div class="card">
            <div class="card-header"><i class="fas fa-user"></i> Mi Perfil</div>
            <div class="p-20">
                <div class="config-info-grid">
                    <div class="config-info-item">
                        <p>Usuario</p>
                        <p>{user_info.get('username', 'N/A')}</p>
                    </div>
                    <div class="config-info-item">
                        <p>Nombre Completo</p>
                        <p>{user_info.get('nombre_completo', 'N/A')}</p>
                    </div>
                    <div class="config-info-item">
                        <p>Email</p>
                        <p>{user_info.get('email', 'N/A')}</p>
                    </div>
                    <div class="config-info-item">
                        <p>Rol</p>
                        <p>{user_info.get('rol', 'N/A')}</p>
                    </div>
                    <div class="config-info-item">
                        <p>Estado</p>
                        <p>
                            {'<span class="badge badge-success">Activo</span>' if user_info.get('activo') else '<span class="badge badge-inactive">Inactivo</span>'}
                        </p>
                    </div>
                    <div class="config-info-item">
                        <p>Miembro desde</p>
                        <p>{user_info.get('created_at', 'N/A')}</p>
                    </div>
                </div>
                <div class="mt-20">
                    <a href="/configuracion/perfil/editar/" class="btn btn-primary">Editar Perfil</a>
                    <a href="/configuracion/perfil/cambiar-password/" class="btn btn-warning ml-10">Cambiar Contraseña</a>
                </div>
            </div>
        </div>
        """
        
        # Sección de estadísticas del sistema
        stats_section = f"""
        <div class="card">
            <div class="card-header"><i class="fas fa-chart-bar"></i> Estadísticas del Sistema</div>
            <div class="stats-grid">
                <div class="stat-card bg-gradient-purple">
                    <h3>Usuarios</h3>
                    <div class="value">{system_stats.get('total_usuarios', 0)}</div>
                </div>
                <div class="stat-card bg-gradient-pink">
                    <h3>Productos</h3>
                    <div class="value">{system_stats.get('total_productos', 0)}</div>
                </div>
                <div class="stat-card bg-gradient-cyan">
                    <h3>Clientes</h3>
                    <div class="value">{system_stats.get('total_clientes', 0)}</div>
                </div>
                <div class="stat-card bg-gradient-green">
                    <h3>Ventas</h3>
                    <div class="value">{system_stats.get('total_ventas', 0)}</div>
                </div>
            </div>
        </div>
        """
        
        # Sección de usuarios del sistema
        users_rows = ""
        if all_users:
            for usuario in all_users:
                estado_badge = '<span class="badge badge-success">Activo</span>' if usuario['activo'] else '<span class="badge badge-inactive">Inactivo</span>'
                users_rows += f"""
                <tr>
                    <td>{usuario['username']}</td>
                    <td>{usuario['nombre_completo']}</td>
                    <td>{usuario['email'] or 'N/A'}</td>
                    <td>{usuario['rol']}</td>
                    <td>{estado_badge}</td>
                    <td>
                        <a href="/configuracion/usuarios/{usuario['id']}/editar/" class="btn btn-warning no-underline">Editar</a>
                        <a href="/configuracion/usuarios/{usuario['id']}/eliminar/" class="btn btn-danger no-underline" onclick="return confirm('¿Está seguro de desactivar este usuario?');">Desactivar</a>
                    </td>
                </tr>
                """
        else:
            users_rows = '<tr><td colspan="6" class="empty-state">No hay usuarios</td></tr>'
        
        users_section = f"""
        <div class="card">
            <div class="card-header">
                <span><i class="fas fa-users"></i> Usuarios del Sistema</span>
                <a href="/configuracion/usuarios/crear/" class="btn btn-primary">+ Nuevo Usuario</a>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Usuario</th>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Rol</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        # Sección de información de base de datos
        db_rows = ""
        if database_info:
            for table in database_info:
                db_rows += f"""
                <tr>
                    <td>{table['table_name']}</td>
                    <td>{table['table_rows']:,}</td>
                    <td>{table['size_mb']} MB</td>
                </tr>
                """
        else:
            db_rows = '<tr><td colspan="3" class="empty-state">No hay información disponible</td></tr>'
        
        db_section = f"""
        <div class="card">
            <div class="card-header"><i class="fas fa-database"></i> Información de Base de Datos</div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Tabla</th>
                            <th>Registros</th>
                            <th>Tamaño</th>
                        </tr>
                    </thead>
                    <tbody>
                        {db_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        content = f"""
        {user_section}
        {stats_section}
        {users_section}
        {db_section}
        """
        
        return HttpResponse(Layout.render('Configuración', user, 'configuracion', content))
    
    @staticmethod
    def create_user(user, roles, request, error=None):
        """Vista del formulario de crear usuario"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Generar opciones de roles
        role_options = ""
        for role in roles:
            role_options += f'<option value="{role["id"]}">{role["nombre"]}</option>'
        
        # Mensaje de error
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nuevo Usuario</span>
                <a href="/configuracion/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/configuracion/usuarios/crear/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Usuario *</label>
                        <input type="text" name="username" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Contraseña *</label>
                        <input type="password" name="password" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Nombre Completo</label>
                        <input type="text" name="nombre_completo" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Email</label>
                        <input type="email" name="email" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Rol *</label>
                        <select name="rol_id" required class="form-select">
                            <option value="">Seleccione un rol</option>
                            {role_options}
                        </select>
                    </div>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Guardar Usuario</button>
                    <a href="/configuracion/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Crear Usuario', user, 'configuracion', content))
    
    @staticmethod
    def edit_user(user, user_to_edit, roles, request, error=None):
        """Vista del formulario de editar usuario"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Generar opciones de roles
        role_options = ""
        for role in roles:
            selected = 'selected' if role['id'] == user_to_edit.get('rol_id') else ''
            role_options += f'<option value="{role["id"]}" {selected}>{role["nombre"]}</option>'
        
        # Mensaje de error
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Usuario</span>
                <a href="/configuracion/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/configuracion/usuarios/{user_to_edit['id']}/editar/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Usuario *</label>
                        <input type="text" name="username" value="{user_to_edit['username']}" required class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Nombre Completo</label>
                        <input type="text" name="nombre_completo" value="{user_to_edit.get('nombre_completo', '')}" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Email</label>
                        <input type="email" name="email" value="{user_to_edit.get('email', '')}" class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Rol *</label>
                        <select name="rol_id" required class="form-select">
                            <option value="">Seleccione un rol</option>
                            {role_options}
                        </select>
                    </div>
                    
                    <div>
                        <label class="form-label">Estado *</label>
                        <select name="activo" required class="form-select">
                            <option value="1" {'selected' if user_to_edit.get('activo', 1) == 1 else ''}>Activo</option>
                            <option value="0" {'selected' if user_to_edit.get('activo', 1) == 0 else ''}>Inactivo</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Actualizar Usuario</button>
                    <a href="/configuracion/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Usuario', user, 'configuracion', content))
    
    @staticmethod
    def edit_profile(user, user_info, request, is_admin=False, error=None):
        """Vista del formulario de editar perfil del usuario actual"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Mensaje de error
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        # Campo de estado solo si es administrador
        estado_field = ""
        if is_admin:
            estado_field = f"""
            <div>
                <label class="form-label">Estado *</label>
                <select name="activo" required 
                        class="form-select">
                    <option value="1" {'selected' if user_info.get('activo', 1) == 1 else ''}>Activo</option>
                    <option value="0" {'selected' if user_info.get('activo', 1) == 0 else ''}>Inactivo</option>
                </select>
            </div>
            """
        else:
            estado_field = f"""
            <div>
                <label class="form-label">Estado</label>
                <input type="text" value="{'Activo' if user_info.get('activo', 1) == 1 else 'Inactivo'}" disabled 
                       class="form-input-disabled">
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Mi Perfil</span>
                <a href="/configuracion/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/configuracion/perfil/editar/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="form-grid">
                    <div>
                        <label class="form-label">Usuario</label>
                        <input type="text" value="{user_info.get('username', '')}" disabled 
                               class="form-input-disabled">
                        <small class="form-hint">El usuario no se puede cambiar</small>
                    </div>
                    
                    <div>
                        <label class="form-label">Nombre Completo</label>
                        <input type="text" name="nombre_completo" value="{user_info.get('nombre_completo', '')}" 
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Email</label>
                        <input type="email" name="email" value="{user_info.get('email', '')}" 
                               class="form-input">
                    </div>
                    
                    <div>
                        <label class="form-label">Rol</label>
                        <input type="text" value="{user_info.get('rol', '')}" disabled 
                               class="form-input-disabled">
                        <small class="form-hint">El rol no se puede cambiar</small>
                    </div>
                    
                    {estado_field}
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Actualizar Perfil</button>
                    <a href="/configuracion/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Perfil', user, 'configuracion', content))
    
    @staticmethod
    def change_password(user, request, error=None):
        """Vista del formulario de cambiar contraseña"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Mensaje de error
        error_html = ""
        if error:
            error_html = f"""
            <div class="alert-error">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Cambiar Contraseña</span>
                <a href="/configuracion/" class="btn btn-secondary">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/configuracion/perfil/cambiar-password/" class="p-20">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div class="max-w-500">
                    <div class="form-field">
                        <label class="form-label">Contraseña Actual *</label>
                        <input type="password" name="current_password" required 
                               class="form-input">
                    </div>
                    
                    <div class="form-field">
                        <label class="form-label">Nueva Contraseña *</label>
                        <input type="password" name="new_password" required 
                               class="form-input">
                        <small class="form-hint">Mínimo 4 caracteres</small>
                    </div>
                    
                    <div class="form-field">
                        <label class="form-label">Confirmar Nueva Contraseña *</label>
                        <input type="password" name="confirm_password" required 
                               class="form-input">
                    </div>
                </div>
                
                <div class="form-actions mt-30">
                    <button type="submit" class="btn btn-primary">Cambiar Contraseña</button>
                    <a href="/configuracion/" class="btn btn-secondary no-underline">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Cambiar Contraseña', user, 'configuracion', content))

