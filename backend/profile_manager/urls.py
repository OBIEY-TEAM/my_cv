from django.urls import path
from .views import ProfileDetailView, PhotoCropView

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile_detail'),
    path('crop-photo/', PhotoCropView.as_view(), name='profile_crop_photo'),
]
