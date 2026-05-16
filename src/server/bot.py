from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from src.common.config import Config

class TelegramManager:
    HELP_TEXT = (
        "🎮 Các lệnh có thể chạy:\n"
        "/light_on - Bật đèn\n"
        "/light_off - Tắt đèn\n"
        "/motor_on - Bật motor\n"
        "/motor_off - Tắt motor\n"
        "/gate_open - Mở cổng\n"
        "/register [tên] - Đăng ký khuôn mặt mới\n"
        "/remove [tên] - Xóa dữ liệu khuôn mặt"
    )

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
        self.application.add_handler(CommandHandler("register", self._auth_wrapper(self._register_face)))
        self.application.add_handler(CommandHandler("remove", self._auth_wrapper(self._remove_face)))
        self.application.add_handler(CallbackQueryHandler(self._button_callback))

    def _auth_wrapper(self, func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            chat_id = update.effective_chat.id if update.effective_chat else None
            if str(chat_id) != str(self.chat_id):
                if update.effective_message:
                    await update.effective_message.reply_text(f"❌ Bạn không có quyền! ID của bạn: {chat_id}")
                print(f"⚠️ Cảnh báo: Truy cập trái phép từ {chat_id}")
                return
            return await func(update, context)
        return wrapper

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id if update.effective_chat else None
        if str(chat_id) != str(self.chat_id):
            if update.effective_message:
                await update.effective_message.reply_text(f"🔒 Hệ thống VDK. ID của bạn: {chat_id}")
            return
        if update.effective_message:
            await update.effective_message.reply_text(f"🎮 Hệ thống VDK sẵn sàng!\n{self.HELP_TEXT}")

    async def _light_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("light", {"state": True})
        if update.effective_message: await update.effective_message.reply_text("💡 Đã gửi lệnh BẬT đèn.")

    async def _light_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("light", {"state": False})
        if update.effective_message: await update.effective_message.reply_text("💡 Đã gửi lệnh TẮT đèn.")

    async def _motor_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("motor", {"state": True})
        if update.effective_message: await update.effective_message.reply_text("⚙️ Đã gửi lệnh BẬT motor.")

    async def _motor_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("motor", {"state": False})
        if update.effective_message: await update.effective_message.reply_text("⚙️ Đã gửi lệnh TẮT motor.")

    async def _gate_open(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.command_callback: await self.command_callback("gate", {})
        if update.effective_message: await update.effective_message.reply_text("🚪 Đã gửi lệnh MỞ cổng.")

    async def _register_face(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            if update.effective_message:
                await update.effective_message.reply_text("⚠️ Vui lòng nhập tên người cần đăng ký: /register [tên]")
            return
        name = context.args[0]
        if self.command_callback:
            await self.command_callback("register_request", {"name": name})
        if update.effective_message:
            await update.effective_message.reply_text(f"📸 Đang yêu cầu chụp ảnh cho: {name}\nHãy đứng trước webcam...")

    async def _remove_face(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            if update.effective_message:
                await update.effective_message.reply_text("⚠️ Vui lòng nhập tên người cần xóa: /remove [tên]")
            return
        name = context.args[0]
        if self.command_callback:
            await self.command_callback("remove", {"name": name})
        if update.effective_message:
            await update.effective_message.reply_text(f"🗑️ Đã gửi lệnh xóa khuôn mặt: {name}")

    async def _button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        data = query.data.split(":")
        action = data[0]
        name = data[1] if len(data) > 1 else ""

        if action == "confirm_reg":
            if self.command_callback:
                await self.command_callback("register_confirm", {"name": name})
            await query.edit_message_caption(caption=f"✅ Đã xác nhận đăng ký cho {name}. Đang lưu...")
        elif action == "cancel_reg":
            await query.edit_message_caption(caption=f"❌ Đã hủy đăng ký cho {name}.")

    async def send_report(self, request_id, result, image_bytes):
        if result not in ["Unknown", "No face data"]:
            caption = f"🔔 THÔNG BÁO HỆ THỐNG VDK\n🆔 ID: {request_id}\n👤 Chào mừng {result}!\n🔓 TRẠNG THÁI: ĐÃ MỞ CỬA"
        else:
            caption = f"🔔 THÔNG BÁO HỆ THỐNG VDK\n🆔 ID: {request_id}\n👤 Kết quả: {result}\n⚠️ TRẠNG THÁI: CẢNH BÁO XÂM NHẬP"
        
        try:
            await self.application.bot.send_photo(chat_id=self.chat_id, photo=image_bytes, caption=caption)
            return True
        except Exception as e:
            print(f"❌ Telegram send error: {e}")
            return False

    async def send_registration_photo(self, name, image_bytes):
        keyboard = [
            [
                InlineKeyboardButton("✅ Xác nhận", callback_data=f"confirm_reg:{name}"),
                InlineKeyboardButton("❌ Hủy", callback_data=f"cancel_reg:{name}"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            await self.application.bot.send_photo(
                chat_id=self.chat_id, 
                photo=image_bytes, 
                caption=f"❓ Bạn có muốn đăng ký khuôn mặt này cho '{name}' không?",
                reply_markup=reply_markup
            )
            return True
        except Exception as e:
            print(f"❌ Telegram registration photo error: {e}")
            return False

    async def send_message(self, text):
        if not self.chat_id:
            print("⚠️ TELEGRAM_CHAT_ID is not set. Cannot send message.")
            return False
        try:
            await self.application.bot.send_message(chat_id=self.chat_id, text=text)
            return True
        except Exception as e:
            print(f"❌ Telegram send_message error: {e}")
            return False

    async def notify_startup(self):
        print("📢 Sending startup notification to Telegram...")
        welcome_msg = f"🚀 Server VDK đã khởi động!\n\n{self.HELP_TEXT}"
        await self.send_message(welcome_msg)

    async def start(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        print("🤖 Telegram Bot started.")

    async def stop(self):
        await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()
