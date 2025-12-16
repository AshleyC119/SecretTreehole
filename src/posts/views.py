from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Q
from .models import Post, Category



class PostListView(ListView):
    """帖子列表页"""
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').order_by('-created_at')

        # 按分类筛选
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        # 搜索功能
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-created_at')[:5]
        return context


class PostDetailView(DetailView):
    """帖子详情页"""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 增加浏览量
        self.object.view_count += 1
        self.object.save(update_fields=['view_count'])

        # 在函数内部导入
        from interactions.models import Comment, Like

        # 获取相关帖子
        if self.object.category:
            context['related_posts'] = Post.objects.filter(
                category=self.object.category,
                status='published'
            ).exclude(id=self.object.id)[:4]
        else:
            context['related_posts'] = Post.objects.filter(status='published').exclude(id=self.object.id)[:4]

        # 获取评论
        context['comments'] = Comment.objects.filter(
            post=self.object
        ).order_by('created_at')

        # 检查当前用户是否点赞
        if self.request.user.is_authenticated:
            context['user_liked'] = Like.objects.filter(
                post=self.object,
                user=self.request.user
            ).exists()
        else:
            context['user_liked'] = False

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """创建新帖子"""
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'content', 'category', 'is_anonymous', 'allow_comments']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'published'
        messages.success(self.request, '帖子发布成功！')
        return super().form_valid(form)

    # 添加 success_url 属性
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """更新帖子"""
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'content', 'category', 'status', 'is_anonymous', 'allow_comments']

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, '帖子更新成功！')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """删除帖子"""
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, '帖子已删除！')
        return super().delete(request, *args, **kwargs)


@login_required
def statistics_view(request):
    """数据统计页面（仅限管理员）"""
    if not request.user.is_staff:
        from django.contrib import messages
        messages.error(request, '您没有权限访问此页面')
        return redirect('home')

    # 获取最近30天的数据
    thirty_days_ago = now() - timedelta(days=30)

    # 帖子统计
    total_posts = Post.objects.count()
    published_posts = Post.objects.filter(status='published').count()
    draft_posts = Post.objects.filter(status='draft').count()
    anonymous_posts = Post.objects.filter(is_anonymous=True).count()

    # 每日发帖趋势（最近30天）
    daily_posts = Post.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(
        select={'day': "date(created_at)"}
    ).values('day').annotate(count=Count('id')).order_by('day')

    # 分类统计
    category_stats = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).order_by('-post_count')[:10]

    # 用户发帖排名
    from accounts.models import CustomUser
    user_post_stats = CustomUser.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='published'))
    ).filter(post_count__gt=0).order_by('-post_count')[:10]

    context = {
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'anonymous_posts': anonymous_posts,
        'daily_posts': daily_posts,
        'category_stats': category_stats,
        'user_post_stats': user_post_stats,
    }

    return render(request, 'posts/statistics.html', context)