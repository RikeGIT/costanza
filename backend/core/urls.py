"""
URL configuration for costanza project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from gamification.api.v1.router import router as gamification_router


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ----------------------------------------------------
    # --- 1. ROTAS DE AUTENTICAÇÃO (DJOSER + JWT + OAuth) ---
    # ----------------------------------------------------
    
    # Rotas de Login, Registro, Reset de Senha, etc. (users/)
    # Endpoint de registro será: POST /api/auth/users/
    # BOM: Ordem correta
    path('api/auth/', include('djoser.urls.jwt')),
    
    # Rotas para JWT: /jwt/create (Login), /jwt/refresh, /jwt/verify
    # Endpoint de login será: POST /api/auth/jwt/create/
    path('api/auth/', include('djoser.urls')), 
    
    # Rotas para Social Auth (OAuth: Google, Github)
    # Endpoint de social será: /api/auth/o/google-oauth2/
    path('api/auth/', include('allauth.socialaccount.urls')), 

    # ----------------------------------------------------
    # --- 3. ROTAS DA SUA API (v1) ---
    # ----------------------------------------------------
    
    # Rotas de usuários e autenticação
    path('api/v1/users/', include('user.api.v1.router')),
    # Rotas de amizades
    path('api/v1/', include('friends.api.v1.router')),
    # Rotas de eventos universitários
    path('api/v1/events/', include('events.api.v1.router')),
    # Rotas do sistema de estudos
    path('api/v1/', include('trilhas.api.v1.router')),
    
    # URLs da documentação API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/gamification/', include(gamification_router.urls)),
]

# Adiciona URLs para servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)