from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JulesSessionViewSet

router = DefaultRouter()
router.register(r'sessions', JulesSessionViewSet, basename='jules-session')

urlpatterns = [
    path('', include(router.urls)),
]
