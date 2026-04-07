"""
认证视图
"""
import logging
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.response import success_response, error_response
from apps.core.exceptions import AuthenticationException
from .models import User, OperationLog
from .serializers import LoginSerializer, UserSerializer, OperationLogSerializer
from .backends import generate_token
from .filters import OperationLogFilter

logger = logging.getLogger('apps')


class LoginView(APIView):
    """登录视图"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            first_error = list(errors.values())[0][0]
            return error_response(message=str(first_error))
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # 查找用户
        user = User.objects.filter(username=username).first()
        if not user:
            logger.warning(f"Login failed: user {username} not found")
            return error_response(message='用户名或密码错误', code=401)
        
        # 验证密码
        if not user.check_password(password):
            logger.warning(f"Login failed: wrong password for user {username}")
            return error_response(message='用户名或密码错误', code=401)
        
        # 检查用户状态
        if not user.is_active:
            logger.warning(f"Login failed: user {username} is disabled")
            return error_response(message='账号已被禁用', code=401)
        
        # 更新最后登录时间
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # 生成Token
        token = generate_token(user)
        
        logger.info(f"User {username} logged in successfully")
        
        return success_response(data={
            'token': token,
            'user': UserSerializer(user).data
        }, message='登录成功')


class LogoutView(APIView):
    """退出登录视图"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logger.info(f"User {request.user.username} logged out")
        return success_response(message='退出成功')


class UserInfoView(APIView):
    """获取当前用户信息"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return success_response(data=serializer.data)


class OperationLogListView(APIView):
    """操作日志列表 - 使用 django-filter"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = OperationLog.objects.all()
        
        # 使用 django-filter 进行筛选
        filterset = OperationLogFilter(request.query_params, queryset=queryset)
        queryset = filterset.qs
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = queryset.count()
        logs = queryset[start:end]
        
        serializer = OperationLogSerializer(logs, many=True)
        
        return success_response(data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
