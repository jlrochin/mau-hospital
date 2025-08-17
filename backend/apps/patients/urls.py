from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Endpoints de pacientes
    path('', views.PacienteListCreateView.as_view(), name='paciente_list_create'),
    path('buscar/', views.buscar_paciente, name='buscar_paciente'),
    path('verificar-duplicados/', views.verificar_duplicados, name='verificar_duplicados'),
    path('<str:expediente>/', views.PacienteDetailView.as_view(), name='paciente_detail'),
    path('<str:expediente>/historial/', views.paciente_historial, name='paciente_historial'),
    
    # Endpoints de CIE-10 México
    path('cie10/', views.CIE10MexicoListView.as_view(), name='cie10_list'),
    path('cie10/buscar/', views.buscar_cie10, name='buscar_cie10'),
    path('cie10/estadisticas/', views.estadisticas_cie10, name='estadisticas_cie10'),
    path('<str:expediente>/cie10-aplicables/', views.cie10_para_paciente, name='cie10_para_paciente'),
]
