import asyncio
import lgpio
from gpiozero import DistanceSensor
from src.common.config import Config

class HardwareManager:
    def __init__(self):
        try:
            # Mở lgpio chip — dùng cho Servo, Relay, LED, Buzzer
            self._h = lgpio.gpiochip_open(0)

            # ===== Cảm biến siêu âm (giữ gpiozero — hoạt động ổn) =====
            self.sensor = DistanceSensor(echo=Config.ECHO_PIN, trigger=Config.TRIG_PIN)

            # ===== Servo (GPIO 5) — dùng lgpio.tx_servo trực tiếp =====
            self._servo_pin = Config.SERVO_PIN
            lgpio.gpio_claim_output(self._h, self._servo_pin)
            print(f"  🔧 Servo: lgpio.tx_servo on GPIO {self._servo_pin}")

            # ===== LED (GPIO 17) — dùng lgpio trực tiếp =====
            self._light_pin = Config.LIGHT_PIN
            lgpio.gpio_claim_output(self._h, self._light_pin)
            lgpio.gpio_write(self._h, self._light_pin, 0)  # Tắt ban đầu
            print(f"  💡 Light: lgpio on GPIO {self._light_pin}")

            # ===== Motor/Relay (GPIO 27) — dùng lgpio trực tiếp =====
            self._motor_pin = Config.MOTOR_PIN
            lgpio.gpio_claim_output(self._h, self._motor_pin)
            lgpio.gpio_write(self._h, self._motor_pin, 0)  # Tắt ban đầu
            print(f"  ⚙️ Motor: lgpio on GPIO {self._motor_pin}")

            # ===== Buzzer (GPIO 25) — dùng lgpio trực tiếp =====
            self._buzzer_pin = Config.BUZZER_PIN
            if self._buzzer_pin > 0:
                lgpio.gpio_claim_output(self._h, self._buzzer_pin)
                print(f"  📢 Buzzer: lgpio on GPIO {self._buzzer_pin}")
            else:
                print("  📢 Buzzer: Disabled (pin 0)")

            self._light_task = None
            print("✅ Hardware initialized (lgpio direct).")
        except Exception as e:
            print(f"⚠️ Hardware init error: {e}")
            self._h = None
            self.sensor = None
            self._servo_pin = None
            self._light_pin = None
            self._motor_pin = None
            self._buzzer_pin = None
            self._light_task = None

    def get_distance(self):
        if self.sensor:
            return self.sensor.distance
        return 1.0  # Mock distance

    # ===== BUZZER =====
    async def beep_welcome(self):
        """Bíp 1 tiếng ngắn khi nhận diện được người quen."""
        if self._h and self._buzzer_pin and self._buzzer_pin > 0:
            print("🔊 Beep: Welcome")
            # Dùng PWM 1kHz cho passive buzzer (giống diagnose_hw.py)
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

    # ===== SERVO (Cửa tự động) =====
    async def open_gate(self):
        """Mở cửa: Servo quay 90° → giữ → đóng lại 0°."""
        if self._h and self._servo_pin is not None:
            print(f"🚪 Opening gate for {Config.GATE_HOLD_TIME}s...")
            # 2000us ≈ 90° (giống diagnose_hw.py dùng lgpio.tx_servo)
            lgpio.tx_servo(self._h, self._servo_pin, 2000)
            print("🚪 Servo -> 90° (open)")
            await asyncio.sleep(Config.GATE_HOLD_TIME)
            # 1000us ≈ 0° (giống diagnose_hw.py)
            lgpio.tx_servo(self._h, self._servo_pin, 1000)
            print("🚪 Servo -> 0° (closed)")
            await asyncio.sleep(0.5)
            # Tắt xung servo để tránh jitter
            lgpio.tx_servo(self._h, self._servo_pin, 0)
        else:
            print(f"🚪 [Mock] Gate opened for {Config.GATE_HOLD_TIME}s.")

    # ===== ĐÈN LED =====
    async def control_light(self, state=True, duration=0):
        """Bật/tắt đèn LED."""
        # Hủy task tự động tắt cũ nếu có
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
                # Tắt tất cả trước khi giải phóng
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
                lgpio.gpiochip_close(self._h)
                print("🧹 GPIO cleaned up.")
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")
