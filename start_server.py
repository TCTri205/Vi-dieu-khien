import asyncio
import json
import base64
import websockets
from src.common.config import Config
from src.server.bot import TelegramManager

class ServerManager:
    def __init__(self):
        self.bot = TelegramManager(command_callback=self.relay_command)
        self.pending_requests = {}
        self.pending_registrations = {}
        self.active_clients = set()

    async def handle_connection(self, websocket, path=None):
        print(f"🔗 Connected: {websocket.remote_address}")
        self.active_clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                req_id = data.get("request_id")
                msg_type = data.get("type")
                
                if msg_type == "register_image":
                    name = data.get("name")
                    image_data = base64.b64decode(data.get("data"))
                    print(f"📸 Received registration image for {name}")
                    await self.bot.send_registration_photo(name, image_data)
                    continue

                if not req_id: continue
                
                if req_id not in self.pending_requests:
                    self.pending_requests[req_id] = {'image': None, 'result': None}
                
                if msg_type == "image":
                    print(f"🖼️ Received image for [{req_id}]")
                    self.pending_requests[req_id]['image'] = base64.b64decode(data.get("data"))
                elif msg_type == "result":
                    print(f"📝 Received result for [{req_id}]: {data.get('data')}")
                    self.pending_requests[req_id]['result'] = data.get("data")
                
                await self._check_and_send(req_id)
        except websockets.exceptions.ConnectionClosed:
            print(f"❌ Disconnected: {websocket.remote_address}")
        finally:
            self.active_clients.remove(websocket)

    async def relay_command(self, command, params):
        """Relay commands from Telegram to all connected Pi clients."""
        if not self.active_clients:
            print("⚠️ No Pi clients connected to relay command.")
            return
        
        payload = {"type": "command", "command": command, "params": params}
        message = json.dumps(payload)
        for ws in list(self.active_clients):
            try:
                await ws.send(message)
            except Exception as e:
                print(f"❌ Error relaying command to {ws.remote_address}: {e}")

    async def _check_and_send(self, req_id):
        req = self.pending_requests.get(req_id)
        if req and req['image'] and req['result']:
            print(f"📧 Sending report [{req_id}]...")
            success = await self.bot.send_report(req_id, req['result'], req['image'])
            if success:
                del self.pending_requests[req_id]

async def main():
    manager = ServerManager()
    await manager.bot.start()
    print(f"🚀 Server listening on port {Config.SERVER_PORT}...")
    async with websockets.serve(manager.handle_connection, "0.0.0.0", Config.SERVER_PORT):
        try:
            await asyncio.Future() # run forever
        finally:
            await manager.bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
