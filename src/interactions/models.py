from django.db import models
from django.conf import settings
from posts.models import Post


class Comment(models.Model):
    """评论"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="所属帖子"
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="评论者"
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="父评论"
    )

    content = models.TextField(verbose_name="评论内容")
    is_hidden = models.BooleanField(default=False, verbose_name="隐藏")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论管理"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author} 的评论 ({self.post.title})"


class Like(models.Model):
    """点赞"""
    LIKE_TYPES = [
        ('like', '喜欢'),
        ('love', '爱心'),
        ('laugh', '大笑'),
        ('wow', '惊讶'),
        ('sad', '难过'),
        ('angry', '生气'),
    ]

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="被赞帖子"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="点赞用户"
    )

    like_type = models.CharField(
        max_length=10,
        choices=LIKE_TYPES,
        default='like',
        verbose_name="点赞类型"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="点赞时间")

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = "点赞管理"
        unique_together = ['post', 'user']  # 每个用户对每个帖子只能点一次赞

    def __str__(self):
        return f"{self.user} 对 {self.post.title} 点了{self.get_like_type_display()}"