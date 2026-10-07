from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/auth/login/', views.api_login, name='api_login'),
    path('api/auth/logout/', views.api_logout, name='api_logout'),
    path('api/categorias/', views.api_categorias, name='api_categorias'),
    path('api/lotes/', views.api_lotes_coleccion, name='api_lotes_coleccion'),
    path('api/lotes/<int:lote_id>/', views.api_lote_detalle, name='api_lote_detalle'),
]
