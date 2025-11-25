from app.models.user import User
from app.models.config import Config
from app.views.config_view import ConfigView
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
import hashlib

class ConfigController:
    @staticmethod
    def index(request):
        """Muestra la página de configuración"""
        # Verificar si el usuario está autenticado
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')
        
        # Obtener el usuario
        user = User.get_by_id(user_id)
        if not user:
            return redirect('/login/')
        
        # Verificar si es superadmin
        is_superadmin = user.get('username') == 'superadmin'
        
        # Obtener datos de configuración
        data = {
            'user_info': Config.get_user_info(user_id),
            'system_stats': Config.get_system_stats(),
            'all_users': Config.get_all_users(include_superadmin=is_superadmin),
            'database_info': Config.get_database_info()
        }
        
        # Renderizar la vista
        return HttpResponse(ConfigView.index(user, data))
    
    @staticmethod
    @ensure_csrf_cookie
    def create_user(request):
        """Crear un nuevo usuario"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Si es GET, mostrar formulario
        if request.method == 'GET':
            roles = Config.get_roles()
            return HttpResponse(ConfigView.create_user(user, roles, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                # Hashear la contraseña
                password = request.POST.get('password')
                password_hash = hashlib.md5(password.encode()).hexdigest()
                
                data = {
                    'username': request.POST.get('username'),
                    'password': password_hash,
                    'nombre_completo': request.POST.get('nombre_completo'),
                    'email': request.POST.get('email'),
                    'rol_id': request.POST.get('rol_id'),
                    'activo': 1
                }
                
                # Validaciones
                if not data['username'] or not password:
                    roles = Config.get_roles()
                    return HttpResponse(ConfigView.create_user(user, roles, request, error='Usuario y contraseña son obligatorios'))
                
                # Crear el usuario
                Config.create_user(data)
                
                # Redireccionar
                return HttpResponseRedirect('/configuracion/')
                
            except Exception as e:
                roles = Config.get_roles()
                return HttpResponse(ConfigView.create_user(user, roles, request, error=f'Error al crear usuario: {str(e)}'))
    
    @staticmethod
    @ensure_csrf_cookie
    def edit_user(request, user_edit_id):
        """Editar un usuario existente"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Obtener el usuario a editar
        user_to_edit = Config.get_user_by_id(user_edit_id)
        if not user_to_edit:
            return HttpResponseRedirect('/configuracion/')
        
        # Si es GET, mostrar formulario
        if request.method == 'GET':
            roles = Config.get_roles()
            return HttpResponse(ConfigView.edit_user(user, user_to_edit, roles, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                data = {
                    'username': request.POST.get('username'),
                    'nombre_completo': request.POST.get('nombre_completo'),
                    'email': request.POST.get('email'),
                    'rol_id': request.POST.get('rol_id'),
                    'activo': int(request.POST.get('activo', 1))
                }
                
                # Validaciones
                if not data['username']:
                    roles = Config.get_roles()
                    return HttpResponse(ConfigView.edit_user(user, user_to_edit, roles, request, error='El usuario es obligatorio'))
                
                # Actualizar el usuario
                Config.update_user(user_edit_id, data)
                
                # Redireccionar
                return HttpResponseRedirect('/configuracion/')
                
            except Exception as e:
                roles = Config.get_roles()
                return HttpResponse(ConfigView.edit_user(user, user_to_edit, roles, request, error=f'Error al actualizar usuario: {str(e)}'))
    
    @staticmethod
    def delete_user(request, user_delete_id):
        """Desactivar un usuario"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # No permitir desactivarse a sí mismo
        if user_id == user_delete_id:
            return HttpResponseRedirect('/configuracion/')
        
        # Desactivar el usuario
        Config.delete_user(user_delete_id)
        
        # Redireccionar
        return HttpResponseRedirect('/configuracion/')
    
    @staticmethod
    @ensure_csrf_cookie
    def edit_profile(request):
        """Editar el perfil del usuario actual"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Obtener información completa del usuario
        user_info = Config.get_user_info(user_id)
        
        # Verificar si el usuario está activo (solo usuarios con activo=1 pueden editar estado)
        is_active_user = user.get('activo') == 1
        
        # Si es GET, mostrar formulario
        if request.method == 'GET':
            return HttpResponse(ConfigView.edit_profile(user, user_info, request, is_admin=is_active_user))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                data = {
                    'nombre_completo': request.POST.get('nombre_completo'),
                    'email': request.POST.get('email')
                }
                
                # Solo permitir cambiar el estado si el usuario está activo (activo=1)
                if is_active_user:
                    data['activo'] = int(request.POST.get('activo', 1))
                
                # Actualizar el perfil
                Config.update_profile(user_id, data)
                
                # Redireccionar
                return HttpResponseRedirect('/configuracion/')
                
            except Exception as e:
                return HttpResponse(ConfigView.edit_profile(user, user_info, request, is_admin=is_active_user, error=f'Error al actualizar perfil: {str(e)}'))
    
    @staticmethod
    @ensure_csrf_cookie
    def change_password(request):
        """Cambiar contraseña del usuario actual"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        user = User.get_by_id(user_id)
        if not user:
            request.session.flush()
            return HttpResponseRedirect('/login/')
        
        # Si es GET, mostrar formulario
        if request.method == 'GET':
            return HttpResponse(ConfigView.change_password(user, request))
        
        # Si es POST, procesar el formulario
        if request.method == 'POST':
            try:
                current_password = request.POST.get('current_password')
                new_password = request.POST.get('new_password')
                confirm_password = request.POST.get('confirm_password')
                
                # Validar contraseña actual
                current_hash = hashlib.md5(current_password.encode()).hexdigest()
                if current_hash != user['password']:
                    return HttpResponse(ConfigView.change_password(user, request, error='La contraseña actual es incorrecta'))
                
                # Validar que las contraseñas coincidan
                if new_password != confirm_password:
                    return HttpResponse(ConfigView.change_password(user, request, error='Las contraseñas no coinciden'))
                
                # Validar longitud mínima
                if len(new_password) < 4:
                    return HttpResponse(ConfigView.change_password(user, request, error='La contraseña debe tener al menos 4 caracteres'))
                
                # Hashear nueva contraseña
                new_hash = hashlib.md5(new_password.encode()).hexdigest()
                
                # Actualizar contraseña
                Config.change_password(user_id, new_hash)
                
                # Redireccionar
                return HttpResponseRedirect('/configuracion/')
                
            except Exception as e:
                return HttpResponse(ConfigView.change_password(user, request, error=f'Error al cambiar contraseña: {str(e)}'))

