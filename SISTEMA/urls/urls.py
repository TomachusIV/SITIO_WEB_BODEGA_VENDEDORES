from django.urls import path

from SISTEMA.views.views import ExportarReportesView, LoginView, HomeView, LogoutView, IngresarReporteView, VerReporteView, IngresarPosibleClienteView, VerPosibleClienteView, ConvertirPosibleClienteView, VerClienteView, error_500_view, error_404_view

urlpatterns = [
    
    
    
    path('', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('reportes/ingresar/', IngresarReporteView.as_view(), name='ingresar_reporte'),
    path('reportes/ver/', VerReporteView.as_view(), name='ver_reporte'),

    path('posibles-clientes/ingresar/', IngresarPosibleClienteView.as_view(), name='ingresar_posible_cliente'),
    path('posibles-clientes/ver/', VerPosibleClienteView.as_view(), name='ver_posible_cliente'),
    path('clientes/ingresar/<int:pk>/', ConvertirPosibleClienteView.as_view(), name='ingresar_cliente'),
    path('clientes/ver/', VerClienteView.as_view(), name='ver_cliente'),
    
    path('reportes/exportar/', ExportarReportesView.as_view(), name='exportar_reportes')
    
    
    
]

handler404 = error_404_view
handler500 = error_500_view
