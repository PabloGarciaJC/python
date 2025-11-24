from django.urls import path
from app.controllers.auth_controller import AuthController
from app.controllers.dashboard_controller import DashboardController
from app.controllers.product_controller import ProductController
from app.controllers.category_controller import CategoryController
from app.controllers.client_controller import ClientController
from app.controllers.supplier_controller import SupplierController
from app.controllers.role_controller import RoleController
from app.controllers.warehouse_controller import WarehouseController
from app.controllers.sale_controller import SaleController
from app.controllers.sale_detail_controller import SaleDetailController
from app.controllers.purchase_controller import PurchaseController
from app.controllers.purchase_detail_controller import PurchaseDetailController
from app.controllers.inventory_movement_controller import InventoryMovementController
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
    path('clientes/', ClientController.index, name='clients'),
    path('clientes/crear/', ClientController.create, name='clients_create'),
    path('clientes/<int:client_id>/editar/', ClientController.edit, name='clients_edit'),
    path('clientes/<int:client_id>/eliminar/', ClientController.delete, name='clients_delete'),
    path('proveedores/', SupplierController.index, name='suppliers'),
    path('proveedores/crear/', SupplierController.create, name='suppliers_create'),
    path('proveedores/<int:supplier_id>/editar/', SupplierController.edit, name='suppliers_edit'),
    path('proveedores/<int:supplier_id>/eliminar/', SupplierController.delete, name='suppliers_delete'),
    path('roles/', RoleController.index, name='roles'),
    path('roles/crear/', RoleController.create, name='roles_create'),
    path('roles/<int:role_id>/editar/', RoleController.edit, name='roles_edit'),
    path('roles/<int:role_id>/eliminar/', RoleController.delete, name='roles_delete'),
    path('almacenes/', WarehouseController.index, name='warehouses'),
    path('almacenes/crear/', WarehouseController.create, name='warehouses_create'),
    path('almacenes/<int:warehouse_id>/editar/', WarehouseController.edit, name='warehouses_edit'),
    path('almacenes/<int:warehouse_id>/eliminar/', WarehouseController.delete, name='warehouses_delete'),
    path('ventas/', SaleController.index, name='sales'),
    path('ventas/crear/', SaleController.create, name='sales_create'),
    path('ventas/<int:sale_id>/editar/', SaleController.edit, name='sales_edit'),
    path('ventas/<int:sale_id>/eliminar/', SaleController.delete, name='sales_delete'),
    path('ventas/<int:sale_id>/ver/', SaleController.view, name='sales_view'),
    path('detalle-ventas/', SaleDetailController.index, name='sale_details'),
    path('detalle-ventas/crear/', SaleDetailController.create, name='sale_details_create'),
    path('detalle-ventas/<int:detail_id>/editar/', SaleDetailController.edit, name='sale_details_edit'),
    path('detalle-ventas/<int:detail_id>/eliminar/', SaleDetailController.delete, name='sale_details_delete'),
    path('detalle-ventas/<int:detail_id>/ver/', SaleDetailController.view, name='sale_details_view'),
    path('compras/', PurchaseController.index, name='purchases'),
    path('compras/crear/', PurchaseController.create, name='purchases_create'),
    path('compras/<int:purchase_id>/editar/', PurchaseController.edit, name='purchases_edit'),
    path('compras/<int:purchase_id>/eliminar/', PurchaseController.delete, name='purchases_delete'),
    path('compras/<int:purchase_id>/ver/', PurchaseController.view, name='purchases_view'),
    path('detalle-compras/', PurchaseDetailController.index, name='purchase_details'),
    path('detalle-compras/crear/', PurchaseDetailController.create, name='purchase_details_create'),
    path('detalle-compras/<int:detail_id>/editar/', PurchaseDetailController.edit, name='purchase_details_edit'),
    path('detalle-compras/<int:detail_id>/eliminar/', PurchaseDetailController.delete, name='purchase_details_delete'),
    path('detalle-compras/<int:detail_id>/ver/', PurchaseDetailController.view, name='purchase_details_view'),
    path('movimientos-inventario/', InventoryMovementController.index, name='inventory_movements'),
    path('movimientos-inventario/crear/', InventoryMovementController.create, name='inventory_movements_create'),
    path('movimientos-inventario/<int:movement_id>/editar/', InventoryMovementController.edit, name='inventory_movements_edit'),
    path('movimientos-inventario/<int:movement_id>/eliminar/', InventoryMovementController.delete, name='inventory_movements_delete'),
    path('movimientos-inventario/<int:movement_id>/ver/', InventoryMovementController.view, name='inventory_movements_view'),
    path('reportes/', ReportController.index, name='reports'),
    path('configuracion/', ConfigController.index, name='config'),
    path('configuracion/perfil/editar/', ConfigController.edit_profile, name='config_edit_profile'),
    path('configuracion/perfil/cambiar-password/', ConfigController.change_password, name='config_change_password'),
    path('configuracion/usuarios/crear/', ConfigController.create_user, name='config_create_user'),
    path('configuracion/usuarios/<int:user_edit_id>/editar/', ConfigController.edit_user, name='config_edit_user'),
    path('configuracion/usuarios/<int:user_delete_id>/eliminar/', ConfigController.delete_user, name='config_delete_user'),
]
