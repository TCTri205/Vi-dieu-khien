import time
from gpiozero import OutputDevice
import sys
import os

# Thêm đường dẫn để import Config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.common.config import Config

def test_buzzer():
    print(f"🧪 Testing Buzzer on GPIO {Config.BUZZER_PIN}...")
    try:
        buzzer = OutputDevice(Config.BUZZER_PIN)
        
        print("🔊 1. Short beep (Welcome mode)...")
        buzzer.on()
        time.sleep(0.2)
        buzzer.off()
        
        time.sleep(1)
        
        print("🔊 2. Three beeps (Alert mode)...")
        for i in range(3):
            print(f"   - Beep {i+1}")
            buzzer.on()
            time.sleep(0.1)
            buzzer.off()
            time.sleep(0.1)
            
        print("✅ Buzzer test completed.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_buzzer()
