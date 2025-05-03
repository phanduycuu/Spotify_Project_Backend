from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from .models import Account
from role.models import Role

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Lưu User với các thông tin mở rộng từ form
        """
        user = super().save_user(request, user, form, False)
        
        # Thiết lập vai trò mặc định (thay 'default_role_id' bằng ID của vai trò mặc định)
        default_role = Role.objects.get(id=1)  # Lấy vai trò mặc định, điều chỉnh logic này
        user.role = default_role
        
        if commit:
            user.save()
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Xử lý lưu user khi đăng nhập bằng tài khoản xã hội
        """
        user = super().save_user(request, sociallogin, form)
        
        # Trích xuất thông tin từ tài khoản Google
        social_data = sociallogin.account.extra_data
        
        # Cập nhật thông tin cá nhân
        if 'name' in social_data:
            user.full_name = social_data.get('name', '')
        
        # Thiết lập vai trò mặc định
        default_role = Role.objects.get(id=1)  # Lấy vai trò mặc định, điều chỉnh logic này
        user.role = default_role
        
        user.save()
        return user