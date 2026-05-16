# Hướng dẫn Triển khai Dự án VDK (Dùng chung OS với PBL5)

Tài liệu này hướng dẫn cách cài đặt dự án VDK lên một chiếc Raspberry Pi đã được thiết lập sẵn từ dự án PBL5. Bạn **không cần** phải cài lại hệ điều hành (Flash OS).

---

## 🔑 1. Kết nối SSH

Sử dụng thông tin đăng nhập cũ để truy cập vào Pi:
```bash
ssh pi@vdk-pi.local
# Hoặc dùng hostname cũ nếu bạn chưa đổi:
# ssh pi@pbl5-pi.local
```

---

# 2. Triển khai Mã nguồn mới

Chúng ta sẽ tạo một thư mục riêng để không ảnh hưởng đến code của PBL5.

```bash
# Di chuyển về thư mục gốc
cd ~

# Tải dự án VDK
git clone https://github.com/TCTri205/Vi-dieu-khien.git ~/vdk_project
cd ~/vdk_project

# Cài đặt các thư viện hệ thống cần thiết (Rất quan trọng cho dlib và opencv)
sudo apt-get update
sudo apt-get install -y cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev

# Tạo môi trường ảo riêng (Để tránh xung đột thư viện với PBL5)
python3 -m venv venv_vdk
source venv_vdk/bin/activate

# Cài đặt các thư viện từ requirements.txt
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📝 3. Cấu hình Môi trường (.env)

Đừng quên tạo file cấu hình để hệ thống biết IP Server và các thông tin cần thiết:

```bash
cp .env.example .env
nano .env
```
*Chỉnh sửa `SERVER_IP` thành IP của Laptop và cập nhật các thông tin Telegram.*

---

## 🛠️ 4. Kiểm tra Tài nguyên (RAM/Swap)

Vì bạn dùng chung image, có thể Swap đã được tăng lên 2GB từ trước. Hãy kiểm tra lại:

```bash
free -h
```
- Nếu phần **Swap** đã hiện khoảng `2.0Gi`, bạn có thể bỏ qua bước này.
- Nếu chưa, hãy làm theo hướng dẫn:
  ```bash
  sudo nano /etc/dphys-swapfile
  # Đổi CONF_SWAPSIZE=2048
  sudo dphys-swapfile setup
  sudo dphys-swapfile swapon
  ```

---

## ⚙️ 5. Cấu hình Dịch vụ (Systemd Service)

Để chạy VDK mà không xung đột với PBL5 (đặc biệt là tranh chấp Webcam), bạn cần quản lý các service:

### A. Dừng service PBL5 (nếu đang chạy)
```bash
sudo systemctl stop pbl5_pi.service
# Nếu muốn tắt hẳn tự động khởi chạy của PBL5:
# sudo systemctl disable pbl5_pi.service
```

### B. Cài đặt service VDK
1. Tạo file: `sudo nano /etc/systemd/system/vdk_pi.service`
2. Dán nội dung:
   ```ini
   [Unit]
   Description=VDK Face Recognition Service
   After=network.target

   [Service]
   User=pi
   WorkingDirectory=/home/pi/vdk_project
   ExecStart=/home/pi/vdk_project/venv_vdk/bin/python /home/pi/vdk_project/start_pi.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
3. Kích hoạt:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable vdk_pi.service
   sudo systemctl start vdk_pi.service
   ```

---

## 🚀 6. Chuyển đổi qua lại giữa 2 dự án

Mỗi khi muốn chuyển từ nhận diện trái cây (PBL5) sang nhận diện khuôn mặt (VDK) và ngược lại:

| Hành động | Lệnh thực hiện |
| :--- | :--- |
| **Chạy VDK** | `sudo systemctl stop pbl5_pi.service && sudo systemctl start vdk_pi.service` |
| **Chạy PBL5** | `sudo systemctl stop vdk_pi.service && sudo systemctl start pbl5_pi.service` |

---

## 🔗 Liên kết liên quan
- [Hướng dẫn Vận hành nhanh](./raspberry_run_guide.md)
- [Điều khiển phần cứng](./hardware_setup_guide.md)
- [Kiểm tra Webcam](./webcam_setup_guide.md)
