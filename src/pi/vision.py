import cv2
import face_recognition
import os
from src.common.config import Config

class VisionManager:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self._load_admin_data()

    def _load_admin_data(self):
        if os.path.exists(Config.ADMIN_FACE_PATH):
            print("⏳ Loading face data...")
            image = face_recognition.load_image_file(Config.ADMIN_FACE_PATH)
            encoding = face_recognition.face_encodings(image)[0]
            self.known_encodings.append(encoding)
            self.known_names.append("Admin")
            print("✅ Face data loaded.")
        else:
            print(f"⚠️ Admin face not found at {Config.ADMIN_FACE_PATH}")

    def recognize(self, frame):
        """Thực hiện nhận diện khuôn mặt trên frame ảnh."""
        # Tối ưu: Resize nhỏ lại để xử lý nhanh
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                return self.known_names[first_match_index]
                
        return "Unknown"
