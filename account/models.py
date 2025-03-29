from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Tạo user với email thay vì username"""
        if not email:
            raise ValueError("Email là bắt buộc")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Tạo superuser với quyền admin"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Account(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    sex = models.CharField(
        max_length=10,
        choices=[('male', 'Nam'), ('female', 'Nữ'), ('other', 'Khác')],
        null=True,
        blank=True
    )
    birthday = models.DateField(null=True, blank=True)
    role = models.ForeignKey('role.Role', on_delete=models.CASCADE, related_name="role_accounts")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = None  # Xóa username
    USERNAME_FIELD = 'email'  # Đăng nhập bằng email
    REQUIRED_FIELDS = []  # Không yêu cầu trường nào khác khi tạo tài khoản

    objects = AccountManager()  # Sử dụng custom manager

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'accounts'
        verbose_name = "Tài khoản"
        verbose_name_plural = "Các tài khoản"
