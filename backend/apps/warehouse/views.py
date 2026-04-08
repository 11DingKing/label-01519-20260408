"""
库房管理视图
"""
import logging
from django.utils import timezone
from django.db import transaction, models
from django.db.models import Sum, Count, Q, F
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.response import success_response, error_response, created_response, deleted_response
from apps.core.exceptions import NotFoundException, BusinessException
from .models import Unit, Category, Variety, Goods, StockIn, StockOut, Warning, Approval
from .serializers import (
    UnitSerializer, CategorySerializer, VarietySerializer,
    GoodsSerializer, GoodsCreateSerializer,
    StockInSerializer, StockInCreateSerializer,
    StockOutSerializer, StockOutCreateSerializer,
    WarningSerializer, ApprovalSerializer
)
from .resources import (
    UnitResource, CategoryResource, VarietyResource, 
    GoodsResource, StockInResource, StockOutResource
)
from .filters import (
    UnitFilter, CategoryFilter, VarietyFilter, GoodsFilter,
    StockInFilter, StockOutFilter, WarningFilter, ApprovalFilter
)

logger = logging.getLogger('apps')


# ==================== 单位管理 ====================
class UnitListCreateView(APIView):
    """单位列表和创建 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Unit.objects.all()
        
        # 使用 django-filter 进行筛选
        filterset = UnitFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        serializer = UnitSerializer(queryset, many=True)
        return success_response(data=serializer.data)
    
    def post(self, request):
        serializer = UnitSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Unit created: {serializer.data['name']}")
        return created_response(data=serializer.data, message='单位创建成功')


class UnitDetailView(APIView):
    """单位详情、更新、删除"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            raise NotFoundException('单位不存在')
    
    def get(self, request, pk):
        unit = self.get_object(pk)
        serializer = UnitSerializer(unit)
        return success_response(data=serializer.data)
    
    def put(self, request, pk):
        unit = self.get_object(pk)
        serializer = UnitSerializer(unit, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Unit updated: {unit.name}")
        return success_response(data=serializer.data, message='单位更新成功')
    
    def delete(self, request, pk):
        unit = self.get_object(pk)
        
        # 检查是否有关联货物
        if Goods.objects.filter(unit=unit).exists():
            return error_response(message='该单位下存在货物，无法删除')
        
        unit_name = unit.name
        unit.delete()
        logger.info(f"Unit deleted: {unit_name}")
        return deleted_response(message='单位删除成功')


# ==================== 品类管理 ====================
class CategoryListCreateView(APIView):
    """品类列表和创建 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Category.objects.all()
        
        # 使用 django-filter 进行筛选
        filterset = CategoryFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        serializer = CategorySerializer(queryset, many=True)
        return success_response(data=serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Category created: {serializer.data['name']}")
        return created_response(data=serializer.data, message='品类创建成功')


class CategoryDetailView(APIView):
    """品类详情、更新、删除"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFoundException('品类不存在')
    
    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return success_response(data=serializer.data)
    
    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Category updated: {category.name}")
        return success_response(data=serializer.data, message='品类更新成功')
    
    def delete(self, request, pk):
        category = self.get_object(pk)
        
        if category.varieties.exists():
            return error_response(message='该品类下存在品种，无法删除')
        
        category_name = category.name
        category.delete()
        logger.info(f"Category deleted: {category_name}")
        return deleted_response(message='品类删除成功')


# ==================== 品种管理 ====================
class VarietyListCreateView(APIView):
    """品种列表和创建 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Variety.objects.select_related('category').all()
        
        # 使用 django-filter 进行筛选
        filterset = VarietyFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        serializer = VarietySerializer(queryset, many=True)
        return success_response(data=serializer.data)
    
    def post(self, request):
        serializer = VarietySerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Variety created: {serializer.data['name']}")
        return created_response(data=serializer.data, message='品种创建成功')


class VarietyDetailView(APIView):
    """品种详情、更新、删除"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Variety.objects.select_related('category').get(pk=pk)
        except Variety.DoesNotExist:
            raise NotFoundException('品种不存在')
    
    def get(self, request, pk):
        variety = self.get_object(pk)
        serializer = VarietySerializer(variety)
        return success_response(data=serializer.data)
    
    def put(self, request, pk):
        variety = self.get_object(pk)
        serializer = VarietySerializer(variety, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Variety updated: {variety.name}")
        return success_response(data=serializer.data, message='品种更新成功')
    
    def delete(self, request, pk):
        variety = self.get_object(pk)
        
        if variety.goods.exists():
            return error_response(message='该品种下存在货物，无法删除')
        
        variety_name = variety.name
        variety.delete()
        logger.info(f"Variety deleted: {variety_name}")
        return deleted_response(message='品种删除成功')


# ==================== 货物管理 ====================
class GoodsListCreateView(APIView):
    """货物列表和创建 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Goods.objects.select_related('variety', 'variety__category', 'unit').all()
        
        # 使用 django-filter 进行筛选
        filterset = GoodsFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = queryset.count()
        goods_list = queryset[start:end]
        
        serializer = GoodsSerializer(goods_list, many=True)
        return success_response(data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    
    def post(self, request):
        serializer = GoodsCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        goods = serializer.save()
        logger.info(f"Goods created: {goods.name}")
        return created_response(data=GoodsSerializer(goods).data, message='货物创建成功')


class GoodsDetailView(APIView):
    """货物详情、更新、删除"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Goods.objects.select_related('variety', 'variety__category', 'unit').get(pk=pk)
        except Goods.DoesNotExist:
            raise NotFoundException('货物不存在')
    
    def get(self, request, pk):
        goods = self.get_object(pk)
        serializer = GoodsSerializer(goods)
        return success_response(data=serializer.data)
    
    def put(self, request, pk):
        goods = self.get_object(pk)
        serializer = GoodsCreateSerializer(goods, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Goods updated: {goods.name}")
        return success_response(data=GoodsSerializer(goods).data, message='货物更新成功')
    
    def delete(self, request, pk):
        goods = self.get_object(pk)
        
        if goods.quantity > 0:
            return error_response(message='该货物还有库存，无法删除')
        
        goods_name = goods.name
        goods.delete()
        logger.info(f"Goods deleted: {goods_name}")
        return deleted_response(message='货物删除成功')


# ==================== 入库管理 ====================
class StockInListCreateView(APIView):
    """入库记录列表和创建 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = StockIn.objects.select_related('goods', 'goods__unit', 'operator').all()
        
        # 使用 django-filter 进行筛选
        filterset = StockInFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = queryset.count()
        stock_ins = queryset[start:end]
        
        serializer = StockInSerializer(stock_ins, many=True)
        return success_response(data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    
    @transaction.atomic
    def post(self, request):
        serializer = StockInCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        stock_in = serializer.save(operator=request.user)
        
        # 更新库存
        goods = stock_in.goods
        goods.quantity += stock_in.quantity
        goods.save(update_fields=['quantity', 'updated_at'])
        
        logger.info(f"Stock in: {goods.name}, quantity: {stock_in.quantity}")
        return created_response(data=StockInSerializer(stock_in).data, message='入库成功')


# ==================== 出库管理 ====================
class StockOutListCreateView(APIView):
    """出库记录列表和创建 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = StockOut.objects.select_related('goods', 'goods__unit', 'operator').all()
        
        # 使用 django-filter 进行筛选
        filterset = StockOutFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = queryset.count()
        stock_outs = queryset[start:end]
        
        serializer = StockOutSerializer(stock_outs, many=True)
        return success_response(data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    
    @transaction.atomic
    def post(self, request):
        serializer = StockOutCreateSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            if isinstance(errors, dict):
                first_error = list(errors.values())[0]
                if isinstance(first_error, list):
                    first_error = first_error[0]
            else:
                first_error = str(errors)
            return error_response(message=str(first_error))
        
        stock_out = serializer.save(operator=request.user)
        
        # 创建审批记录
        Approval.objects.create(stock_out=stock_out)
        
        logger.info(f"Stock out request: {stock_out.goods.name}, quantity: {stock_out.quantity}")
        return created_response(data=StockOutSerializer(stock_out).data, message='出库申请已提交')


# ==================== 预警管理 ====================
class WarningListView(APIView):
    """预警列表 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Warning.objects.select_related('goods').all()
        
        # 使用 django-filter 进行筛选
        filterset = WarningFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        serializer = WarningSerializer(queryset, many=True)
        return success_response(data=serializer.data)


class WarningReadView(APIView):
    """标记预警已读"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        try:
            warning = Warning.objects.get(pk=pk)
        except Warning.DoesNotExist:
            raise NotFoundException('预警记录不存在')
        
        warning.is_read = True
        warning.save(update_fields=['is_read'])
        
        logger.info(f"Warning marked as read: {warning.id}")
        return success_response(message='已标记为已读')


class WarningManualCheckView(APIView):
    """手动触发库存预警检查"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            from apps.reports.cron import check_stock_warning
            
            logger.info(f"用户 {request.user.username} 手动触发库存预警检查")
            
            result = check_stock_warning()
            
            logger.info(f"手动库存预警检查完成: 新增 {result['new_warnings_count']} 条预警")
            
            return success_response(
                data=result,
                message=f'库存预警检查完成，共发现 {result["total_warning_goods"]} 个预警货物，新增 {result["new_warnings_count"]} 条预警记录'
            )
        except Exception as e:
            logger.error(f"手动触发库存预警检查失败: {str(e)}")
            return error_response(message=f'检查失败: {str(e)}')


# ==================== 审批管理 ====================
class ApprovalListView(APIView):
    """审批列表 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Approval.objects.select_related(
            'stock_out', 'stock_out__goods', 'stock_out__operator', 'approver'
        ).all()
        
        # 使用 django-filter 进行筛选
        filterset = ApprovalFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = queryset.count()
        approvals = queryset[start:end]
        
        serializer = ApprovalSerializer(approvals, many=True)
        return success_response(data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })


class ApprovalActionView(APIView):
    """审批操作"""
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def put(self, request, pk):
        try:
            approval = Approval.objects.select_related('stock_out', 'stock_out__goods').get(pk=pk)
        except Approval.DoesNotExist:
            raise NotFoundException('审批记录不存在')
        
        if approval.status != 'pending':
            return error_response(message='该审批已处理')
        
        action = request.data.get('action')  # approve or reject
        remark = request.data.get('remark', '')
        
        if action not in ['approve', 'reject']:
            return error_response(message='无效的操作')
        
        stock_out = approval.stock_out
        
        if action == 'approve':
            # 检查库存
            if stock_out.quantity > stock_out.goods.quantity:
                return error_response(message='库存不足，无法审批通过')
            
            # 扣减库存
            stock_out.goods.quantity -= stock_out.quantity
            stock_out.goods.save(update_fields=['quantity', 'updated_at'])
            
            # 更新出库记录状态
            stock_out.status = 'completed'
            stock_out.stock_out_time = timezone.now()
            stock_out.save(update_fields=['status', 'stock_out_time'])
            
            # 检查是否需要生成预警
            if stock_out.goods.is_warning:
                Warning.objects.create(
                    goods=stock_out.goods,
                    type='low_stock',
                    message=f'货物 {stock_out.goods.name} 库存不足，当前库存: {stock_out.goods.quantity}'
                )
            
            approval.status = 'approved'
            message = '审批通过'
        else:
            stock_out.status = 'rejected'
            stock_out.save(update_fields=['status'])
            approval.status = 'rejected'
            message = '审批拒绝'
        
        approval.approver = request.user
        approval.remark = remark
        approval.save()
        
        logger.info(f"Approval {action}: {approval.id}")
        return success_response(data=ApprovalSerializer(approval).data, message=message)


# ==================== 数据导入导出 (使用django-import-export) ====================
class ImportExportView(APIView):
    """数据导入导出视图 - 使用django-import-export"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    
    RESOURCE_MAP = {
        'units': UnitResource,
        'categories': CategoryResource,
        'varieties': VarietyResource,
        'goods': GoodsResource,
        'stock_in': StockInResource,
        'stock_out': StockOutResource,
    }
    
    def get(self, request):
        """导出数据"""
        data_type = request.query_params.get('type', 'goods')
        file_format = request.query_params.get('format', 'xlsx')
        
        if data_type not in self.RESOURCE_MAP:
            return error_response(message='无效的数据类型')
        
        resource_class = self.RESOURCE_MAP[data_type]
        resource = resource_class()
        
        # 获取数据集
        dataset = resource.export()
        
        # 根据格式导出
        if file_format == 'xlsx':
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            content = dataset.xlsx
        elif file_format == 'csv':
            content_type = 'text/csv'
            content = dataset.csv.encode('utf-8-sig')
        elif file_format == 'json':
            content_type = 'application/json'
            content = dataset.json.encode('utf-8')
        else:
            return error_response(message='不支持的导出格式')
        
        response = HttpResponse(content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{data_type}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{file_format}"'
        
        logger.info(f"Data exported via import-export: {data_type}, format: {file_format}")
        return response
    
    def post(self, request):
        """导入数据"""
        data_type = request.data.get('type', 'goods')
        file = request.FILES.get('file')
        
        if not file:
            return error_response(message='请上传文件')
        
        if data_type not in self.RESOURCE_MAP:
            return error_response(message='无效的数据类型')
        
        resource_class = self.RESOURCE_MAP[data_type]
        resource = resource_class()
        
        try:
            # 读取文件
            from tablib import Dataset
            dataset = Dataset()
            
            file_ext = file.name.split('.')[-1].lower()
            if file_ext == 'xlsx':
                dataset.load(file.read(), format='xlsx')
            elif file_ext == 'csv':
                dataset.load(file.read().decode('utf-8-sig'), format='csv')
            elif file_ext == 'json':
                dataset.load(file.read().decode('utf-8'), format='json')
            else:
                return error_response(message='不支持的文件格式，请使用xlsx、csv或json')
            
            # 预览导入结果
            result = resource.import_data(dataset, dry_run=True)
            
            if result.has_errors():
                errors = []
                for row_errors in result.row_errors():
                    row_num, row_error_list = row_errors
                    for err in row_error_list:
                        errors.append(f"第{row_num}行: {str(err.error)}")
                return error_response(message=f"导入失败: {'; '.join(errors[:5])}")
            
            # 正式导入
            result = resource.import_data(dataset, dry_run=False)
            
            logger.info(f"Data imported via import-export: {data_type}, rows: {result.total_rows}")
            return success_response(
                data={
                    'total_rows': result.total_rows,
                    'imported': result.totals.get('new', 0) + result.totals.get('update', 0),
                    'skipped': result.totals.get('skip', 0)
                },
                message=f'导入成功，共处理 {result.total_rows} 条数据'
            )
            
        except Exception as e:
            logger.error(f"Import error: {str(e)}")
            return error_response(message=f'导入失败: {str(e)}')
