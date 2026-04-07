"""
库房管理URL配置
"""
from django.urls import path
from .views import (
    UnitListCreateView, UnitDetailView,
    CategoryListCreateView, CategoryDetailView,
    VarietyListCreateView, VarietyDetailView,
    GoodsListCreateView, GoodsDetailView,
    StockInListCreateView,
    StockOutListCreateView,
    WarningListView, WarningReadView,
    ApprovalListView, ApprovalActionView,
    ImportExportView
)

urlpatterns = [
    # 单位管理
    path('units/', UnitListCreateView.as_view(), name='unit-list'),
    path('units/<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    
    # 品类管理
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # 品种管理
    path('varieties/', VarietyListCreateView.as_view(), name='variety-list'),
    path('varieties/<int:pk>/', VarietyDetailView.as_view(), name='variety-detail'),
    
    # 货物管理
    path('goods/', GoodsListCreateView.as_view(), name='goods-list'),
    path('goods/<int:pk>/', GoodsDetailView.as_view(), name='goods-detail'),
    
    # 入库管理
    path('stock-in/', StockInListCreateView.as_view(), name='stock-in-list'),
    
    # 出库管理
    path('stock-out/', StockOutListCreateView.as_view(), name='stock-out-list'),
    
    # 预警管理
    path('warnings/', WarningListView.as_view(), name='warning-list'),
    path('warnings/<int:pk>/read/', WarningReadView.as_view(), name='warning-read'),
    
    # 审批管理
    path('approvals/', ApprovalListView.as_view(), name='approval-list'),
    path('approvals/<int:pk>/', ApprovalActionView.as_view(), name='approval-action'),
    
    # 数据导入导出 (django-import-export)
    path('import-export/', ImportExportView.as_view(), name='import-export'),
]
