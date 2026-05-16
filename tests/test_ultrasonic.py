import time
from gpiozero import DistanceSensor
import sys
import os

# Thêm đường dẫn để import Config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.common.config import Config

def test_ultrasonic():
    print(f"🧪 Testing Ultrasonic Sensor (Trig={Config.TRIG_PIN}, Echo={Config.ECHO_PIN})...")
    print("⚠️ CẢNH BÁO: Đảm bảo đã có mạch phân áp cho chân Echo!")
    try:
        sensor = DistanceSensor(echo=Config.ECHO_PIN, trigger=Config.TRIG_PIN)
        
        print("📡 Reading distance for 10 seconds. Wave your hand in front of the sensor...")
        for i in range(20):
            distance_cm = sensor.distance * 100
            print(f"   [{i+1}] Distance: {distance_cm:.2f} cm")
            
            if distance_cm < 30:
                print("   ⚠️ THRESHOLD REACHED (< 30cm)!")
                
            time.sleep(0.5)
            
        print("✅ Ultrasonic test completed.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ultrasonic()
