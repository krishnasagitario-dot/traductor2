from django.urls import path
from . import views

urlpatterns = [
    # Login real
    path('', views.login_user, name='login_user'),
    path('login/', views.login_user, name='login_user'),

    # Registro y logout
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # HOME
    path('home/', views.home, name='home'),

    # Doctor
    path('translate/', views.translator_page, name='translator_page'),
    path('traducir/', views.translate_text, name='translate_text'),

    # Admin - Traducciones
    path('admin_traducciones/', views.manage_translations, name='manage_translations'),

    # API traducción
    path('api/translate/', views.TranslateAPIView.as_view(), name='translate_api'),

    # CRUD traducciones
    path('traduccion/<int:pk>/editar/', views.edit_traduccion, name='edit_traduccion'),
    path('traduccion/<int:pk>/eliminar/', views.delete_traduccion, name='delete_traduccion'),

    # JSON
    path('api/observations/', views.list_observations, name='list_observations'),

    # Employees
    #path('employee/', views.EmployeeView, name='employee_view'),

    # API Notificaciones
    path("api/notificaciones/", views.api_notificaciones, name="api_notificaciones"),

    # Panel Admin de Notificaciones (CORREGIDO)
    path("notificaciones/admin/", views.admin_notificaciones, name="admin_notificaciones"),

    # Marcar como leída
    path("notificacion/<int:pk>/leer/", views.mark_notificacion_read, name="mark_notificacion_read"),

    path('', views.notificaciones_home, name='notificaciones_home'),

     path('admin/', views.admin_notificaciones, name='panel_admin'),


     

]
