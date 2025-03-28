from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Account(AbstractUser):
    role = models.ForeignKey('role.Role', on_delete=models.CASCADE, related_name="role_accounts")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'  


    def __str__(self):
        return self.username

    class Meta:
      db_table = 'accounts'
      verbose_name = "Tài khoản"
      verbose_name_plural = "Các tài khoản"