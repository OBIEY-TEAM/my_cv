from django.urls import path
from .views import JobOfferListCreateView, ApplicationPackageListView

urlpatterns = [
    path('offers/', JobOfferListCreateView.as_view(), name='job_offer_list_create'),
    path('packages/', ApplicationPackageListView.as_view(), name='application_package_list'),
]
