import asyncio
from gpiozero import AngularServo, OutputDevice, DistanceSensor
from src.common.config import Config

class HardwareManager:
    def __init__(self):
        try:
            self.sensor = DistanceSensor(echo=Config.ECHO_PIN, trigger=Config.TRIG_PIN)
            self.servo = AngularServo(Config.SERVO_PIN, min_pulse_width=0.0005, max_pulse_width=0.0025)
            self.light = OutputDevice(Config.LIGHT_PIN, active_high=False)
            self.motor = OutputDevice(Config.MOTOR_PIN, active_high=False)
            self.buzzer = OutputDevice(Config.BUZZER_PIN)
            self._light_task = None
            print("✅ Hardware initialized.")
        except Exception as e:
            print(f"⚠️ Hardware init error (Mock mode enabled): {e}")
            self.sensor = None
            self.servo = None
            self.light = None
            self.motor = None
            self.buzzer = None
            self._light_task = None

    def get_distance(self):
        if self.sensor:
            return self.sensor.distance
        return 1.0 # Mock distance

    async def beep_welcome(self):
        if self.buzzer:
            print("🔊 Beep: Welcome")
            self.buzzer.on()
            await asyncio.sleep(Config.BUZZER_SHORT_BEEP)
            self.buzzer.off()
        else:
            print("🔊 [Mock] Beep: Welcome")

    async def beep_alert(self):
        if self.buzzer:
            print(f"🔊 Beep: Alert ({Config.BUZZER_ALERT_COUNT} times)")
            for _ in range(Config.BUZZER_ALERT_COUNT):
                self.buzzer.on()
                await asyncio.sleep(Config.BUZZER_ALERT_BEEP)
                self.buzzer.off()
                await asyncio.sleep(Config.BUZZER_ALERT_BEEP)
        else:
            print(f"🔊 [Mock] Beep: Alert ({Config.BUZZER_ALERT_COUNT} times)")

    async def open_gate(self):
        if self.servo:
            print(f"🚪 Opening gate for {Config.GATE_HOLD_TIME}s...")
            self.servo.angle = 90
            await asyncio.sleep(Config.GATE_HOLD_TIME)
            self.servo.angle = 0
        else:
            print(f"🚪 [Mock] Gate opened for {Config.GATE_HOLD_TIME}s.")

    async def control_light(self, state=True, duration=0):
        # Hủy task tự động tắt cũ nếu có
        if self._light_task:
            self._light_task.cancel()
            self._light_task = None

        if self.light:
            print(f"💡 Light {'ON' if state else 'OFF'}")
            if state:
                self.light.on()
                # Nếu có duration (từ lệnh manual) hoặc theo mặc định 1h
                off_delay = duration if duration > 0 else Config.LIGHT_AUTO_OFF_TIME
                self._light_task = asyncio.create_task(self._auto_off_light(off_delay))
            else:
                self.light.off()
        else:
            print(f"💡 [Mock] Light {'ON' if state else 'OFF'}")

    async def _auto_off_light(self, delay):
        try:
            await asyncio.sleep(delay)
            if self.light:
                self.light.off()
                print(f"💡 Light auto-off after {delay}s.")
            else:
                print(f"💡 [Mock] Light auto-off after {delay}s.")
        except asyncio.CancelledError:
            pass

    async def control_motor(self, state=True, duration=0):
        if self.motor:
            print(f"⚙️ Motor {'ON' if state else 'OFF'}")
            if state:
                self.motor.on()
                if duration > 0:
                    await asyncio.sleep(duration)
                    self.motor.off()
            else:
                self.motor.off()
        else:
            print(f"⚙️ [Mock] Motor {'ON' if state else 'OFF'}")
