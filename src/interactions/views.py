from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Comment, Like
from posts.models import Post


@login_required
@require_POST
def add_comment(request, post_id):
    """添加评论"""
    post = get_object_or_404(Post, id=post_id)

    if not post.allow_comments:
        messages.error(request, '该帖子已关闭评论')
        return redirect('post_detail', pk=post.id)

    content = request.POST.get('content', '').strip()

    if content:
        Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        # 更新评论数
        post.comment_count = Comment.objects.filter(post=post).count()
        post.save(update_fields=['comment_count'])
        messages.success(request, '评论发布成功！')

    return redirect('post_detail', pk=post.id)


@login_required
@require_POST
def delete_comment(request, comment_id):
    """删除评论"""
    comment = get_object_or_404(Comment, id=comment_id)

    # 只允许评论作者或帖子作者删除
    if request.user == comment.author or request.user == comment.post.author:
        post_id = comment.post.id
        comment.delete()

        # 更新评论数
        post = get_object_or_404(Post, id=post_id)
        post.comment_count = Comment.objects.filter(post=post).count()
        post.save(update_fields=['comment_count'])

        messages.success(request, '评论已删除')

    return redirect('post_detail', pk=comment.post.id)


@login_required
def like_post(request, post_id):
    """点赞/取消点赞帖子"""
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user,
        defaults={'like_type': 'like'}
    )

    if not created:
        # 如果已点赞，则取消点赞
        like.delete()
        liked = False
    else:
        liked = True

    # 更新点赞数
    post.like_count = Like.objects.filter(post=post).count()
    post.save(update_fields=['like_count'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX 请求返回 JSON
        return JsonResponse({
            'liked': liked,
            'like_count': post.like_count
        })

    return redirect('post_detail', pk=post.id)