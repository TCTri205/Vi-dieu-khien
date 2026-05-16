# Hướng dẫn Kết nối và Điều khiển Phần cứng (VDK)

Tài liệu này hướng dẫn cách kết nối và lập trình cho Động cơ Servo, Motor DC và Module Relay trên Raspberry Pi 4 cho dự án VDK.

---

## 1. Động cơ Servo (Góc quay)

### Sơ đồ đấu nối:
- **Dây Đỏ**: 5V.
- **Dây Nâu/Đen**: GND.
- **Dây Cam/Vàng (Signal)**: **GPIO 5** (Pin 29).

### Mã nguồn mẫu (`gpiozero`):
```python
from gpiozero import AngularServo
from time import sleep

servo = AngularServo(5, min_pulse_width=0.0005, max_pulse_width=0.0025)

def open_gate():
    servo.angle = 90
    sleep(2)
    servo.angle = 0
```

---

## 2. Module Relay (Bật tắt thiết bị)

### Sơ đồ đấu nối:
- **VCC**: 5V.
- **GND**: GND.
- **IN**: **GPIO 17** (Pin 11).

### Mã nguồn mẫu:
```python
from gpiozero import OutputDevice

relay = OutputDevice(17, active_high=False)

def toggle_light():
    relay.on() # Bật
    sleep(1)
    relay.off() # Tắt
```

---

## ⚠️ Lưu ý an toàn:
- Luôn sử dụng nguồn riêng cho Motor/Servo nếu cần dòng lớn.
- Kiểm tra kỹ chân GPIO trước khi cấp điện.

---

## 🔗 Liên kết liên quan
- [Hướng dẫn Webcam](./webcam_setup_guide.md)
- [Quy trình vận hành](./system_workflow_guide.md)
- [Cài đặt Raspberry Pi](./raspberry_pi_setup_guide.md)
