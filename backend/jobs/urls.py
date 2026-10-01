from django.urls import path
from .views import JobOfferListCreateView, ApplicationPackageListView, ApplicationPackageUpdateContentView

urlpatterns = [
    path('offers/', JobOfferListCreateView.as_view(), name='job_offer_list_create'),
    path('packages/', ApplicationPackageListView.as_view(), name='application_package_list'),
    path('packages/<int:pk>/update-content/', ApplicationPackageUpdateContentView.as_view(), name='application_package_update_content'),
]
