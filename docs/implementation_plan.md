# Kế hoạch Triển khai Hệ thống VDK (Cập nhật: Tích hợp Cảm biến Siêu âm & Đa luồng)

Hệ thống được thiết kế để hoạt động tự động dựa trên cảm biến khoảng cách. Khi phát hiện người ở gần, hệ thống sẽ tự động chụp ảnh, nhận diện và gửi dữ liệu về Server.

## Các tính năng chính
1.  **Cảm biến siêu âm**: Tự động kích hoạt quy trình khi vật cản < 3cm (có thể điều chỉnh).
2.  **Chụp ảnh thông minh**: Delay 1s sau khi phát hiện vật cản để người dùng kịp ổn định vị trí trước camera.
3.  **Xử lý song song (Concurrency)**:
    *   Luồng 1: Gửi ngay ảnh chụp thô lên Server để lưu trữ/hiển thị.
    *   Luồng 2: Chạy thuật toán nhận diện khuôn mặt cục bộ trên Pi.
    *   Gửi kết quả nhận diện lên Server sau khi hoàn tất.
4.  **Server thông minh**: Ghép nối ảnh và kết quả nhận diện, sau đó gửi tin nhắn kèm hình ảnh lên Telegram Bot.

## Cấu trúc Mã nguồn

### 1. `start_server.py` (Chạy trên Laptop)
- **Chức năng**: WebSocket Server lắng nghe ảnh và kết quả từ Pi.
- **Tích hợp Telegram Bot**: Sử dụng `python-telegram-bot` để gửi ảnh kèm caption kết quả nhận diện.
- **Quản lý trạng thái**: Ghép nối dữ liệu từ nhiều luồng gửi về dựa trên `request_id`.

### 2. `start_pi.py` (Chạy trên Raspberry Pi)
- **Cảm biến**: Sử dụng `gpiozero.DistanceSensor` (HC-SR04).
- **Webcam**: Sử dụng OpenCV để chụp ảnh.
- **Nhận diện**: Thư viện `face_recognition`.
- **Giao tiếp**: WebSocket client gửi dữ liệu thô (Base64) và JSON.

### 3. `.env.example`
- Chứa Token Telegram, Chat ID, IP Server và cấu hình chân GPIO.

---

## 🛑 User Review Required

> [!IMPORTANT]
> 1. **Khoảng cách 3cm**: Bạn có muốn nâng lên khoảng 30cm-50cm để thực tế hơn không? 3cm là rất sát cảm biến.
> 2. **Phần cứng**: Bạn xác nhận sử dụng cảm biến HC-SR04 chứ?
> 3. **Đa luồng**: Việc gửi ảnh và nhận diện sẽ chạy song song để tối ưu tốc độ phản hồi của hệ thống.

## Kế hoạch Kiểm thử
- **Kiểm tra cảm biến**: Đảm bảo đo khoảng cách chính xác.
- **Kiểm tra đa luồng**: Đảm bảo Server nhận đủ 2 bản tin (ảnh và kết quả) cho mỗi lần kích hoạt.
- **Kiểm tra Telegram**: Xác nhận bot gửi được ảnh kèm nội dung text.
