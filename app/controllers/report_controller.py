from app.models.user import User
from app.models.report import Report
from app.views.report_view import ReportView
from django.shortcuts import redirect
from django.http import HttpResponse

class ReportController:
    @staticmethod
    def index(request):
        """Muestra el dashboard de reportes"""
        # Verificar si el usuario está autenticado
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')
        
        # Obtener el usuario
        user = User.get_by_id(user_id)
        if not user:
            return redirect('/login/')
        
        # Obtener datos para reportes
        data = {
            'resumen': Report.resumen_general(),
            'ventas_mes': Report.ventas_por_mes(),
            'productos_top': Report.productos_mas_vendidos(5),
            'ventas_estado': Report.ventas_por_estado(),
            'clientes_top': Report.clientes_frecuentes(5),
            'stock_bajo': Report.inventario_bajo_stock(10)
        }
        
        # Renderizar la vista
        return HttpResponse(ReportView.index(user, data))
