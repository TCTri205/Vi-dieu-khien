# 🚪 Hệ thống Nhận diện Khuôn mặt và Điều khiển Thiết bị (VDK)

Dự án này sử dụng Raspberry Pi 4 để thực hiện nhận diện khuôn mặt Admin và tự động điều khiển các thiết bị ngoại vi (Servo, Relay, Motor) kết hợp với thông báo qua Telegram.

---

## 🚀 Tính năng chính
- **Face Recognition**: Nhận diện Admin với độ chính xác cao bằng thư viện `dlib` và `face_recognition`.
- **Hardware Control**: Điều khiển mở cổng (Servo), bật đèn (Relay) ngay khi phát hiện người quen.
- **Smart Notification**: Gửi thông báo tức thì kèm hình ảnh về điện thoại qua Telegram Bot.
- **Hybrid Architecture**: Xử lý hình ảnh nặng trên Laptop Server và thực thi lệnh điều khiển trên Raspberry Pi Edge.

---

## 📂 Cấu trúc Tài liệu (Documentation)

Để bắt đầu dự án, vui lòng đọc các hướng dẫn trong thư mục `docs/` theo thứ tự sau:

1.  **Thiết lập hệ thống**:
    *   [Cài đặt Raspberry Pi](./docs/raspberry_pi_setup_guide.md): Hướng dẫn triển khai dự án lên Pi (có hỗ trợ dùng chung image với PBL5).
    *   [Kiểm tra Webcam](./docs/webcam_setup_guide.md): Đảm bảo camera hoạt động ổn định.
    *   [Kiểm tra Xung đột](./docs/environment_conflict_audit.md): Lưu ý khi chạy song song nhiều dự án AI trên Pi.

2.  **Phát triển và Vận hành**:
    *   [Quy trình vận hành](./docs/system_workflow_guide.md): Luồng xử lý từ Camera -> Pi -> Laptop -> Telegram.
    *   [Nhận diện khuôn mặt](./docs/face_recognition_guide.md): Chi tiết thuật toán và code mẫu.
    *   [Điều khiển Phần cứng](./docs/hardware_setup_guide.md): Sơ đồ đấu nối và code điều khiển GPIO.
    *   [Tích hợp Telegram Bot](./docs/telegram_bot_guide.md): Cách lấy Token và gửi thông báo.

3.  **Hướng dẫn chạy nhanh**:
    *   [Chạy dự án (Run Guide)](./docs/raspberry_run_guide.md): Các lệnh SSH, khởi động Server và Edge.

---

## 🛠️ Yêu cầu hệ thống
- **Hardware**: Raspberry Pi 4 (khuyên dùng bản 4GB/8GB RAM), Webcam USB, Servo SG90, Module Relay.
- **OS**: Raspberry Pi OS (64-bit) Lite.
- **Language**: Python 3.9+.

---

## 📝 Lưu ý quan trọng
- **Tản nhiệt**: Do quá trình nhận diện khuôn mặt tiêu thụ rất nhiều CPU, hãy đảm bảo Raspberry Pi có quạt hoặc tản nhiệt tốt.
- **Bảo mật**: Không bao giờ commit file `.env` hoặc để lộ Telegram Bot Token lên các kho lưu trữ công khai.

---
*Chúc bạn thực hiện dự án thành công!*
