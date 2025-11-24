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
            <div class="card-header">👤 Mi Perfil</div>
            <div style="padding: 20px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                    <div>
                        <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Usuario</p>
                        <p style="font-weight: 600;">{user_info.get('username', 'N/A')}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Nombre Completo</p>
                        <p style="font-weight: 600;">{user_info.get('nombre_completo', 'N/A')}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Email</p>
                        <p style="font-weight: 600;">{user_info.get('email', 'N/A')}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Rol</p>
                        <p style="font-weight: 600;">{user_info.get('rol', 'N/A')}</p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Estado</p>
                        <p style="font-weight: 600;">
                            {'<span class="badge badge-success">Activo</span>' if user_info.get('activo') else '<span class="badge" style="background: #fee2e2; color: #991b1b;">Inactivo</span>'}
                        </p>
                    </div>
                    <div>
                        <p style="color: #666; font-size: 0.9rem; margin-bottom: 5px;">Miembro desde</p>
                        <p style="font-weight: 600;">{user_info.get('created_at', 'N/A')}</p>
                    </div>
                </div>
                <div style="margin-top: 20px;">
                    <a href="/configuracion/perfil/editar/" class="btn btn-primary">Editar Perfil</a>
                    <a href="/configuracion/perfil/cambiar-password/" class="btn btn-warning" style="margin-left: 10px;">Cambiar Contraseña</a>
                </div>
            </div>
        </div>
        """
        
        # Sección de estadísticas del sistema
        stats_section = f"""
        <div class="card">
            <div class="card-header">📊 Estadísticas del Sistema</div>
            <div class="stats-grid">
                <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <h3>Usuarios</h3>
                    <div class="value">{system_stats.get('total_usuarios', 0)}</div>
                </div>
                <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <h3>Productos</h3>
                    <div class="value">{system_stats.get('total_productos', 0)}</div>
                </div>
                <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <h3>Clientes</h3>
                    <div class="value">{system_stats.get('total_clientes', 0)}</div>
                </div>
                <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
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
                estado_badge = '<span class="badge badge-success">Activo</span>' if usuario['activo'] else '<span class="badge" style="background: #fee2e2; color: #991b1b;">Inactivo</span>'
                users_rows += f"""
                <tr>
                    <td>{usuario['username']}</td>
                    <td>{usuario['nombre_completo']}</td>
                    <td>{usuario['email'] or 'N/A'}</td>
                    <td>{usuario['rol']}</td>
                    <td>{estado_badge}</td>
                    <td>
                        <a href="/configuracion/usuarios/{usuario['id']}/editar/" class="btn btn-warning" style="text-decoration: none;">Editar</a>
                        <a href="/configuracion/usuarios/{usuario['id']}/eliminar/" class="btn btn-danger" style="text-decoration: none;" onclick="return confirm('¿Está seguro de desactivar este usuario?');">Desactivar</a>
                    </td>
                </tr>
                """
        else:
            users_rows = '<tr><td colspan="6" class="empty-state">No hay usuarios</td></tr>'
        
        users_section = f"""
        <div class="card">
            <div class="card-header">
                <span>👥 Usuarios del Sistema</span>
                <a href="/configuracion/usuarios/crear/" class="btn btn-primary">+ Nuevo Usuario</a>
            </div>
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
            <div class="card-header">💾 Información de Base de Datos</div>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Crear Nuevo Usuario</span>
                <a href="/configuracion/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/configuracion/usuarios/crear/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Usuario *</label>
                        <input type="text" name="username" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Contraseña *</label>
                        <input type="password" name="password" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre Completo</label>
                        <input type="text" name="nombre_completo" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email</label>
                        <input type="email" name="email" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Rol *</label>
                        <select name="rol_id" required 
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="">Seleccione un rol</option>
                            {role_options}
                        </select>
                    </div>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Guardar Usuario</button>
                    <a href="/configuracion/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Usuario</span>
                <a href="/configuracion/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/configuracion/usuarios/{user_to_edit['id']}/editar/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Usuario *</label>
                        <input type="text" name="username" value="{user_to_edit['username']}" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre Completo</label>
                        <input type="text" name="nombre_completo" value="{user_to_edit.get('nombre_completo', '')}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email</label>
                        <input type="email" name="email" value="{user_to_edit.get('email', '')}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Rol *</label>
                        <select name="rol_id" required 
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="">Seleccione un rol</option>
                            {role_options}
                        </select>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Estado *</label>
                        <select name="activo" required 
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="1" {'selected' if user_to_edit.get('activo', 1) == 1 else ''}>Activo</option>
                            <option value="0" {'selected' if user_to_edit.get('activo', 1) == 0 else ''}>Inactivo</option>
                        </select>
                    </div>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Actualizar Usuario</button>
                    <a href="/configuracion/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Editar Usuario', user, 'configuracion', content))
    
    @staticmethod
    def edit_profile(user, user_info, request, error=None):
        """Vista del formulario de editar perfil del usuario actual"""
        
        # Obtener token CSRF
        from django.middleware.csrf import get_token
        csrf_token = get_token(request)
        
        # Mensaje de error
        error_html = ""
        if error:
            error_html = f"""
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Editar Mi Perfil</span>
                <a href="/configuracion/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/configuracion/perfil/editar/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Usuario</label>
                        <input type="text" value="{user_info.get('username', '')}" disabled 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f5f5f5;">
                        <small style="color: #666;">El usuario no se puede cambiar</small>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nombre Completo</label>
                        <input type="text" name="nombre_completo" value="{user_info.get('nombre_completo', '')}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Email</label>
                        <input type="email" name="email" value="{user_info.get('email', '')}" 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Rol</label>
                        <input type="text" value="{user_info.get('rol', '')}" disabled 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; background: #f5f5f5;">
                        <small style="color: #666;">El rol no se puede cambiar</small>
                    </div>
                    
                    <div>
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Estado *</label>
                        <select name="activo" required 
                                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                            <option value="1" {'selected' if user_info.get('activo', 1) == 1 else ''}>Activo</option>
                            <option value="0" {'selected' if user_info.get('activo', 1) == 0 else ''}>Inactivo</option>
                        </select>
                    </div>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Actualizar Perfil</button>
                    <a href="/configuracion/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
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
            <div style="background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                {error}
            </div>
            """
        
        content = f"""
        <div class="card">
            <div class="card-header">
                <span>Cambiar Contraseña</span>
                <a href="/configuracion/" class="btn" style="background: #6b7280; color: white;">← Volver</a>
            </div>
            {error_html}
            <form method="POST" action="/configuracion/perfil/cambiar-password/" style="padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                
                <div style="max-width: 500px;">
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Contraseña Actual *</label>
                        <input type="password" name="current_password" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Nueva Contraseña *</label>
                        <input type="password" name="new_password" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                        <small style="color: #666;">Mínimo 4 caracteres</small>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Confirmar Nueva Contraseña *</label>
                        <input type="password" name="confirm_password" required 
                               style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                </div>
                
                <div style="margin-top: 30px; display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary">Cambiar Contraseña</button>
                    <a href="/configuracion/" class="btn" style="background: #6b7280; color: white; text-decoration: none;">Cancelar</a>
                </div>
            </form>
        </div>
        """
        
        return HttpResponse(Layout.render('Cambiar Contraseña', user, 'configuracion', content))

