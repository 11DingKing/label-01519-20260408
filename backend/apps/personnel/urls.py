"""
人员管理URL配置
"""
from django.urls import path
from .views import (
    AttendancePersonListCreateView, AttendancePersonDetailView,
    StockOutPersonListCreateView, StockOutPersonDetailView
)

urlpatterns = [
    # 考勤人员管理
    path('attendance-persons/', AttendancePersonListCreateView.as_view(), name='attendance-person-list'),
    path('attendance-persons/<int:pk>/', AttendancePersonDetailView.as_view(), name='attendance-person-detail'),
    
    # 出库人员管理
    path('stock-out-persons/', StockOutPersonListCreateView.as_view(), name='stock-out-person-list'),
    path('stock-out-persons/<int:pk>/', StockOutPersonDetailView.as_view(), name='stock-out-person-detail'),
]
