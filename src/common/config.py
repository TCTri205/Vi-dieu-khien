import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Network
    SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
    SERVER_PORT = int(os.getenv("SERVER_PORT", 8765))
    
    # Pi Hardware GPIO
    TRIG_PIN = int(os.getenv("TRIG_PIN", 23))
    ECHO_PIN = int(os.getenv("ECHO_PIN", 24))
    SERVO_PIN = int(os.getenv("SERVO_PIN", 18))
    BUZZER_PIN = int(os.getenv("BUZZER_PIN", 25))
    LIGHT_PIN = int(os.getenv("LIGHT_PIN", 17))
    MOTOR_PIN = int(os.getenv("MOTOR_PIN", 27))
    
    # Logic
    DISTANCE_THRESHOLD = 0.05  # 5cm (gpiozero trả về mét)
    CAPTURE_DELAY = 1.0 # seconds
    RE_TRIGGER_DELAY = 5.0 # seconds
    GATE_HOLD_TIME = 3.0 # seconds
    LIGHT_AUTO_OFF_TIME = 3600 # 1 hour (seconds)
    
    # Buzzer timing
    BUZZER_SHORT_BEEP = 0.2
    BUZZER_ALERT_BEEP = 0.1
    BUZZER_ALERT_COUNT = 3
    
    # Paths
    FACES_DIR = "data/faces/"
