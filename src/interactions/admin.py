from django.contrib import admin
from .models import Comment, Like


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'post', 'author', 'parent', 'created_at', 'is_hidden')
    list_filter = ('created_at', 'is_hidden')
    search_fields = ('content', 'post__title', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_hidden',)

    def truncated_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    truncated_content.short_description = '评论内容'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'get_like_type_display', 'created_at')
    list_filter = ('like_type', 'created_at')
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('created_at',)