from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

def root_health_check(request):
    return JsonResponse({
        "status": "online",
        "service": "Luka Mosala SaaS API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth/",
            "profile": "/api/profile/",
            "jobs": "/api/jobs/",
            "subscriptions": "/api/subscriptions/",
            "jules": "/api/jules/",
            "swagger": "/api/docs/swagger/",
            "redoc": "/api/docs/redoc/",
            "schema": "/api/docs/schema/",
            "admin": "/admin/"
        }
    })

urlpatterns = [
    path('', root_health_check, name='root_health_check'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/profile/', include('profile_manager.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/jules/', include('jules_integration.urls')),

    # Swagger / OpenAPI Documentation
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
