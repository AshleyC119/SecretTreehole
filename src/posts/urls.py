from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('category/<str:category_slug>/', views.PostListView.as_view(), name='post_list_by_category'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('new/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('statistics/', views.statistics_view, name='statistics'),  # 添加统计页面
]