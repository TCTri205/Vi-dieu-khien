# Tổng quan hệ thống Vi-điều-khiển (VDK)

Hệ thống hoạt động theo mô hình **Edge Computing** (Xử lý tại biên trên Pi) kết hợp với **Server thông báo**.

## 1. Kết quả kiểm tra (Code Review)
Đã sửa lỗi cú pháp quan trọng: Đổi tên biến `RE-TRIGGER_DELAY` thành `RE_TRIGGER_DELAY` trong `config.py` và `start_pi.py`.

## 2. Luồng hoạt động của hệ thống

### Bước 1: Giám sát khoảng cách (Raspberry Pi)
- Cảm biến siêu âm HC-SR04 liên tục đo khoảng cách.
- Nếu có người đến gần (khoảng cách < 3cm), hệ thống sẽ kích hoạt quy trình kiểm tra.

### Bước 2: Thu thập dữ liệu (Raspberry Pi)
- Hệ thống đợi 1 giây (`CAPTURE_DELAY`) để người dùng đứng ổn định trước camera.
- Camera chụp 1 khung hình (frame).
- Một `request_id` duy nhất được tạo ra để đồng bộ dữ liệu giữa Pi và Server.

### Bước 3: Xử lý song song (Raspberry Pi)
Hệ thống thực hiện 3 việc cùng lúc:
1. **Gửi ảnh:** Mã hóa ảnh sang Base64 và gửi lên Server qua WebSocket.
2. **Nhận diện:** So khớp khuôn mặt trong ảnh với dữ liệu Admin đã lưu sẵn.
3. **Gửi kết quả:** Gửi kết quả nhận diện ("Admin" hoặc "Unknown") lên Server.

### Bước 4: Điều khiển phần cứng (Raspberry Pi)
- Nếu kết quả là **Admin**:
    - Quay Servo 90 độ để mở cửa, đợi 2 giây rồi đóng lại.
    - Bật Relay (đèn) trong 3 giây rồi tắt.

### Bước 5: Thông báo (Laptop Server)
- Server lắng nghe kết nối từ Pi.
- Khi nhận đủ cả **Ảnh** và **Kết quả** của cùng một `request_id`, Server sẽ gửi thông báo đến Telegram (Kèm ảnh và trạng thái).

## 3. Các thông số cần lưu ý trong `Config`
- `DISTANCE_THRESHOLD = 0.03`: Khoảng cách kích hoạt (3cm).
- `RE_TRIGGER_DELAY = 5.0`: Thời gian nghỉ sau mỗi lần kích hoạt.
- `SERVER_IP`: IP của Laptop trong mạng nội bộ.
