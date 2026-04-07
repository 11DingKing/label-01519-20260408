"""
人员管理模型
"""
from django.db import models
from PIL import Image
import os


def avatar_upload_path(instance, filename):
    """头像上传路径"""
    ext = filename.split('.')[-1]
    return f'avatars/{instance.employee_no}.{ext}'


class AttendancePerson(models.Model):
    """考勤人员模型"""
    name = models.CharField('姓名', max_length=50)
    employee_no = models.CharField('工号', max_length=50, unique=True)
    department = models.CharField('部门', max_length=100)
    position = models.CharField('职位', max_length=100, blank=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    avatar = models.ImageField('头像', upload_to=avatar_upload_path, blank=True, null=True)
    is_active = models.BooleanField('是否在职', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'pm_attendance_person'
        verbose_name = '考勤人员'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.employee_no})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 使用Pillow处理头像图片
        if self.avatar:
            self._process_avatar()
    
    def _process_avatar(self):
        """使用Pillow处理头像图片 - 压缩和调整尺寸"""
        try:
            img = Image.open(self.avatar.path)
            
            # 转换为RGB模式（处理PNG透明背景）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 调整尺寸为200x200
            max_size = (200, 200)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存压缩后的图片
            img.save(self.avatar.path, 'JPEG', quality=85, optimize=True)
        except Exception:
            pass  # 图片处理失败不影响保存


class StockOutPerson(models.Model):
    """出库人员模型"""
    name = models.CharField('姓名', max_length=50)
    employee_no = models.CharField('工号', max_length=50, unique=True)
    department = models.CharField('部门', max_length=100)
    position = models.CharField('职位', max_length=100, blank=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    avatar = models.ImageField('头像', upload_to=avatar_upload_path, blank=True, null=True)
    is_active = models.BooleanField('是否在职', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'pm_stock_out_person'
        verbose_name = '出库人员'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.employee_no})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 使用Pillow处理头像图片
        if self.avatar:
            self._process_avatar()
    
    def _process_avatar(self):
        """使用Pillow处理头像图片 - 压缩和调整尺寸"""
        try:
            img = Image.open(self.avatar.path)
            
            # 转换为RGB模式
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 调整尺寸为200x200
            max_size = (200, 200)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存压缩后的图片
            img.save(self.avatar.path, 'JPEG', quality=85, optimize=True)
        except Exception:
            pass
