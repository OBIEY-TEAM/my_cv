from django.urls import path
from .views import PlanListView, UserSubscriptionView, InitiatePaymentView

urlpatterns = [
    path('plans/', PlanListView.as_view(), name='plan_list'),
    path('me/', UserSubscriptionView.as_view(), name='subscription_me'),
    path('pay/', InitiatePaymentView.as_view(), name='initiate_payment'),
]
