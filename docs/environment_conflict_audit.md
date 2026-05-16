# Kiểm tra Xung đột Môi trường (Environment Audit)

Tài liệu này phân tích khả năng xung đột giữa dự án cũ và các yêu cầu mới cho hệ thống nhận diện khuôn mặt (VDK).

---

## ⚠️ 1. Các điểm cần lưu ý về thư viện

| Thư viện | Dự án cũ (Fruit) | Hệ thống mới (VDK) | Khả năng xung đột |
| :--- | :--- | :--- | :--- |
| **OpenCV** | `opencv-python-headless` | `opencv-python` | **Cao**. Không nên cài cả hai bản. |
| **Numpy** | Không chỉ định phiên bản | Yêu cầu bởi `face_recognition` | **Trung bình**. Nên ghim phiên bản. |
| **Dlib & ONNX** | Không có | Cần cho `face_recognition` | **Cao (về RAM)**. Cần tăng Swap lên 2GB. |

---

## 🛠️ 2. Phương án tối ưu: Sử dụng Môi trường ảo riêng biệt (Separate Venvs)

Vì bạn không chạy cả hai dự án cùng lúc, hãy tạo mỗi dự án một môi trường ảo riêng.

### Cấu trúc thư mục đề xuất trên Pi:
- `~/pbl5_project/` (Dự án cũ - dùng `venv_pbl5`)
- `~/vdk_project/` (Dự án VDK hiện tại - dùng `venv_vdk`)

### Lợi ích:
1. **Cô lập thư viện**: VDK có thể dùng bản OpenCV đầy đủ tính năng.
2. **Quản lý sạch sẽ**: Không làm hỏng hệ thống khi cài các thư viện nặng như `dlib`.

---

## 🚀 3. Hướng dẫn thiết lập và Chuyển đổi

### Bước 1: Tạo môi trường ảo cho VDK
```bash
cd ~/vdk_project
python3 -m venv venv_vdk
source venv_vdk/bin/activate

# Cài đặt thư viện
pip install opencv-python dlib face_recognition gpiozero websockets
```

### Bước 2: Cách chuyển đổi giữa 2 dự án
Mỗi khi muốn chuyển sang chạy dự án khác, bạn hãy `deactivate` môi trường hiện tại:

```bash
# Đang ở dự án cũ
deactivate

# Chuyển sang VDK
cd ~/vdk_project
source venv_vdk/bin/activate
python start_pi.py
```

---

## 📝 4. Lưu ý về tài nguyên hệ thống

Dù không chạy cùng lúc, nhưng **Dlib** vẫn yêu cầu tài nguyên rất lớn. Hãy đảm bảo:
1. **Tăng Swap lên 2GB** (Hướng dẫn tại [Setup Guide](./raspberry_pi_setup_guide.md)).
2. **Giải phóng RAM**: Tắt các service cũ trước khi chạy:
   ```bash
   sudo systemctl stop pbl5_pi.service
   ```

---

## 📊 5. Đánh giá tài nguyên (Resource Usage)

| Trạng thái | RAM tiêu thụ (Ước tính) | CPU tiêu thụ (Pi 4) |
| :--- | :--- | :--- |
| **Chỉ chạy dự án cũ** | ~400MB | 20-30% |
| **Chỉ chạy dự án VDK** | ~600MB | 40-60% |
| **Chạy cả hai cùng lúc** | **~1.2GB - 1.5GB** | **80-100%** |

> [!IMPORTANT]
> **Khuyên dùng**: Không nên chạy cả hai cùng lúc trên Pi 4 để tránh quá nhiệt và treo máy.
