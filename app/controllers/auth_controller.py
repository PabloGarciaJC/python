from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token
from app.models.user import User
from app.views.auth_view import AuthView

class AuthController:
    """Controlador de Autenticación"""
    
    @staticmethod
    def login(request):
        """Maneja login"""
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = User.authenticate(username, password)
            
            if user:
                request.session['user_id'] = user['id']
                request.session['username'] = user['username']
                return HttpResponseRedirect('/')
            else:
                csrf_token = get_token(request)
                return HttpResponse(AuthView.login(error='Usuario o contraseña incorrectos', csrf_token=csrf_token))
        
        csrf_token = get_token(request)
        return HttpResponse(AuthView.login(csrf_token=csrf_token))
    
    @staticmethod
    def register(request):
        """Maneja registro"""
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            nombre_completo = request.POST.get('nombre_completo')
            
            # Validaciones
            errors = []
            
            if not all([username, email, password, password_confirm, nombre_completo]):
                errors.append('Todos los campos son obligatorios')
            
            if password != password_confirm:
                errors.append('Las contraseñas no coinciden')
            
            if len(password) < 6:
                errors.append('La contraseña debe tener al menos 6 caracteres')
            
            if User.exists(username=username):
                errors.append('El nombre de usuario ya está en uso')
            
            if User.exists(email=email):
                errors.append('El email ya está registrado')
            
            if errors:
                csrf_token = get_token(request)
                return HttpResponse(AuthView.register(errors=errors, csrf_token=csrf_token, form_data=request.POST))
            
            # Crear usuario
            user_id = User.create(username, email, password, nombre_completo)
            
            if user_id:
                # Auto-login después del registro
                request.session['user_id'] = user_id
                request.session['username'] = username
                return HttpResponseRedirect('/')
            else:
                csrf_token = get_token(request)
                return HttpResponse(AuthView.register(errors=['Error al crear el usuario'], csrf_token=csrf_token))
        
        csrf_token = get_token(request)
        return HttpResponse(AuthView.register(csrf_token=csrf_token))
    
    @staticmethod
    def logout(request):
        """Cierra sesión"""
        request.session.flush()
        return HttpResponseRedirect('/login/')
