# Hướng dẫn Tích hợp Telegram Bot (VDK)

Hướng dẫn xây dựng Telegram Bot để giám sát và điều khiển hệ thống VDK từ xa.

---

## 🏗️ 1. Kiến trúc hệ thống

| Tiêu chí | Chạy trên Raspberry Pi (Edge) | Chạy trên Laptop (Server) |
| :--- | :--- | :--- |
| **Ưu điểm** | Hoạt động độc lập. | Xử lý được các logic phức tạp. |
| **Khuyên dùng** | Nếu chỉ giám sát cảm biến đơn giản. | **Nên dùng cho dự án VDK** vì Laptop sẽ xử lý logic thông báo sau khi nhận tin từ Pi. |

---

## 🤖 2. Thiết lập Telegram Bot

1. Mở Telegram, tìm `@BotFather` -> `/newbot` để lấy **API Token**.
2. Tìm `@userinfobot` để lấy **Chat ID**.

---

## 💻 3. Mã nguồn mẫu (`python-telegram-bot`)

```python
import asyncio
from telegram import Bot

TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

async def send_notification(message):
    bot = Bot(token=TOKEN)
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    asyncio.run(send_notification("🚀 Hệ thống VDK đã sẵn sàng!"))
```

---

## 🛠️ 4. Bảo mật
- Sử dụng file `.env` để lưu Token. **Không để lộ Token lên GitHub**.

---

## 🔗 Liên kết liên quan
- [Hướng dẫn Phần cứng](./hardware_setup_guide.md)
- [Quy trình vận hành](./system_workflow_guide.md)
- [Hướng dẫn chạy dự án](./raspberry_run_guide.md)
