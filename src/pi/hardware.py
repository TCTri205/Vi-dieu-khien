import asyncio
import time
import threading
import lgpio
from src.common.config import Config


class HardwareManager:
    def __init__(self):
        self._lock = threading.Lock()  # Bảo vệ lgpio handle khỏi đa luồng
        try:
            # Mở DUY NHẤT 1 lgpio handle — không dùng gpiozero
            self._h = lgpio.gpiochip_open(0)

            # ===== Cảm biến siêu âm — lgpio trực tiếp =====
            self._trig_pin = Config.TRIG_PIN
            self._echo_pin = Config.ECHO_PIN
            lgpio.gpio_claim_output(self._h, self._trig_pin)
            lgpio.gpio_write(self._h, self._trig_pin, 0)
            lgpio.gpio_claim_input(self._h, self._echo_pin)
            print(f"  📡 Sensor: lgpio on GPIO {self._trig_pin}/{self._echo_pin}")

            # ===== Servo (GPIO 5) =====
            self._servo_pin = Config.SERVO_PIN
            lgpio.gpio_claim_output(self._h, self._servo_pin)
            print(f"  🔧 Servo: lgpio on GPIO {self._servo_pin}")

            # ===== LED (GPIO 17) =====
            self._light_pin = Config.LIGHT_PIN
            lgpio.gpio_claim_output(self._h, self._light_pin)
            lgpio.gpio_write(self._h, self._light_pin, 0)
            print(f"  💡 Light: lgpio on GPIO {self._light_pin}")

            # ===== Motor/Relay (GPIO 27) =====
            self._motor_pin = Config.MOTOR_PIN
            lgpio.gpio_claim_output(self._h, self._motor_pin)
            lgpio.gpio_write(self._h, self._motor_pin, 0)
            print(f"  ⚙️ Motor: lgpio on GPIO {self._motor_pin}")

            # ===== Buzzer (GPIO 25) =====
            self._buzzer_pin = Config.BUZZER_PIN
            if self._buzzer_pin > 0:
                lgpio.gpio_claim_output(self._h, self._buzzer_pin)
                print(f"  📢 Buzzer: lgpio on GPIO {self._buzzer_pin}")
            else:
                print("  📢 Buzzer: Disabled (pin 0)")

            self._light_task = None
            print("✅ Hardware initialized (lgpio only).")
        except Exception as e:
            print(f"⚠️ Hardware init error: {e}")
            self._h = None
            self._trig_pin = None
            self._echo_pin = None
            self._servo_pin = None
            self._light_pin = None
            self._motor_pin = None
            self._buzzer_pin = None
            self._light_task = None

    # ===== CẢM BIẾN SIÊU ÂM =====
    def get_distance(self):
        """Đo khoảng cách bằng HC-SR04/HY-SRF05, trả về mét."""
        if not self._h:
            return 1.0
        with self._lock:  # Khóa handle trong khi đọc cảm biến
            try:
                # Gửi xung trigger 10us
                lgpio.gpio_write(self._h, self._trig_pin, 1)
                time.sleep(0.00001)  # 10 microseconds
                lgpio.gpio_write(self._h, self._trig_pin, 0)

                # Chờ echo HIGH (timeout 0.1s)
                start = time.time()
                timeout = start + 0.1
                while lgpio.gpio_read(self._h, self._echo_pin) == 0:
                    start = time.time()
                    if start > timeout:
                        return 1.0  # Timeout

                # Chờ echo LOW
                end = time.time()
                timeout2 = end + 0.1
                while lgpio.gpio_read(self._h, self._echo_pin) == 1:
                    end = time.time()
                    if end > timeout2:
                        return 1.0  # Timeout

                # Tính khoảng cách (m)
                duration = end - start
                distance = (duration * 34300) / 2 / 100  # cm -> m
                return distance
            except Exception:
                return 1.0

    # ===== BUZZER =====
    async def beep_welcome(self):
        """Bíp 1 tiếng ngắn khi nhận diện được người quen."""
        if self._h and self._buzzer_pin and self._buzzer_pin > 0:
            print("🔊 Beep: Welcome")
            lgpio.tx_pwm(self._h, self._buzzer_pin, 1000, 50)
            await asyncio.sleep(Config.BUZZER_SHORT_BEEP)
            lgpio.tx_pwm(self._h, self._buzzer_pin, 0, 0)

    async def beep_alert(self):
        """Bíp 3 tiếng liên tục khi phát hiện người lạ."""
        if self._h and self._buzzer_pin and self._buzzer_pin > 0:
            print(f"🔊 Beep: Alert ({Config.BUZZER_ALERT_COUNT} times)")
            for _ in range(Config.BUZZER_ALERT_COUNT):
                lgpio.tx_pwm(self._h, self._buzzer_pin, 880, 50)
                await asyncio.sleep(Config.BUZZER_ALERT_BEEP)
                lgpio.tx_pwm(self._h, self._buzzer_pin, 0, 0)
                await asyncio.sleep(Config.BUZZER_ALERT_BEEP)

    # ===== SERVO =====
    async def open_gate(self):
        """Mở cửa: Servo quay từ 2000us về 1000us (đảo chiều) -> giữ -> trả về 2000us."""
        if self._h and self._servo_pin is not None:
            print(f"🚪 Opening gate for {Config.GATE_HOLD_TIME}s...")
            lgpio.tx_servo(self._h, self._servo_pin, 1000)
            print("🚪 Servo -> 0° (open)")
            await asyncio.sleep(Config.GATE_HOLD_TIME)
            lgpio.tx_servo(self._h, self._servo_pin, 2000)
            print("🚪 Servo -> 90° (closed)")
            await asyncio.sleep(0.5)
            lgpio.tx_servo(self._h, self._servo_pin, 0)
        else:
            print(f"🚪 [Mock] Gate opened for {Config.GATE_HOLD_TIME}s.")

    # ===== ĐÈN LED =====
    async def control_light(self, state=True, duration=0):
        """Bật/tắt đèn LED."""
        if self._light_task:
            self._light_task.cancel()
            self._light_task = None

        if self._h and self._light_pin is not None:
            print(f"💡 Light {'ON' if state else 'OFF'}")
            lgpio.gpio_write(self._h, self._light_pin, 1 if state else 0)
            if state:
                off_delay = duration if duration > 0 else Config.LIGHT_AUTO_OFF_TIME
                self._light_task = asyncio.create_task(self._auto_off_light(off_delay))
        else:
            print(f"💡 [Mock] Light {'ON' if state else 'OFF'}")

    async def _auto_off_light(self, delay):
        try:
            await asyncio.sleep(delay)
            if self._h and self._light_pin is not None:
                lgpio.gpio_write(self._h, self._light_pin, 0)
                print(f"💡 Light auto-off after {delay}s.")
        except asyncio.CancelledError:
            pass

    # ===== MOTOR (Relay → Quạt) =====
    async def control_motor(self, state=True, duration=0):
        """Bật/tắt quạt qua relay."""
        if self._h and self._motor_pin is not None:
            print(f"⚙️ Motor {'ON' if state else 'OFF'}")
            lgpio.gpio_write(self._h, self._motor_pin, 1 if state else 0)
            if state and duration > 0:
                await asyncio.sleep(duration)
                lgpio.gpio_write(self._h, self._motor_pin, 0)
        else:
            print(f"⚙️ [Mock] Motor {'ON' if state else 'OFF'}")

    def cleanup(self):
        """Giải phóng tài nguyên GPIO."""
        if self._h is not None:
            try:
                for pin in [self._light_pin, self._motor_pin]:
                    if pin is not None:
                        lgpio.gpio_write(self._h, pin, 0)
                        lgpio.gpio_free(self._h, pin)
                if self._servo_pin is not None:
                    lgpio.tx_servo(self._h, self._servo_pin, 0)
                    lgpio.gpio_free(self._h, self._servo_pin)
                if self._buzzer_pin and self._buzzer_pin > 0:
                    lgpio.tx_pwm(self._h, self._buzzer_pin, 0, 0)
                    lgpio.gpio_free(self._h, self._buzzer_pin)
                if self._trig_pin is not None:
                    lgpio.gpio_free(self._h, self._trig_pin)
                if self._echo_pin is not None:
                    lgpio.gpio_free(self._h, self._echo_pin)
                lgpio.gpiochip_close(self._h)
                print("🧹 GPIO cleaned up.")
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")
