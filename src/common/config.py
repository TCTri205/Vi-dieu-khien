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
    SERVO_PIN = int(os.getenv("SERVO_PIN", 5))
    LIGHT_PIN = int(os.getenv("LIGHT_PIN", 17))
    MOTOR_PIN = int(os.getenv("MOTOR_PIN", 27))
    
    # Logic
    DISTANCE_THRESHOLD = 0.03 # 3cm
    CAPTURE_DELAY = 1.0 # seconds
    RE_TRIGGER_DELAY = 5.0 # seconds
    
    # Paths
    ADMIN_FACE_PATH = "data/faces/admin.jpg"
