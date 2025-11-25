from django.http import HttpResponse, HttpResponseRedirect
from app.models.user import User
from app.views.documentation_view import DocumentationView

class DocumentationController:
    """Controlador de Documentación"""
    
    @staticmethod
    def index(request):
        """Muestra la página de documentación del sistema"""
        # Verificar autenticación
        user_id = request.session.get('user_id')
        
        if not user_id:
            return HttpResponseRedirect('/login/')
        
        # Obtener usuario
        user = User.get_by_id(user_id)
        
        if not user:
            return HttpResponseRedirect('/login/')
        
        return DocumentationView.index(user, request.path)
