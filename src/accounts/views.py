from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView  # 移除 CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


def home_view(request):
    """首页"""
    # 在函数内部导入，避免循环导入问题
    from posts.models import Post, Category
    from interactions.models import Comment, Like

    # 获取热门帖子（按点赞数排序，取前5个）
    hot_posts = Post.objects.filter(status='published').order_by('-like_count', '-created_at')[:5]

    # 获取总点赞数
    total_likes = Like.objects.count()

    context = {
        'posts': Post.objects.filter(status='published').order_by('-created_at')[:5],
        'categories': Category.objects.all()[:8],
        'post_count': Post.objects.filter(status='published').count(),
        'user_count': CustomUser.objects.count(),
        'comment_count': Comment.objects.count(),
        'hot_posts': hot_posts,  # 热门帖子
        'total_likes': total_likes,  # 总点赞数
    }
    return render(request, 'home.html', context)


def register_view(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！欢迎来到SecretTreehole！')
            return redirect('home')
        else:
            messages.error(request, '注册失败，请检查表单信息。')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """用户登录视图"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('home')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """用户登出视图"""
    logout(request)
    messages.success(request, '已成功退出登录')
    return redirect('home')


class ProfileView(LoginRequiredMixin, DetailView):
    """用户资料页面"""
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        # 如果有pk参数，查看指定用户；否则查看当前用户
        if 'pk' in self.kwargs:
            return super().get_object(queryset)
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()

        # 在函数内部导入以避免循环导入
        from posts.models import Post
        from interactions.models import Comment, Like

        context['posts_count'] = Post.objects.filter(author=profile_user, status='published').count()
        context['comments_count'] = Comment.objects.filter(author=profile_user).count()
        context['likes_count'] = Like.objects.filter(user=profile_user).count()
        context['user_posts'] = Post.objects.filter(
            author=profile_user,
            status='published'
        ).order_by('-created_at')[:5]

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """更新用户资料"""
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, '个人资料已更新！')
        return super().form_valid(form)