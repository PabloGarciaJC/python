from django.urls import path
from app.controllers.auth_controller import AuthController
from app.controllers.dashboard_controller import DashboardController
from app.controllers.product_controller import ProductController
from app.controllers.category_controller import CategoryController
from app.controllers.sale_controller import SaleController
from app.controllers.report_controller import ReportController
from app.controllers.config_controller import ConfigController

urlpatterns = [
    path('', DashboardController.index, name='dashboard'),
    path('login/', AuthController.login, name='login'),
    path('register/', AuthController.register, name='register'),
    path('logout/', AuthController.logout, name='logout'),
    path('productos/', ProductController.index, name='products'),
    path('productos/crear/', ProductController.create, name='products_create'),
    path('productos/<int:product_id>/editar/', ProductController.edit, name='products_edit'),
    path('productos/<int:product_id>/eliminar/', ProductController.delete, name='products_delete'),
    path('categorias/', CategoryController.index, name='categories'),
    path('categorias/crear/', CategoryController.create, name='categories_create'),
    path('categorias/<int:category_id>/editar/', CategoryController.edit, name='categories_edit'),
    path('categorias/<int:category_id>/eliminar/', CategoryController.delete, name='categories_delete'),
    path('ventas/', SaleController.index, name='sales'),
    path('ventas/crear/', SaleController.create, name='sales_create'),
    path('ventas/<int:sale_id>/editar/', SaleController.edit, name='sales_edit'),
    path('ventas/<int:sale_id>/eliminar/', SaleController.delete, name='sales_delete'),
    path('reportes/', ReportController.index, name='reports'),
    path('configuracion/', ConfigController.index, name='config'),
]
