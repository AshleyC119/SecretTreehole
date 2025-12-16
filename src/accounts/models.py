from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """自定义用户模型"""
    bio = models.TextField(max_length=500, blank=True, verbose_name="个人简介")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户管理"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username