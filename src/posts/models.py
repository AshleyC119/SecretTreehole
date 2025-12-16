from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """帖子分类"""
    name = models.CharField(max_length=100, verbose_name="分类名称")
    slug = models.SlugField(unique=True, verbose_name="URL标识", allow_unicode=True)  # 添加 allow_unicode=True
    description = models.TextField(blank=True, verbose_name="分类描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def save(self, *args, **kwargs):
        # 如果 slug 为空，自动从 name 生成
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类管理"

    def __str__(self):
        return self.name


class Post(models.Model):
    """帖子"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('hidden', '隐藏'),
    ]

    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="摘要")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="作者"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name="分类"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="状态"
    )

    is_anonymous = models.BooleanField(default=False, verbose_name="匿名发布")
    allow_comments = models.BooleanField(default=True, verbose_name="允许评论")

    view_count = models.PositiveIntegerField(default=0, verbose_name="浏览次数")
    like_count = models.PositiveIntegerField(default=0, verbose_name="点赞数")
    comment_count = models.PositiveIntegerField(default=0, verbose_name="评论数")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="发布时间")

    class Meta:
        verbose_name = "帖子"
        verbose_name_plural = "帖子管理"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)