from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account
from .serializers import AccountSerializer,LoginSerializer,LogoutSerializer,UpdateProfieSerializer

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """API Đăng ký người dùng với quyền"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": AccountSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], serializer_class=LoginSerializer)
    def login(self, request):
        """API Đăng nhập bằng email và trả về JWT"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"error": "Sai email hoặc mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": AccountSerializer(user).data
        }, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], serializer_class=LogoutSerializer)
    def logout(self, request):
        """API Logout bằng cách đưa Refresh Token vào blacklist"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data['refresh']  # Lấy refresh token từ serializer
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['put'], permission_classes=[AllowAny],serializer_class=LoginSerializer)
    def update_password(self, request, pk=None):
        """API cập nhật mật khẩu"""
        user = self.get_object()
        password = request.data.get("password")
        if not password:
            return Response({"error": "Vui lòng nhập mật khẩu mới"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({"message": "Cập nhật mật khẩu thành công"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'], permission_classes=[AllowAny],serializer_class=UpdateProfieSerializer)
    def update_profile(self, request, pk=None):
        """API cập nhật thông tin cá nhân (full_name, sex, birthday)"""
        user = self.get_object()
        data = request.data

        user.full_name = data.get("full_name", user.full_name)
        user.sex = data.get("sex", user.sex)
        user.birthday = data.get("birthday", user.birthday)
        user.save()

        return Response({"message": "Cập nhật thông tin cá nhân thành công", "user": AccountSerializer(user).data}, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """API Lấy thông tin user hiện tại"""
        return Response(AccountSerializer(request.user).data)