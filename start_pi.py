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
    
    if result == "Admin":
        # Thực hiện các thao tác chào mừng
        await hardware.beep_welcome()
        
        # Chạy song song: Mở cửa và Bật đèn (đèn sáng ngay khi cửa mở)
        await asyncio.gather(
            hardware.open_gate(),
            hardware.control_light(state=True)
        )
    else:
        # Người lạ: Cảnh báo
        await hardware.beep_alert()
    
    await upload_task

async def handle_command(command, params, hardware):
    """Handle commands received from the server."""
    state = params.get("state", True)
    if command == "light":
        await hardware.control_light(state)
    elif command == "motor":
        await hardware.control_motor(state)
    elif command == "gate":
        await hardware.open_gate()
    else:
        print(f"❓ Unknown command: {command}")

async def main():
    hardware = HardwareManager()
    vision = VisionManager()
    net = PiNetworking()
    
    # Start command listener task
    asyncio.create_task(net.listen_for_commands(
        lambda cmd, params: handle_command(cmd, params, hardware)
    ))
    
    video_capture = cv2.VideoCapture(0)
    print("🚀 System started. Monitoring and listening for commands...")

    while True:
        current_distance = hardware.get_distance()
        
        if current_distance < Config.DISTANCE_THRESHOLD:
            print(f"⚠️ Obstacle detected! Distance: {current_distance*100:.1f}cm")
            await asyncio.sleep(Config.CAPTURE_DELAY)
            
            ret, frame = video_capture.read()
            if ret:
                request_id = str(uuid.uuid4())[:8]
                asyncio.create_task(process_detection(request_id, frame, vision, net, hardware))
            
            await asyncio.sleep(Config.RE_TRIGGER_DELAY)
        
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped.")
