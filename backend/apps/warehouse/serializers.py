"""
库房管理序列化器
"""
from rest_framework import serializers
from .models import Unit, Category, Variety, Goods, StockIn, StockOut, Warning, Approval


class UnitSerializer(serializers.ModelSerializer):
    """单位序列化器"""
    class Meta:
        model = Unit
        fields = ['id', 'name', 'symbol', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    """品类序列化器"""
    variety_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'code', 'description', 'is_active', 'variety_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_variety_count(self, obj):
        return obj.varieties.count()


class VarietySerializer(serializers.ModelSerializer):
    """品种序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    goods_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Variety
        fields = ['id', 'category', 'category_name', 'name', 'code', 
                  'description', 'is_active', 'goods_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_goods_count(self, obj):
        return obj.goods.count()


class GoodsSerializer(serializers.ModelSerializer):
    """货物序列化器"""
    variety_name = serializers.CharField(source='variety.name', read_only=True)
    category_name = serializers.CharField(source='variety.category.name', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    is_warning = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Goods
        fields = ['id', 'variety', 'variety_name', 'category_name', 'unit', 'unit_name',
                  'name', 'code', 'specification', 'quantity', 'warning_threshold',
                  'location', 'remark', 'is_active', 'is_warning', 'created_at']
        read_only_fields = ['id', 'quantity', 'created_at']


class GoodsCreateSerializer(serializers.ModelSerializer):
    """货物创建序列化器"""
    class Meta:
        model = Goods
        fields = ['variety', 'unit', 'name', 'code', 'specification',
                  'warning_threshold', 'location', 'remark']
    
    def validate_code(self, value):
        if Goods.objects.filter(code=value).exists():
            raise serializers.ValidationError('货物编码已存在')
        return value


class StockInSerializer(serializers.ModelSerializer):
    """入库记录序列化器"""
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    goods_code = serializers.CharField(source='goods.code', read_only=True)
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    unit_name = serializers.CharField(source='goods.unit.name', read_only=True)
    
    class Meta:
        model = StockIn
        fields = ['id', 'goods', 'goods_name', 'goods_code', 'unit_name',
                  'operator', 'operator_name', 'quantity', 'batch_no',
                  'supplier', 'stock_in_time', 'remark']
        read_only_fields = ['id', 'operator', 'stock_in_time']


class StockInCreateSerializer(serializers.ModelSerializer):
    """入库创建序列化器"""
    class Meta:
        model = StockIn
        fields = ['goods', 'quantity', 'batch_no', 'supplier', 'remark']
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('入库数量必须大于0')
        return value


class StockOutSerializer(serializers.ModelSerializer):
    """出库记录序列化器"""
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    goods_code = serializers.CharField(source='goods.code', read_only=True)
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    unit_name = serializers.CharField(source='goods.unit.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = StockOut
        fields = ['id', 'goods', 'goods_name', 'goods_code', 'unit_name',
                  'operator', 'operator_name', 'receiver', 'receiver_dept',
                  'quantity', 'status', 'status_display', 'stock_out_time',
                  'remark', 'created_at']
        read_only_fields = ['id', 'operator', 'status', 'stock_out_time', 'created_at']


class StockOutCreateSerializer(serializers.ModelSerializer):
    """出库创建序列化器"""
    class Meta:
        model = StockOut
        fields = ['goods', 'receiver', 'receiver_dept', 'quantity', 'remark']
    
    def validate(self, data):
        goods = data['goods']
        quantity = data['quantity']
        
        if quantity <= 0:
            raise serializers.ValidationError({'quantity': '出库数量必须大于0'})
        
        if quantity > goods.quantity:
            raise serializers.ValidationError({'quantity': f'出库数量不能超过库存数量({goods.quantity})'})
        
        return data


class WarningSerializer(serializers.ModelSerializer):
    """预警序列化器"""
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    goods_code = serializers.CharField(source='goods.code', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    current_quantity = serializers.DecimalField(source='goods.quantity', 
                                                 max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Warning
        fields = ['id', 'goods', 'goods_name', 'goods_code', 'type', 
                  'type_display', 'message', 'current_quantity', 'is_read', 'created_at']
        read_only_fields = ['id', 'goods', 'type', 'message', 'created_at']


class ApprovalSerializer(serializers.ModelSerializer):
    """审批序列化器"""
    stock_out_info = StockOutSerializer(source='stock_out', read_only=True)
    approver_name = serializers.CharField(source='approver.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Approval
        fields = ['id', 'stock_out', 'stock_out_info', 'approver', 'approver_name',
                  'status', 'status_display', 'remark', 'created_at', 'updated_at']
        read_only_fields = ['id', 'stock_out', 'approver', 'created_at', 'updated_at']
