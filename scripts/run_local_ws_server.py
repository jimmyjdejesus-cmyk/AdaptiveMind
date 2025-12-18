#!/usr/bin/env python3
"""Simple WebSocket test server used by the local test suite.

Listens on 127.0.0.1:8000 and responds to JSON ping messages on
/ws/pytest_client with a JSON pong message.
"""
import asyncio
import json
import logging
import signal

import websockets

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("local_ws_server")


async def handler(ws, path):
    log.info("Connection to path: %s", path)
    if path != "/ws/pytest_client":
        log.warning("Unexpected path: %s, closing", path)
        await ws.close()
        return
    try:
        async for msg in ws:
            try:
                data = json.loads(msg)
            except Exception:
                data = None
            if isinstance(data, dict) and data.get("type") == "ping":
                await ws.send(json.dumps({"type": "pong"}))
            else:
                # echo fallback
                await ws.send(msg)
    except websockets.ConnectionClosed:
        log.info("Connection closed")


async def main():
    server = await websockets.serve(handler, "127.0.0.1", 8000)
    log.info("WebSocket test server listening on ws://127.0.0.1:8000/ws/pytest_client")

    loop = asyncio.get_running_loop()
    stop = asyncio.Future()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.cancel)
    try:
        await stop
    finally:
        server.close()
        await server.wait_closed()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
