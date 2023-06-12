import asyncio
import time
from websockets.server import serve

stop = None
message = None

CLIENTS = set()


async def relay(queue, websocket):
    while True:
        # Implement custom logic based on queue.qsize() and
        # websocket.transport.get_write_buffer_size() here.
        message = await queue.get()
        await websocket.send(message)


async def handler(websocket):
    queue = asyncio.Queue()
    relay_task = asyncio.create_task(relay(queue, websocket))
    CLIENTS.add(queue)
    try:
        await websocket.wait_closed()
    finally:
        CLIENTS.remove(queue)
        relay_task.cancel()


def broadcast(message):
    for queue in CLIENTS:
        queue.put_nowait(message)


async def broadcast_messages():
    while True:
        await asyncio.sleep(10)
        print("waiting")
        broadcast("message")


async def main():
    async with serve(handler, "localhost", 5678):
        await broadcast_messages()  # runs forever


if __name__ == "__main__":
    asyncio.run(main())
    print("a")

# print(server.sockets[0].getsockname()[1])
