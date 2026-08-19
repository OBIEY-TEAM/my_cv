from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileDetailView, PhotoCropView, UserProfileInfoView,
    ExperienceViewSet, CertificationViewSet,
    EducationViewSet, ProjectViewSet
)

router = DefaultRouter()
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'certifications', CertificationViewSet, basename='certification')
router.register(r'educations', EducationViewSet, basename='education')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile_detail'),
    path('info/', UserProfileInfoView.as_view(), name='profile_info'),
    path('crop-photo/', PhotoCropView.as_view(), name='profile_crop_photo'),
    path('', include(router.urls)),
]
