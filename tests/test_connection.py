import asyncio
import json
import base64
import uuid
import cv2
import numpy as np
import websockets
import sys
import os

# Để có thể import từ src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.common.config import Config

async def run_simulation():
    uri = f"ws://{Config.SERVER_IP}:{Config.SERVER_PORT}"
    print(f"🧪 Bắt đầu mô phỏng kết nối tới: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            request_id = "test_" + str(uuid.uuid4())[:4]
            print(f"🆔 Tạo Request ID: {request_id}")
            
            # 1. Tạo ảnh giả lập (Màu xanh lá cây)
            print("📸 1. Tạo ảnh giả lập...")
            img = np.zeros((480, 640, 3), np.uint8)
            img[:] = (0, 255, 0) # Màu xanh
            cv2.putText(img, f"SIMULATION: {request_id}", (50, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            _, buffer = cv2.imencode('.jpg', img)
            img_str = base64.b64encode(buffer).decode('utf-8')
            
            # 2. Gửi ảnh lên server
            print("🚀 2. Gửi ảnh lên server...")
            payload_img = {
                "request_id": request_id,
                "type": "image",
                "data": img_str
            }
            await websocket.send(json.dumps(payload_img))
            print("✅ Đã gửi ảnh.")
            
            # Chờ 2 giây giả lập việc Pi đang xử lý AI
            print("⏳ 3. Đang giả lập xử lý nhận diện (2s)...")
            await asyncio.sleep(2)
            
            # 3. Gửi kết quả nhận diện
            print("🚀 4. Gửi kết quả nhận diện (Admin)...")
            payload_res = {
                "request_id": request_id,
                "type": "result",
                "data": "Admin"
            }
            await websocket.send(json.dumps(payload_res))
            print("✅ Đã gửi kết quả.")
            
            print("\n🎉 MÔ PHỎNG HOÀN TẤT!")
            print("👉 Kiểm tra Terminal của start_server.py và Telegram Bot của bạn.")
            
    except Exception as e:
        print(f"❌ Lỗi: Không thể kết nối tới Server. Đảm bảo start_server.py đang chạy.")
        print(f"Chi tiết: {e}")

if __name__ == "__main__":
    asyncio.run(run_simulation())
