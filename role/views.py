from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Role
from .serializers import RoleSerializer

class RoleListCreate(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer