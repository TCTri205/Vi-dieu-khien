import cv2
import asyncio
import uuid
from src.common.config import Config
from src.pi.hardware import HardwareManager
from src.pi.vision import VisionManager
from src.pi.networking import PiNetworking

async def process_detection(request_id, frame, vision, net, hardware):
    """Xử lý song song việc gửi ảnh và nhận diện."""
    # Luồng 1: Upload ảnh thô
    upload_task = asyncio.create_task(net.upload_image(request_id, frame))
    
    # Luồng 2: Nhận diện và thông báo kết quả
    result = await asyncio.to_thread(vision.recognize, frame)
    print(f"🎯 [{request_id}] Result: {result}")
    await net.upload_result(request_id, result)
    
    if result not in ["Unknown", "No face data"]:
        # Thực hiện các thao tác chào mừng
        await hardware.beep_welcome()
        
        # Mở cửa trước, sau đó bật đèn và quạt
        await hardware.open_gate()
        await hardware.control_light(state=True)
        await hardware.control_motor(state=True)
    else:
        # Người lạ hoặc chưa có dữ liệu: Cảnh báo
        await hardware.beep_alert()
    
    await upload_task

class PiSystem:
    def __init__(self):
        self.hardware = HardwareManager()
        self.vision = VisionManager()
        self.net = PiNetworking()
        self.video_capture = cv2.VideoCapture(0)
        self.last_frame = None
        self.reg_frame = None # Frame to be registered
        self.reg_name = None

    async def handle_command(self, command, params):
        """Handle commands received from the server."""
        state = params.get("state", True)
        if command == "light":
            await self.hardware.control_light(state)
        elif command == "motor":
            await self.hardware.control_motor(state)
        elif command == "gate":
            await self.hardware.open_gate()
        elif command == "register_request":
            name = params.get("name")
            print(f"📸 Registration request for: {name}")
            if self.last_frame is not None:
                self.reg_frame = self.last_frame.copy()
                self.reg_name = name
                await self.net.upload_register_image(name, self.reg_frame)
            else:
                print("⚠️ No frame captured yet.")
        elif command == "remove":
            name = params.get("name")
            print(f"🗑️ Remove request for: {name}")
            success = await asyncio.to_thread(self.vision.remove_face, name)
            if success:
                print(f"✅ Successfully removed: {name}")
            else:
                print(f"⚠️ Face not found: {name}")
        elif command == "register_confirm":
            name = params.get("name")
            if self.reg_frame is not None and self.reg_name == name:
                await asyncio.to_thread(self.vision.add_face, name, self.reg_frame)
                print(f"✅ Successfully registered face: {name}")
                self.reg_frame = None
                self.reg_name = None
            else:
                print(f"⚠️ Registration confirmation mismatch or no frame for {name}")
        else:
            print(f"❓ Unknown command: {command}")

    async def run(self):
        # Start command listener task
        asyncio.create_task(self.net.listen_for_commands(self.handle_command))
        
        print("🚀 System started. Monitoring and listening for commands...")

        while True:
            # Đảm bảo camera sẵn sàng
            if not self.video_capture.isOpened():
                print("⚠️ Camera not ready, retrying...")
                self.video_capture.open(0)
                await asyncio.sleep(2)
                continue

            ret, frame = self.video_capture.read()
            if ret:
                self.last_frame = frame
            else:
                print("⚠️ Failed to read from camera.")
                await asyncio.sleep(1)
                continue

            current_distance = self.hardware.get_distance()
            
            if current_distance < Config.DISTANCE_THRESHOLD:
                print(f"⚠️ Obstacle detected! Distance: {current_distance*100:.1f}cm")
                await asyncio.sleep(Config.CAPTURE_DELAY)
                
                # Re-read to get a fresh frame after delay
                ret, frame = self.video_capture.read()
                if ret:
                    request_id = str(uuid.uuid4())[:8]
                    asyncio.create_task(process_detection(request_id, frame, self.vision, self.net, self.hardware))
                
                await asyncio.sleep(Config.RE_TRIGGER_DELAY)
            
            await asyncio.sleep(0.05)

async def main():
    system = PiSystem()
    try:
        await system.run()
    finally:
        system.hardware.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped.")
