"""
前端页面URL配置
"""
from django.urls import path
from .views import (
    LoginPageView, IndexPageView, TestPageView, DashboardPageView,
    StockInPageView, UnitPageView, CategoryPageView, VarietyPageView,
    QueryExportPageView, DailyReportPageView, WarningPageView,
    ApprovalPageView, AttendancePersonPageView, StockOutPersonPageView
)

urlpatterns = [
    path('', LoginPageView.as_view(), name='login-page'),
    path('login/', LoginPageView.as_view(), name='login-page-alt'),
    path('index/', IndexPageView.as_view(), name='index-page'),
    path('test/', TestPageView.as_view(), name='test-page'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard-page'),
    path('stock-in/', StockInPageView.as_view(), name='stock-in-page'),
    path('unit/', UnitPageView.as_view(), name='unit-page'),
    path('category/', CategoryPageView.as_view(), name='category-page'),
    path('variety/', VarietyPageView.as_view(), name='variety-page'),
    path('query-export/', QueryExportPageView.as_view(), name='query-export-page'),
    path('daily-report/', DailyReportPageView.as_view(), name='daily-report-page'),
    path('warning/', WarningPageView.as_view(), name='warning-page'),
    path('approval/', ApprovalPageView.as_view(), name='approval-page'),
    path('attendance-person/', AttendancePersonPageView.as_view(), name='attendance-person-page'),
    path('stock-out-person/', StockOutPersonPageView.as_view(), name='stock-out-person-page'),
]
