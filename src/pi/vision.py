import cv2
import face_recognition
import os
from src.common.config import Config

class VisionManager:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self._load_known_faces()

    def _load_known_faces(self):
        self.known_encodings = []
        self.known_names = []
        if not os.path.exists(Config.FACES_DIR):
            os.makedirs(Config.FACES_DIR)
            print(f"📁 Created faces directory: {Config.FACES_DIR}")
            return

        print("⏳ Loading face data...")
        for filename in os.listdir(Config.FACES_DIR):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                name = os.path.splitext(filename)[0]
                path = os.path.join(Config.FACES_DIR, filename)
                try:
                    image = face_recognition.load_image_file(path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        self.known_encodings.append(encodings[0])
                        self.known_names.append(name)
                        print(f"✅ Loaded face: {name}")
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
        
        print(f"🏁 Loaded {len(self.known_names)} faces.")

    def add_face(self, name, frame):
        """Lưu khuôn mặt mới và tải lại dữ liệu."""
        if not os.path.exists(Config.FACES_DIR):
            os.makedirs(Config.FACES_DIR)
        
        path = os.path.join(Config.FACES_DIR, f"{name}.jpg")
        cv2.imwrite(path, frame)
        print(f"💾 Saved new face: {name} at {path}")
        self._load_known_faces() # Reload to update encodings
        return True

    def recognize(self, frame):
        """Thực hiện nhận diện khuôn mặt trên frame ảnh."""
        if not self.known_encodings:
            return "No face data"

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

    def remove_face(self, name):
        """Xóa khuôn mặt và tải lại dữ liệu."""
        path = os.path.join(Config.FACES_DIR, f"{name}.jpg")
        if os.path.exists(path):
            os.remove(path)
            print(f"🗑️ Removed face: {name}")
            self._load_known_faces()
            return True
        return False
