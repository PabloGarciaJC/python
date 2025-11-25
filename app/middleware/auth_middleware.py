from django.http import JsonResponse
from app.models.user import User

class AuthMiddleware:
    """Middleware para verificar permisos de usuario"""
    
    @staticmethod
    def check_user_active(request):
        """Verifica si el usuario está activo"""
        user_id = request.session.get('user_id')
        
        if not user_id:
            return False, None
        
        user = User.get_by_id(user_id)
        
        if not user:
            return False, None
        
        # Si activo = 1 → Usuario PUEDE modificar (retorna True)
        # Si activo = 0 → Usuario NO puede modificar (retorna False)
        is_active = user.get('activo', 0) == 1
        
        return is_active, user
    
    @staticmethod
    def require_active_user(view_func):
        """Decorador para restringir usuarios activos en operaciones de escritura"""
        def wrapper(request, *args, **kwargs):
            # Solo verificar en operaciones POST (crear, editar, eliminar)
            if request.method == 'POST':
                is_active, user = AuthMiddleware.check_user_active(request)
                
                # Si el usuario NO está activo (activo = 0), mostrar restricción
                if not is_active:
                    # Retornar respuesta JSON indicando acceso restringido
                    return JsonResponse({
                        'success': False,
                        'restricted': True,
                        'message': 'Acceso Restringido'
                    })
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
