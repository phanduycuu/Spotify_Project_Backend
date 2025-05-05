from rest_framework import viewsets, status,filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account
from friend.models import Friend
from friend.serializers import FriendSerializer
from django.db import models
from .serializers import AccountSerializer,LoginSerializer,LogoutSerializer,UpdateProfieSerializer,AccountReadSerializer

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.filter(is_deleted=False)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email']
    ordering_fields = ['email']
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
        """API Đăng nhập bằng email và trả về JWT + thông tin tài khoản + album"""
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
            "user": AccountReadSerializer(user, context={'request': request}).data  # dùng serializer có album + favourite
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
    

    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def send_friend_request(self, request, pk=None):
        """API gửi lời mời kết bạn"""
        user1 = request.user
        try:
            user2 = Account.objects.get(pk=pk)
            if user1 == user2:
                return Response({"error": "Không thể kết bạn với chính mình"}, status=status.HTTP_400_BAD_REQUEST)

            # Kiểm tra tồn tại mối quan hệ bạn bè giữa 2 người, bất kể thứ tự user1-user2
            friendship = Friend.objects.filter(
                models.Q(user1=user1, user2=user2) | models.Q(user1=user2, user2=user1)
            ).first()

            if friendship:
                if friendship.status == "accepted":
                    return Response({"error": "Hai người đã là bạn bè"}, status=status.HTTP_400_BAD_REQUEST)
                elif friendship.status == "pending":
                    return Response({"error": "Lời mời kết bạn đang chờ xác nhận"}, status=status.HTTP_400_BAD_REQUEST)
                elif friendship.status == "declined":
                    # Cập nhật lại trạng thái
                    friendship.user1 = user1
                    friendship.user2 = user2
                    friendship.status = "pending"
                    friendship.save()
                    return Response({"message": "Lời mời kết bạn đã được gửi lại"}, status=status.HTTP_200_OK)

            # Nếu chưa có mối quan hệ nào
            Friend.objects.create(user1=user1, user2=user2, status="pending")
            return Response({"message": "Lời mời kết bạn đã được gửi"}, status=status.HTTP_201_CREATED)

        except Account.DoesNotExist:
            return Response({"error": "Người dùng không tồn tại"}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def respond_friend_request(self, request, pk=None):
        """API chấp nhận hoặc từ chối lời mời kết bạn"""
        user2 = request.user
        action = request.data.get("action")

        if action not in ["accepted", "declined"]:
            return Response({"error": "Hành động không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            friendship = Friend.objects.get(user1__id=pk, user2=user2, status="pending")

            if action == "accepted":
                friendship.status = "accepted"
                friendship.save()
                return Response({"message": "Đã chấp nhận lời mời kết bạn"}, status=status.HTTP_200_OK)

            elif action == "declined":
                friendship.status = "declined"
                friendship.save()
                return Response({"message": "Đã từ chối lời mời kết bạn"}, status=status.HTTP_200_OK)

        except friendship.DoesNotExist:
            return Response({"error": "Không tìm thấy lời mời kết bạn"}, status=status.HTTP_404_NOT_FOUND)





    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def friends(self, request):
        """API lấy danh sách bạn bè"""
        user = request.user
        friends = Account.objects.filter(
            models.Q(friends1__user2=user, friends1__status="accepted") | 
            models.Q(friends2__user1=user, friends2__status="accepted")
        )
        return Response(AccountSerializer(friends, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pending_requests(self, request):
        """API lấy danh sách lời mời kết bạn đang chờ"""
        user = request.user
        requests = Friend.objects.filter(user2=user, status="pending")
        return Response(FriendSerializer(requests, many=True).data, status=status.HTTP_200_OK)