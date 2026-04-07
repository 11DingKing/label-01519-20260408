"""
人员管理序列化器
"""
from rest_framework import serializers
from .models import AttendancePerson, StockOutPerson


class AttendancePersonSerializer(serializers.ModelSerializer):
    """考勤人员序列化器"""
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = AttendancePerson
        fields = ['id', 'name', 'employee_no', 'department', 'position',
                  'phone', 'avatar', 'avatar_url', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None


class StockOutPersonSerializer(serializers.ModelSerializer):
    """出库人员序列化器"""
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = StockOutPerson
        fields = ['id', 'name', 'employee_no', 'department', 'position',
                  'phone', 'avatar', 'avatar_url', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
