from django.urls import path
from .views import RoleListCreate, RoleRetrieveUpdateDestroy

urlpatterns = [
    path('', RoleListCreate.as_view()),
    path('<int:pk>/', RoleRetrieveUpdateDestroy.as_view()),
]