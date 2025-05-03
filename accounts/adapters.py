from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        # Không cần làm gì nếu mô hình của bạn không sử dụng username
        return user
        
    def save_user(self, request, user, form, commit=True):
        # Overwrite này để tránh việc thiết lập username
        user = super().save_user(request, user, form, commit=False)
        # Thêm bất kỳ xử lý tùy chỉnh nào bạn cần
        if commit:
            user.save()
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        # Không thiết lập username
        email = data.get('email')
        if email:
            user.email = email
        # Thêm các trường khác nếu cần
        return user
        
    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        # Đảm bảo email là duy nhất
        if not user.email:
            user.email = f"user_{sociallogin.account.uid}@example.com"
        # Lưu người dùng
        user.save()
        sociallogin.save(request)
        return user