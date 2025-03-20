from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/live-user-profiles/', views.live_user_profiles, name='live_user_profiles'),
    path('api/demo-user-profiles/', views.demo_user_profiles, name='demo_user_profiles'),
    path('api/login/', views.login_view, name='login'),
    path('api/dashboard/', views.dashboard_view, name='dashboard'),
    path('api/groups/', views.group_list_create, name='group-list-create'),
    path('api/orders/', views.order_list, name='order-list'),
    path('api/withdrawal-requests/', views.withdrawal_requests_list, name='withdrawal-request-list'),
    path('api/customers/<int:customer_id>/update_customer_details/', views.update_customer_details, name='update_customer_details'),
    path('api/user-kyc/<int:user_id>/', views.get_user_kyc_details, name='get_user_kyc_details'),
    path('api/update-customer-funds/', views.update_customer_funds, name='update_customer_funds'),
    path('api/wallet-transactions/<str:user_id>/', views.get_wallet_transactions, name='get_wallet_transactions'),
    path('api/user-trades/<int:user_id>/', views.user_trades, name='user_trades'),
    path('api/block-unblock/', views.block_unblock_user, name='block_unblock_user'),

]

