# 🎧 Spotify Clone - Backend

Hướng dẫn cài đặt
---

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
backend/
├── core/               # App chính: models, views, serializers, urls
├── backend/            # Cấu hình Django
├── media/              # Lưu trữ file upload (ảnh, video)
├── static/             # Tài nguyên tĩnh (nếu có)
├── manage.py
├── requirements.txt
└── .env                # Biến môi trường (nếu dùng)
```

---

### ⚙️ Thiết lập môi trường

1. Truy cập thư mục `backend`:

```bash
cd backend
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
venv\Scripts\activate
```

3. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

4. Chạy migrate để tạo database:

```bash
python manage.py migrate
```

5. (Tùy chọn) Tạo tài khoản superuser:

```bash
python manage.py createsuperuser
```

---

### ▶️ Khởi chạy server

```bash
python manage.py runserver
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
- `GET /api/users/me/` – Thông tin người dùng hiện tại

---

### 🧑‍💻 Thành viên thực hiện phần Backend

- **Phan Duy Cửu**  
  - Thiết kế cơ sở dữ liệu và models  
  - Xây dựng API bằng Django REST Framework  
  - Xử lý logic nghiệp vụ và các tương tác CRUD  
  - Phát triển giao diện quản trị  

- **Trịnh Quang Trường**  
  -  Thiết kế cơ sở dữ liệu và models artist, video, album
  -  Xử lý logic nghiệp vụ phía server
  -  Kết nối với backend API 
