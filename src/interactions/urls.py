from django.urls import path
from . import views

urlpatterns = [
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
]