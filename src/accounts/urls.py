from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # 个人资料 - 查看自己的
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # 查看其他用户的资料
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile_with_pk'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]