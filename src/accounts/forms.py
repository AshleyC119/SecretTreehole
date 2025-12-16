from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 添加表单字段的帮助文本
        self.fields['username'].help_text = '3-15个字符，只能包含字母、数字和下划线'
        self.fields['password1'].help_text = '至少8个字符，不能全是数字'
        self.fields['password2'].help_text = '再次输入密码以确认'


class CustomUserChangeForm(UserChangeForm):
    password = None  # 不在编辑表单中显示密码字段

    class Meta:
        model = CustomUser
        fields = ('email', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }