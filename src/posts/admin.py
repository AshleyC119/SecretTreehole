from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'view_count')
    list_filter = ('status', 'category', 'created_at', 'is_anonymous')
    search_fields = ('title', 'content', 'author__username')
    list_editable = ('status',)
    readonly_fields = ('view_count', 'like_count', 'comment_count', 'created_at', 'updated_at', 'published_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'content', 'excerpt', 'author', 'category')
        }),
        ('状态设置', {
            'fields': ('status', 'is_anonymous', 'allow_comments')
        }),
        ('统计信息', {
            'fields': ('view_count', 'like_count', 'comment_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )