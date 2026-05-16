# Hướng dẫn Vận hành Dự án trên Raspberry Pi

Hướng dẫn này tập trung vào việc cập nhật mã nguồn, cấu hình tham số và chạy hệ thống (Server & Edge) trên môi trường Raspberry Pi đã được thiết lập sẵn.

---

## 🚀 1. Kết nối vào Raspberry Pi

Mở Terminal (macOS/Linux) hoặc PowerShell (Windows) trên Laptop của bạn và kết nối qua SSH:

```bash
# Thay 'vdk-pi.local' bằng IP nếu không nhận dạng được tên máy
# ssh pi@vdk-pi.local
ssh pi@pbl5-pi.local
```

*Mật khẩu mặc định: `123456` (nếu chưa đổi).*

---

## 📥 2. Cập nhật mã nguồn (Git Pull)

Di chuyển vào thư mục dự án và lấy bản cập nhật mới nhất từ GitHub:

```bash
cd ~/vdk_project
git pull origin main
```

> [!NOTE]
> Nếu có xung đột mã nguồn (conflict), bạn có thể dùng lệnh `git reset --hard origin/main` để ghi đè hoàn toàn bằng bản trên Github (Cẩn thận: các thay đổi local sẽ bị mất).

---

## 💻 3. Chạy Server (Trên Laptop/Máy tính cá nhân)

Server đóng vai trò là trung tâm nhận dữ liệu, xử lý Dashboard và lưu trữ.

1. Mở Terminal tại thư mục `repo` của dự án trên Laptop.
2. Kích hoạt môi trường ảo:
   - **Windows**: `.venv\Scripts\activate` (Hoặc venv riêng của Laptop)
   - **Linux/macOS**: `source venv_vdk/bin/activate`
3. Chạy server:

```bash
# python start_server.py
GPIOZERO_PIN_FACTORY=lgpio python start_pi.py
```

1. Truy cập Dashboard tại: `http://localhost:8765` hoặc `http://<IP_LAPTOP>:8765`.

---

## 🥧 4. Chạy Client/Edge (Trên Raspberry Pi)

Sau khi Server đã chạy, ta khởi động script xử lý trên Pi.

### Cách 1: Chạy trực tiếp (Chế độ nhận diện khuôn mặt)

```bash
cd ~/vdk_project
source venv_vdk/bin/activate

# Chạy với logic nhận diện khuôn mặt và điều khiển phần cứng
python start_pi.py --mode "face_recognition" --server <IP_CỦA_LAPTOP>
```

### Cách 2: Chạy thông qua Systemd Service (Chạy ngầm)

Nếu bạn đã cấu hình Service, chỉ cần khởi động lại nó để áp dụng code mới:

```bash
sudo systemctl restart vdk_pi.service
```

Để xem log đang chạy ngầm:

```bash
sudo journalctl -u vdk_pi.service -f
```

---

## 🛠️ 5. Kiểm tra và Khắc phục nhanh

- **Kiểm tra Camera**: Nếu không thấy hình, thử lệnh `ls /dev/video*`.
- **Lỗi kết nối Server**: Đảm bảo Laptop và Pi đang bắt **cùng một mạng Wifi**.
- **Tràn RAM**: Nếu script bị văng (Killed), kiểm tra dung lượng Swap bằng lệnh `free -h`.

---

## 🔗 Tài liệu tham khảo

- [Hướng dẫn cài đặt chi tiết (Setup Guide)](./raspberry_pi_setup_guide.md)
- [Cấu hình Systemd Service](./raspberry_pi_setup_guide.md#5-cấu-hình-tự-động-chạy-auto-start)
