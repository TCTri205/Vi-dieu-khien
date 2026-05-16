# Hướng dẫn Kết nối và Điều khiển Phần cứng (VDK)

Tài liệu này hướng dẫn cách kết nối và lập trình cho các thiết bị ngoại vi trên Raspberry Pi 4 cho dự án VDK, dựa trên sơ đồ mạch chuẩn.

---

## 1. Bảng tra cứu chân GPIO (Mapping)

| Thiết bị | Chân GPIO | Pin vật lý | Chú thích |
|----------|-----------|------------|-----------|
| **Servo SG90** | **GPIO 18** | Pin 12 | PWM phần cứng (Mượt hơn) |
| **Đèn LED** | **GPIO 17** | Pin 11 | Điều khiển qua điện trở 220Ω |
| **Relay (Quạt)**| **GPIO 27** | Pin 13 | Module Relay 1 kênh |
| **Buzzer** | **GPIO 25** | Pin 22 | Âm thanh phản hồi |
| **Siêu âm (Trig)**| **GPIO 23** | Pin 16 | Phát tín hiệu |
| **Siêu âm (Echo)**| **GPIO 24** | Pin 18 | Nhận tín hiệu (Cần mạch phân áp) |

---

## 2. Chi tiết từng thành phần

### A. Động cơ Servo (Cửa tự động)
- **GPIO 18**: Chân này cực kỳ quan trọng vì hỗ trợ xung PWM phần cứng.
- **Mã nguồn:** `AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)`

### B. Module Relay & Quạt
- **GPIO 27**: Được cấu hình `active_high=False` (Kích mức thấp). Khi `relay.on()`, Relay sẽ đóng mạch.

### C. Đèn LED
- **GPIO 17**: Điều khiển bật/tắt đơn giản. Code tích hợp cơ chế tự động tắt sau 1 giờ để tiết kiệm điện.

### D. Còi Buzzer
- **GPIO 25**: Dùng để tạo tiếng bíp chào mừng (1 bíp) hoặc cảnh báo (3 bíp).

---

## 🧪 Kiểm tra nhanh (Test Scripts)

Bạn có thể chạy các script sau trong thư mục `tests/` để kiểm tra từng thiết bị riêng lẻ:

1. `python tests/test_servo.py`: Kiểm tra cửa xoay.
2. `python tests/test_buzzer.py`: Kiểm tra còi kêu.
3. `python tests/test_ultrasonic.py`: Kiểm tra cảm biến khoảng cách.

---

## ⚠️ Lưu ý an toàn:
- **Nguồn điện:** Tuyệt đối không cấp nguồn 6V từ khay pin vào chân 5V của Pi.
- **GND chung:** Bắt buộc nối cực Âm (-) của pin 6V vào chân GND của Pi.
- **Mạch phân áp:** Chân Echo của Siêu âm PHẢI đi qua 2 điện trở để hạ áp xuống 2.5V trước khi vào Pi.

---

## 🔗 Liên kết liên quan
- [Sơ đồ mạch chi tiết](./So_do_mach.md)
- [Quy trình vận hành](./system_workflow_guide.md)
- [Cài đặt Raspberry Pi](./raspberry_pi_setup_guide.md)
