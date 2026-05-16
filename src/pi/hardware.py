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
            print("✅ Hardware initialized.")
        except Exception as e:
            print(f"⚠️ Hardware init error (Mock mode enabled): {e}")
            self.sensor = None
            self.servo = None
            self.light = None
            self.motor = None

    def get_distance(self):
        if self.sensor:
            return self.sensor.distance
        return 1.0 # Mock distance

    async def open_gate(self):
        if self.servo:
            print("🚪 Opening gate...")
            self.servo.angle = 90
            await asyncio.sleep(2)
            self.servo.angle = 0
        else:
            print("🚪 [Mock] Gate opened.")

    async def control_light(self, state=True, duration=0):
        if self.light:
            print(f"💡 Light {'ON' if state else 'OFF'}")
            if state:
                self.light.on()
                if duration > 0:
                    await asyncio.sleep(duration)
                    self.light.off()
            else:
                self.light.off()
        else:
            print(f"💡 [Mock] Light {'ON' if state else 'OFF'}")

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
