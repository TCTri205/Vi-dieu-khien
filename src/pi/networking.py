import asyncio
import websockets
import json
import base64
import cv2
from src.common.config import Config

class PiNetworking:
    def __init__(self):
        self.uri = f"ws://{Config.SERVER_IP}:{Config.SERVER_PORT}"
        self.websocket = None
        self.lock = asyncio.Lock()

    async def ensure_connection(self):
        async with self.lock:
            if self.websocket is None or self.websocket.closed:
                try:
                    self.websocket = await websockets.connect(self.uri, ping_interval=20)
                    print(f"🔗 Connected to server at {self.uri}")
                except Exception as e:
                    print(f"❌ Connection failed: {e}")
                    return False
        return True

    async def send_payload(self, payload):
        if await self.ensure_connection():
            try:
                await self.websocket.send(json.dumps(payload))
            except Exception as e:
                print(f"❌ Send error: {e}")
                self.websocket = None

    async def upload_image(self, request_id, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        img_str = base64.b64encode(buffer).decode('utf-8')
        payload = {"request_id": request_id, "type": "image", "data": img_str}
        await self.send_payload(payload)

    async def upload_result(self, request_id, result):
        payload = {"request_id": request_id, "type": "result", "data": result}
        await self.send_payload(payload)

    async def upload_register_image(self, name, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        img_str = base64.b64encode(buffer).decode('utf-8')
        payload = {"type": "register_image", "name": name, "data": img_str}
        await self.send_payload(payload)

    async def listen_for_commands(self, callback):
        """Listen for incoming commands from the server."""
        while True:
            if await self.ensure_connection():
                try:
                    message = await self.websocket.recv()
                    data = json.loads(message)
                    if data.get("type") == "command":
                        await callback(data.get("command"), data.get("params", {}))
                except websockets.exceptions.ConnectionClosed:
                    print("⚠️ Connection closed by server. Retrying...")
                    self.websocket = None
                except Exception as e:
                    print(f"⚠️ Listen error: {e}")
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(5)
