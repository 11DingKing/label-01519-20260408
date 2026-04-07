"""
认证URL配置
"""
from django.urls import path
from .views import LoginView, LogoutView, UserInfoView, OperationLogListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('logs/', OperationLogListView.as_view(), name='operation-logs'),
]
