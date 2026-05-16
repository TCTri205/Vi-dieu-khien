# Hướng dẫn Cấu hình và Kiểm tra Webcam (Raspberry Pi)

Tài liệu này hướng dẫn cách kết nối, kiểm tra và tối ưu hóa Webcam USB cho dự án VDK trên Raspberry Pi 4.

---

## 🔍 1. Kiểm tra nhận diện thiết bị

Sau khi cắm Webcam vào cổng USB 3.0, thực hiện các lệnh sau:

### Kiểm tra danh sách thiết bị USB:
```bash
lsusb
```

### Kiểm tra file thiết bị video:
```bash
ls /dev/video*
```

### Kiểm tra chi tiết thông số:
```bash
sudo apt update && sudo apt install -y v4l-utils
v4l2-ctl --list-formats-ext
```

---

## 🐍 2. Kiểm tra bằng Python (OpenCV)

```python
import cv2

def test_camera():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ Camera hoạt động! Kích thước: {frame.shape[1]}x{frame.shape[0]}")
        cap.release()
    else:
        print("❌ Không tìm thấy Webcam.")

if __name__ == "__main__":
    test_camera()
```

---

## 🛠️ 3. Các lỗi thường gặp

### 1. Lỗi "Permission Denied"
Thêm user `pi` vào nhóm `video`:
```bash
sudo usermod -a -G video pi
```

### 2. Camera bị "Busy"
Nếu một service khác đang dùng camera, bạn sẽ không thể mở nó. 
Kiểm tra xem service nào đang chạy:
```bash
sudo systemctl status vdk_pi.service
```

---

## 🔗 Liên kết liên quan
- [Hướng dẫn chạy dự án (Run Guide)](./raspberry_run_guide.md)
- [Cài đặt hệ thống (Setup Guide)](./raspberry_pi_setup_guide.md)
