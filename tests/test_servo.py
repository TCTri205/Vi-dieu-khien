import time
from gpiozero import AngularServo
import sys
import os

# Thêm đường dẫn để import Config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.common.config import Config

def test_servo():
    print(f"🧪 Testing Servo on GPIO {Config.SERVO_PIN}...")
    print("⚠️ CẢNH BÁO: Đảm bảo bạn đã cấp nguồn 6V riêng cho Servo và nối chung GND.")
    try:
        servo = AngularServo(Config.SERVO_PIN, min_pulse_width=0.0005, max_pulse_width=0.0025)
        
        print("🔄 1. Moving to 90 degrees (Open)...")
        servo.angle = 90
        time.sleep(2)
        
        print("🔄 2. Moving to 0 degrees (Closed)...")
        servo.angle = 0
        time.sleep(2)
        
        print("🔄 3. Moving to -90 degrees...")
        servo.angle = -90
        time.sleep(2)
        
        print("🔄 4. Returning to 0 degrees...")
        servo.angle = 0
        
        print("✅ Servo test completed.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_servo()
