"""
认证序列化器
"""
from rest_framework import serializers
from .models import User, OperationLog


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(max_length=50, required=True, error_messages={
        'required': '用户名不能为空',
        'max_length': '用户名长度不能超过50个字符'
    })
    password = serializers.CharField(max_length=128, required=True, write_only=True, error_messages={
        'required': '密码不能为空'
    })


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'role', 'role_display', 
                  'phone', 'email', 'is_active', 'created_at', 'last_login']
        read_only_fields = ['id', 'created_at', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, min_length=6, error_messages={
        'min_length': '密码长度不能少于6个字符'
    })
    
    class Meta:
        model = User
        fields = ['username', 'password', 'real_name', 'role', 'phone', 'email']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = OperationLog
        fields = ['id', 'username', 'action', 'action_display', 'module', 
                  'detail', 'ip_address', 'created_at']
