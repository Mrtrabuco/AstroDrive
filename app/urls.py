from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('dashboard/mapa1', views.mapa_1, name='mapa1'),
    path('dashboard/mapa2', views.mapa_2, name='mapa2'),
    path('dashboard/mapa3', views.mapa_3, name='mapa3'),
    path('dashboard/mapa4', views.mapa_4, name='mapa4'),
    path('dashboard/mapa5', views.mapa_5, name='mapa5'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)