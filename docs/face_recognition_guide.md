# Hướng dẫn Nhận diện Khuôn mặt trên Raspberry Pi

Tài liệu này hướng dẫn cài đặt và chạy thuật toán nhận diện khuôn mặt cơ bản, tối ưu cho phần cứng Raspberry Pi.

---

## 📦 1. Cài đặt thư viện cần thiết

Trên Raspberry Pi, hãy kích hoạt môi trường ảo và cài đặt OpenCV:

```bash
cd ~/vdk_project
source venv_vdk/bin/activate

# Cài đặt OpenCV (Bản dành cho Pi)
pip install opencv-python
```

---

## 🧠 2. Thuật toán: Haar Cascades (Tối ưu tốc độ)

Haar Cascades là phương pháp nhận diện khuôn mặt cổ điển, tiêu tốn rất ít tài nguyên, phù hợp để chạy thời gian thực trên Pi 4.

### Tải file cấu hình mẫu:
OpenCV đi kèm với các file `.xml` đã huấn luyện sẵn. Bạn có thể tìm thấy chúng trong thư mục cài đặt OpenCV hoặc tải về:
`haarcascade_frontalface_default.xml`

### Mã nguồn mẫu nhận diện:
```python
import cv2

# Tải bộ phân loại (classifier)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_face(frame):
    # Chuyển sang ảnh xám để tăng tốc độ xử lý
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Phát hiện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) > 0:
        return True, faces
    return False, []

# Ví dụ tích hợp
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    found, coords = detect_face(frame)
    
    if found:
        print("👤 Đã thấy khuôn mặt! Đang kích hoạt hệ thống...")
        # Gọi hàm điều khiển phần cứng và gửi Telegram ở đây
        break
```

---

## 🚀 3. Nhận diện Admin bằng thư viện `face_recognition` (Độ chính xác cao)

Thư viện này sử dụng mô hình học sâu (Deep Learning) để so sánh đặc điểm khuôn mặt. Đây là cách tốt nhất để xác định danh tính cụ thể (như Admin).

### A. Cài đặt các thành phần phụ thuộc (Bắt buộc)
Việc cài đặt `dlib` (thư viện lõi) trên Pi mất nhiều thời gian. Hãy kiên nhẫn:

```bash
# Cài đặt các công cụ biên dịch
sudo apt update
sudo apt install -y build-essential cmake pkg-config libx11-dev libatlas-base-dev libboost-python-dev

# Kích hoạt môi trường ảo và cài đặt
source venv_vdk/bin/activate
pip install dlib
pip install face_recognition
```

### B. Chuẩn bị dữ liệu mẫu
Tạo thư mục `data/faces/` và lưu ảnh chân dung của bạn vào đó:
- `admin.jpg`: Ảnh rõ mặt của bạn.

### C. Mã nguồn nhận diện và so sánh
Dưới đây là script tối ưu để nhận diện đúng tên Admin và kích hoạt hệ thống:

```python
import face_recognition
import cv2
import numpy as np

# 1. Khởi tạo và nạp khuôn mặt Admin
print("⏳ Đang nạp dữ liệu khuôn mặt Admin...")
admin_image = face_recognition.load_image_file("data/faces/admin.jpg")
admin_encoding = face_recognition.face_encodings(admin_image)[0]

known_face_encodings = [admin_encoding]
known_face_names = ["Admin"]

# 2. Mở camera
video_capture = cv2.VideoCapture(0)

print("🚀 Hệ thống bắt đầu quét...")

while True:
    ret, frame = video_capture.read()
    
    # TỐI ƯU: Resize ảnh nhỏ lại (1/4) để xử lý nhanh hơn
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Tìm tất cả khuôn mặt trong frame hiện tại
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        # So sánh với khuôn mặt Admin đã biết
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Tính toán độ tương đồng (distance)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        if name == "Admin":
            print(f"✅ CHÀO MỪNG ADMIN! (Độ khớp: {1 - face_distances[best_match_index]:.2%})")
            # --- KÍCH HOẠT PHẦN CỨNG TẠI ĐÂY ---
            # open_gate()
            # send_telegram_alert("Admin has arrived!")
            break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
```

---

## 🛠️ 4. Bí quyết tối ưu cho Raspberry Pi 4
Để `face_recognition` không bị giật lag trên Pi:
1. **Resize Frame**: Luôn resize ảnh xuống 0.25 trước khi encoding (như ví dụ trên).
2. **Bỏ qua Frame**: Chỉ thực hiện nhận diện 1 lần sau mỗi 3 hoặc 5 frame. Các frame ở giữa chỉ dùng để hiển thị.
3. **Sử dụng HOG model**: `face_locations` mặc định dùng HOG (nhanh). Đừng đổi sang `cnn` trừ khi bạn có GPU rời (như Coral TPU).
4. **Tăng Swap**: Đảm bảo Swap của bạn là **2GB** (Hướng dẫn tại [Setup Guide](./raspberry_pi_setup_guide.md#4-tối-ưu-hóa-tăng-swap-size-chống-tràn-ram)).

---

## 🔗 Liên kết liên quan
- [Quy trình vận hành hệ thống](./system_workflow_guide.md)
- [Điều khiển phần cứng](./hardware_setup_guide.md)
