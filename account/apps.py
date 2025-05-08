from django.apps import AppConfig
import os

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    path = os.path.dirname(os.path.abspath(__file__))  # Thêm dòng này
