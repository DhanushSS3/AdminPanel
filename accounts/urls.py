# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/live-user-profiles/', views.live_user_profiles, name='live_user_profiles'),
    path('api/demo-user-profiles/', views.demo_user_profiles, name='demo_user_profiles'),
    path('api/login/', views.login_view, name='login'),
    path('api/dashboard/', views.dashboard_view, name='dashboard'),
    path('api/groups/', views.group_list, name='group-list'),
    path('api/orders/', views.order_list, name='order-list'),
    path('api/withdrawal-requests/', views.withdrawal_requests_list, name='withdrawal-request-list'),
]