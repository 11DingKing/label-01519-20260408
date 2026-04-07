"""
人员管理视图
"""
import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.core.response import success_response, error_response, created_response, deleted_response
from apps.core.exceptions import NotFoundException
from .models import AttendancePerson, StockOutPerson
from .serializers import AttendancePersonSerializer, StockOutPersonSerializer

logger = logging.getLogger('apps')


# ==================== 考勤人员管理 ====================
class AttendancePersonListCreateView(APIView):
    """考勤人员列表和创建"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = AttendancePerson.objects.all()
        
        name = request.query_params.get('name')
        department = request.query_params.get('department')
        is_active = request.query_params.get('is_active')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if department:
            queryset = queryset.filter(department__icontains=department)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == 'true')
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = queryset.count()
        persons = queryset[start:end]
        
        serializer = AttendancePersonSerializer(persons, many=True)
        return success_response(data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    
    def post(self, request):
        serializer = AttendancePersonSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Attendance person created: {serializer.data['name']}")
        return created_response(data=serializer.data, message='考勤人员创建成功')


class AttendancePersonDetailView(APIView):
    """考勤人员详情、更新、删除"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return AttendancePerson.objects.get(pk=pk)
        except AttendancePerson.DoesNotExist:
            raise NotFoundException('考勤人员不存在')
    
    def get(self, request, pk):
        person = self.get_object(pk)
        serializer = AttendancePersonSerializer(person)
        return success_response(data=serializer.data)
    
    def put(self, request, pk):
        person = self.get_object(pk)
        serializer = AttendancePersonSerializer(person, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Attendance person updated: {person.name}")
        return success_response(data=serializer.data, message='考勤人员更新成功')
    
    def delete(self, request, pk):
        person = self.get_object(pk)
        person_name = person.name
        person.delete()
        logger.info(f"Attendance person deleted: {person_name}")
        return deleted_response(message='考勤人员删除成功')


# ==================== 出库人员管理 ====================
class StockOutPersonListCreateView(APIView):
    """出库人员列表和创建"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = StockOutPerson.objects.all()
        
        name = request.query_params.get('name')
        department = request.query_params.get('department')
        is_active = request.query_params.get('is_active')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if department:
            queryset = queryset.filter(department__icontains=department)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == 'true')
        
        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = queryset.count()
        persons = queryset[start:end]
        
        serializer = StockOutPersonSerializer(persons, many=True)
        return success_response(data={
            'list': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    
    def post(self, request):
        serializer = StockOutPersonSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Stock out person created: {serializer.data['name']}")
        return created_response(data=serializer.data, message='出库人员创建成功')


class StockOutPersonDetailView(APIView):
    """出库人员详情、更新、删除"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return StockOutPerson.objects.get(pk=pk)
        except StockOutPerson.DoesNotExist:
            raise NotFoundException('出库人员不存在')
    
    def get(self, request, pk):
        person = self.get_object(pk)
        serializer = StockOutPersonSerializer(person)
        return success_response(data=serializer.data)
    
    def put(self, request, pk):
        person = self.get_object(pk)
        serializer = StockOutPersonSerializer(person, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(message=list(serializer.errors.values())[0][0])
        
        serializer.save()
        logger.info(f"Stock out person updated: {person.name}")
        return success_response(data=serializer.data, message='出库人员更新成功')
    
    def delete(self, request, pk):
        person = self.get_object(pk)
        person_name = person.name
        person.delete()
        logger.info(f"Stock out person deleted: {person_name}")
        return deleted_response(message='出库人员删除成功')
