# 🎧 Spotify Clone - Backend

## Hướng dẫn cài đặt

### 🚀 Công nghệ sử dụng

- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL
- Django CORS Headers
- JWT (Xác thực người dùng)

---

### 📁 Cấu trúc thư mục chính

```bash
Spotify_Project_Backend/
├── Spotify_Project_Backend/                         # Cấu hình Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                            # Tất cả app được gom tại đây
│   ├── accounts/                    # Xử lý đăng nhập, đăng ký, quyền
│   ├── users/                       # Thông tin người dùng (trước là account, album_user)
│   ├── music/                       # Các app về bài hát và album
│   │   ├── album/
│   │   ├── album_song/
│   │   ├── album_user/
│   │   ├── song/
│   │   ├── singer/
│   │   ├── artist/
│   │   ├── songClient/
│   │   ├── favourite_album/
│   │   └── favourite_song/
│   ├── chat/                        # Giao tiếp giữa người dùng
│   ├── video/                       # Truyền thông video
│   ├── friend/                      # Danh sách bạn bè
│   ├── role/                        # Phân quyền
│
├── media/                           # Upload file
├── venv/                            # Virtual environment
│
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
└── api.http                         # File test API


```

---

### ⚙️ Thiết lập môi trường

1. Truy cập thư mục `Spotify_Project_Backend`:

```bash
cd Spotify_Project_Backend
```

2. Tạo và kích hoạt môi trường ảo:

**Trên Linux/macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

**Trên Windows:**

```bash
python -m venv venv
source venv/Scripts/activate
```

3. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

4. Chạy migrate để tạo database:

```bash
python manage.py migrate
```

---

### ▶️ Khởi chạy server

```bash
python -m daphne -b 127.0.0.1 -p 8000 Spotify_Project_Backend.asgi:application
```

Mặc định backend sẽ chạy tại: [http://localhost:8000](http://localhost:8000)

---

### 📌 Tính năng chính

- Quản lý người dùng: đăng ký, đăng nhập
- CRUD ca sĩ, bài hát, video, album
- Phát nhạc và video qua API
- API dành riêng cho frontend và admin
- Cơ chế phân quyền truy cập (nếu có)
- Xử lý media: tải ảnh, video
- Tối ưu cho RESTful API

---

### 📡 Đường dẫn API mẫu

- `GET /api/songs/` – Danh sách bài hát
- `POST /api/albums/` – Tạo album
- `GET /api/videos/` – Danh sách video

---

### 🧑‍💻 Thành viên thực hiện phần Backend

- **Phan Duy Cửu**

  - Thiết kế cơ sở dữ liệu và models
  - Xây dựng API bằng Django REST Framework
  - Xử lý logic nghiệp vụ và các tương tác CRUD
  - Phát triển giao diện quản trị

- **Trịnh Quang Trường**
  - Thiết kế cơ sở dữ liệu và models artist, video, album
  - Xử lý logic nghiệp vụ phía server
  - Kết nối với backend API
