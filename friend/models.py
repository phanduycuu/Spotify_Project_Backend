from django.db import models
from accounts.models import Account
# Create your models here.
class Friend(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang chờ'),
        ('accepted', 'Đã chấp nhận'),
        ('declined', 'Từ chối'),
    ]

    user1 = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friends1')
    user2 = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='friends2')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'friends'
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} - {self.user2} ({self.status})"