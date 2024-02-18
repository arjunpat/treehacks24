import asyncio
import websockets
import json

async def receive_progress():
    async with websockets.connect('ws://localhost:8000/generate') as websocket:
        await websocket.send(json.dumps({"question": "When is Clement's birthday?"}))
        while True:
            message = await websocket.recv()
            body = json.loads(message)
            print(body)
            if body["status"] != "progress":
                break

asyncio.run(receive_progress())
