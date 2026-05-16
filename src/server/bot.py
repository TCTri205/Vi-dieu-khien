from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from src.common.config import Config

class TelegramManager:
    def __init__(self, command_callback=None):
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.command_callback = command_callback
        self._add_handlers()

    def _add_handlers(self):
        self.application.add_handler(CommandHandler("start", self._start_command))
        self.application.add_handler(CommandHandler("light_on", self._auth_wrapper(self._light_on)))
        self.application.add_handler(CommandHandler("light_off", self._auth_wrapper(self._light_off)))
        self.application.add_handler(CommandHandler("motor_on", self._auth_wrapper(self._motor_on)))
        self.application.add_handler(CommandHandler("motor_off", self._auth_wrapper(self._motor_off)))
        self.application.add_handler(CommandHandler("gate_open", self._auth_wrapper(self._gate_open)))

    def _auth_wrapper(self, func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if str(update.effective_chat.id) != str(self.chat_id):
                await update.message.reply_text(f"❌ Bạn không có quyền! ID của bạn: {update.effective_chat.id}")
                print(f"⚠️ Cảnh báo: Truy cập trái phép từ {update.effective_chat.id}")
                return
            return await func(update, context)
        return wrapper

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if str(update.effective_chat.id) != str(self.chat_id):
            await update.message.reply_text(f"🔒 Hệ thống VDK. ID của bạn: {update.effective_chat.id}")
            return
        await update.message.reply_text("🎮 Hệ thống VDK sẵn sàng!\nCác lệnh:\n/light_on, /light_off\n/motor_on, /motor_off\n/gate_open")

    async def _light_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("light", {"state": True})
        await update.message.reply_text("💡 Đã gửi lệnh BẬT đèn.")

    async def _light_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("light", {"state": False})
        await update.message.reply_text("💡 Đã gửi lệnh TẮT đèn.")

    async def _motor_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("motor", {"state": True})
        await update.message.reply_text("⚙️ Đã gửi lệnh BẬT motor.")

    async def _motor_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("motor", {"state": False})
        await update.message.reply_text("⚙️ Đã gửi lệnh TẮT motor.")

    async def _gate_open(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("gate", {})
        await update.message.reply_text("🚪 Đã gửi lệnh MỞ cổng.")

    async def send_report(self, request_id, result, image_bytes):
        caption = f"🔔 THÔNG BÁO HỆ THỐNG VDK\n🆔 ID: {request_id}\n👤 Kết quả: {result}\n"
        caption += "🔓 TRẠNG THÁI: ĐÃ MỞ CỬA" if result == "Admin" else "⚠️ TRẠNG THÁI: CẢNH BÁO XÂM NHẬP"
        try:
            await self.application.bot.send_photo(chat_id=self.chat_id, photo=image_bytes, caption=caption)
            return True
        except Exception as e:
            print(f"❌ Telegram send error: {e}")
            return False

    async def start(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        print("🤖 Telegram Bot started.")

    async def stop(self):
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()
