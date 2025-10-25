from fastapi import FastAPI, WebSocket
import os, json, asyncio
import websockets

app = FastAPI()

@app.websocket("/ws")
async def sales_ws(websocket: WebSocket):
    await websocket.accept()
    # 1. 读入系统提示词
    sys_prompt = open("prompt.txt", encoding="utf-8").read()
    # 2. 百炼 websocket 地址
    uri = "wss://bailiang.aliyuncs.com/ws"
    # 3. 环境变量里取长期 Token
    token = os.getenv("BL_TOKEN")
    headers = {"Authorization": "Bearer " + token}
    async with websockets.connect(uri, extra_headers=headers) as bl_ws:
        # 先发送系统提示
        await bl_ws.send(json.dumps({"header": {"action": "start"}, "payload": {"prompt": sys_prompt}}))
        while True:
            data = await websocket.receive_text()          # 销售说的话
            await bl_ws.send(json.dumps({"header": {"action": "continue"}, "payload": {"text": data}}))
            reply = await bl_ws.recv()
            await websocket.send_text(json.loads(reply)["payload"]["text"])