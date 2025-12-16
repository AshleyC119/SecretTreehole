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
 // 点赞功能（AJAX） - 修正版
$(document).on('click', '.like-btn', function(e) {
    e.preventDefault();

    // 获取按钮和数据
    const likeBtn = $(this);
    const postId = likeBtn.data('post-id');
    const likeUrl = `/interactions/like/${postId}/`;

    // 1. 获取 CSRF Token（标准方法）
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
    const csrftoken = getCookie('csrftoken');

    // 2. 发送 AJAX 请求（必须包含正确的 headers）
    $.ajax({
        url: likeUrl,
        type: 'POST',
        // 关键是下面这个 headers 配置
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest' // 明确告知Django这是AJAX请求
        },
        dataType: 'json', // 期待服务器返回JSON
        success: function(response) {
            // 更新按钮状态和计数
            if (response.liked) {
                likeBtn.addClass('liked');
                likeBtn.find('i').removeClass('far').addClass('fas');
            } else {
                likeBtn.removeClass('liked');
                likeBtn.find('i').removeClass('fas').addClass('far');
            }
            likeBtn.find('.like-count').text(response.like_count);
        },
        error: function(xhr, status, error) {
            console.error('点赞失败:', status, error);
            // 如果是因为未认证（401/403），刷新页面让用户重新登录
            if (xhr.status === 401 || xhr.status === 403) {
                alert('操作失败，请刷新页面或重新登录。');
                window.location.reload();
            }
        }
    });
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