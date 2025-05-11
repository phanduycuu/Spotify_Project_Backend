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
from django.shortcuts import get_object_or_404
from album.serializers import AlbumSerializer
from album_user.serializers import AlbumUserSerializer
from song.serializers import SongReadSerializer
from favourite_album.serializers import FavouriteAlbumUserSerializer
from favourite_song.serializers import FavouriteSongUserSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from role.models import Role
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.filter(is_deleted=False)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email','full_name']
    ordering_fields = ['email','full_name']
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

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({"error": "Tài khoản không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra nếu tài khoản đã bị xóa
        if user.is_deleted:
            return Response({"error": "Tài khoản đã bị khóa "}, status=status.HTTP_403_FORBIDDEN)

        # Kiểm tra mật khẩu
        if not user.check_password(password):
            return Response({"error": "Mật khẩu không đúng"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            # "user": AccountReadSerializer(user, context={'request': request}).data  # dùng serializer có album + favourite
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

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated], serializer_class=UpdateProfieSerializer)
    def update_profile(self, request):
        """API cập nhật thông tin cá nhân (full_name, sex, birthday) từ token"""
        user = request.user  # Lấy người dùng từ token đã xác thực
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
            channel_layer = get_channel_layer()
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
                    # Gửi realtime cho user2
                    async_to_sync(channel_layer.group_send)(
                        f"user_{user2.id}",
                        {
                            "type": "friend_update",
                            "action": "new_request",
                            "message": f"{user1.username} đã gửi lại lời mời kết bạn"
                        }
                    )
                    return Response({"message": "Lời mời kết bạn đã được gửi lại"}, status=status.HTTP_200_OK)

            # Nếu chưa có mối quan hệ nào
            Friend.objects.create(user1=user1, user2=user2, status="pending")
            async_to_sync(channel_layer.group_send)(
                f"user_{user2.id}",
                {
                    "type": "friend_update",
                    "action": "new_request",
                    "message": f"{user1.username} đã gửi lời mời kết bạn"
                }
            )
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
            channel_layer = get_channel_layer()
            if action == "accepted":
                friendship.status = "accepted"
                friendship.save()
                async_to_sync(channel_layer.group_send)(
                    f"user_{friendship.user1.id}",
                    {
                        "type": "friend_update",
                        "action": "request_accepted",
                        "message": f"{user2.username} đã chấp nhận lời mời kết bạn"
                    }
                )

                return Response({"message": "Đã chấp nhận lời mời kết bạn"}, status=status.HTTP_200_OK)

            elif action == "declined":
                friendship.status = "declined"
                friendship.save()
                async_to_sync(channel_layer.group_send)(
                    f"user_{friendship.user1.id}",
                    {
                        "type": "friend_update",
                        "action": "request_declined",
                        "message": f"{user2.username} đã từ chối lời mời kết bạn"
                    }
                )
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
    
    @action(detail=False, methods=['get'], url_path='get-favourite-albums/(?P<account_id>[^/.]+)')
    def get_favourite_albums(self, request, account_id=None):
        account = get_object_or_404(Account, pk=account_id, is_deleted=False)
        favourite_relations = account.account_favourite_albums.filter(is_deleted=False).select_related('album')
        serializer = FavouriteAlbumUserSerializer(favourite_relations, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get-albums/(?P<account_id>[^/.]+)')
    def get_albums(self, request, account_id=None):
        account = get_object_or_404(Account, pk=account_id, is_deleted=False)
        albums = account.account_albums.filter(is_deleted=False)  # 👈 sửa ở đây
        serializer = AlbumUserSerializer(albums, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get-favourite-songs/(?P<account_id>[^/.]+)')
    def get_favourite_songs(self, request, account_id=None):
        account = get_object_or_404(Account, pk=account_id, is_deleted=False)
        favourite_relations = account.account_favourite_songs.filter(is_deleted=False).select_related('song')
        serializer = FavouriteSongUserSerializer(favourite_relations, many=True, context={'request': request})
        return Response(
            serializer.data
       , status=status.HTTP_200_OK)
    

class AuthViewSet(viewsets.ViewSet):
    @action(methods=['post'], detail=False, url_path='google-login')
    def google_login(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token không được cung cấp'}, status=400)
            
        try:
            # Xác thực token với Google
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=10  # Allow some clock skew
            )
            
            # Kiểm tra issuer hợp lệ
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return Response({'error': 'Token không từ Google'}, status=400)
                
            # In thông tin gỡ lỗi (có thể xóa ở sản phẩm)
            print(f"Token hợp lệ. Dữ liệu người dùng: {idinfo}")
            
            email = idinfo.get('email')
            name = idinfo.get('name', '')  # Default empty string if name not provided
            
            # Kiểm tra email đã được xác minh chưa
            if not idinfo.get('email_verified', False):
                return Response({'error': 'Email chưa được xác minh'}, status=400)

            if not email:
                return Response({'error': 'Không lấy được email từ Google'}, status=400)

            try:
                # Tìm hoặc tạo người dùng
                default_role, _ = Role.objects.get_or_create(name='User')
                
                user, created = Account.objects.get_or_create(
                    email=email,
                    defaults={
                        'full_name': name,
                        'role': default_role,
                        'is_deleted': False
                    }
                )

                # Tạo JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    "user": AccountSerializer(user).data
                })
            except Exception as e:
                print(f"Database error: {str(e)}")
                return Response({'error': f'Lỗi khi xử lý tài khoản: {str(e)}'}, status=500)

        except ValueError as e:
            print(f"Token validation error: {str(e)}")
            return Response({'error': 'Token không hợp lệ hoặc hết hạn'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Response({'error': f'Lỗi xác thực: {str(e)}'}, status=500)
    

