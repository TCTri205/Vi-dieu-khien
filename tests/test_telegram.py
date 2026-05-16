import asyncio
import os
from src.server.bot import TelegramManager
from src.common.config import Config

async def test_telegram():
    print("🧪 Bắt đầu kiểm tra kết nối Telegram Bot...")
    
    # Kiểm tra Config
    if not Config.TELEGRAM_BOT_TOKEN or not Config.TELEGRAM_CHAT_ID:
        print("❌ LỖI: Chưa cấu hình TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong file .env")
        return

    # Khởi tạo bot
    # Lưu ý: Không cần callback vì chỉ test gửi tin nhắn
    bot_manager = TelegramManager()
    
    try:
        # Khởi tạo ứng dụng bot
        await bot_manager.application.initialize()
        
        print(f"📡 Đang gửi tin nhắn thử nghiệm tới Chat ID: {Config.TELEGRAM_CHAT_ID}...")
        
        # 1. Test gửi tin nhắn văn bản đơn giản
        await bot_manager.application.bot.send_message(
            chat_id=Config.TELEGRAM_CHAT_ID,
            text="🚀 [TEST] Kết nối từ Server tới Telegram Bot thành công!"
        )
        print("✅ Đã gửi tin nhắn văn bản.")

        # 2. Test gửi báo cáo (có ảnh giả lập)
        # Tạo một ảnh đen đơn giản để test
        print("🖼️ Đang gửi báo cáo thử nghiệm kèm ảnh...")
        test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        
        success = await bot_manager.send_report(
            request_id="TEST1234",
            result="Admin (Test)",
            image_bytes=test_image
        )
        
        if success:
            print("✅ Đã gửi báo cáo kèm ảnh thành công.")
        else:
            print("❌ Gửi báo cáo thất bại.")

    except Exception as e:
        print(f"❌ Có lỗi xảy ra trong quá trình test: {e}")
    finally:
        # Dọn dẹp
        await bot_manager.application.shutdown()
        print("🏁 Kết thúc kiểm tra.")

if __name__ == "__main__":
    asyncio.run(test_telegram())
