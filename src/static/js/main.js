// SecretTreehole 主 JavaScript 文件

$(document).ready(function() {
    // 初始化工具提示
    $('[data-bs-toggle="tooltip"]').tooltip();

    // 自动消失的提示框
    setTimeout(function() {
        $('.alert').fadeTo(500, 0).slideUp(500, function() {
            $(this).remove();
        });
    }, 5000);

    // 关闭提示框按钮
    $('.alert .btn-close').click(function() {
        $(this).closest('.alert').fadeOut();
    });

    // 表单提交加载状态
    $('form').submit(function() {
        const submitBtn = $(this).find('button[type="submit"]');
        if (submitBtn.length) {
            submitBtn.prop('disabled', true);
            submitBtn.html('<i class="fas fa-spinner fa-spin"></i> 处理中...');
        }
    });

    // 帖子图片懒加载
    $('.post-content img').each(function() {
        const img = $(this);
        const src = img.data('src') || img.attr('src');
        if (src) {
            img.attr('src', 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Crect width="100" height="100" fill="%23f0f0f0"/%3E%3C/svg%3E');
            img.data('original-src', src);

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const lazyImg = entry.target;
                        lazyImg.src = $(lazyImg).data('original-src');
                        observer.unobserve(lazyImg);
                    }
                });
            });

            observer.observe(this);
        }
    });

    // 点赞功能（AJAX）
    $('.like-btn').click(function(e) {
        e.preventDefault();
        const likeBtn = $(this);
        const postId = likeBtn.data('post-id');
        const likeUrl = `/interactions/like/${postId}/`;

        if (!likeBtn.hasClass('liked')) {
            // 立即更新UI，提供即时反馈
            likeBtn.addClass('liked');
            likeBtn.find('i').removeClass('far').addClass('fas');
            const likeCount = parseInt(likeBtn.find('.like-count').text()) + 1;
            likeBtn.find('.like-count').text(likeCount);

            // 发送AJAX请求
            $.ajax({
                url: likeUrl,
                type: 'POST',
                xhrFields: {
                    withCredentials: true
                },
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function(response) {
                    // AJAX请求成功，更新计数
                    likeBtn.find('.like-count').text(response.like_count);
                },
                error: function(xhr, status, error) {
                    // 如果未登录，重定向到登录页面
                    if (xhr.status === 403 || xhr.status === 401) {
                        window.location.href = '/accounts/login/?next=' + window.location.pathname;
                    } else {
                        // 其他错误，恢复UI状态
                        likeBtn.removeClass('liked');
                        likeBtn.find('i').removeClass('fas').addClass('far');
                        alert('点赞失败，请刷新页面重试');
                    }
                }
            });
        }
    });

    // 评论字数统计
    $('#commentContent').on('input', function() {
        const length = $(this).val().length;
        const counter = $(this).data('counter') || $('<small class="text-muted float-end">0/500</small>').insertAfter($(this));
        counter.text(`${length}/500`);

        if (length > 500) {
            counter.addClass('text-danger').removeClass('text-muted');
        } else {
            counter.removeClass('text-danger').addClass('text-muted');
        }
    });

    // 帖子内容预览（如果超过一定长度）
    $('.post-content-preview').each(function() {
        const content = $(this).text();
        if (content.length > 200) {
            $(this).text(content.substring(0, 200) + '...');
            $(this).after('<button class="btn btn-link btn-sm show-more-btn">显示全部</button>');
        }
    });

    // 显示全部内容
    $(document).on('click', '.show-more-btn', function() {
        const preview = $(this).prev('.post-content-preview');
        const fullContent = preview.data('full-content');
        if (fullContent) {
            preview.text(fullContent);
            $(this).text('收起').removeClass('show-more-btn').addClass('show-less-btn');
        }
    });

    // 获取CSRF token的辅助函数
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 页面加载动画
    $('main.container').addClass('animate-fade-in');

    // 监听页面可见性变化
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            // 页面重新获得焦点时，可以更新一些数据
            console.log('页面重新激活');
        }
    });
});

// 全局函数：格式化时间
function formatTimeAgo(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diffMs = now - time;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return '刚刚';
    if (diffMins < 60) return `${diffMins}分钟前`;
    if (diffHours < 24) return `${diffHours}小时前`;
    if (diffDays < 7) return `${diffDays}天前`;

    return time.toLocaleDateString();
}

// 初始化时间格式化
$(document).ready(function() {
    $('.time-ago').each(function() {
        const timestamp = $(this).data('timestamp');
        if (timestamp) {
            $(this).text(formatTimeAgo(timestamp));
        }
    });
});