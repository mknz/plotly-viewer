import asyncio
import json
import time
from pathlib import Path

import websockets


DATA_DIR = Path('/tmp/plotly')


client_files = set()
server_files = set()

async def producer(websocket, path):
    while True:
        for sfile in server_files:
            if sfile.name not in client_files:
                with sfile.open('r') as f:
                    fig = json.load(f)
                data = {}
                data['fig'] = fig
                data['id'] = str(sfile.name)
                data_str = json.dumps(data)
                await websocket.send(data_str)
                print(f'Sent {sfile}')
        await asyncio.sleep(2)


async def file_updater():
    while True:
        files = set(DATA_DIR.glob('*.json'))
        new_files = files.difference(server_files)
        if new_files:
            print(f'new files {new_files}')
            server_files.update(new_files)
        await asyncio.sleep(2)


async def consumer(websocket, path):
    while True:
        async for message in websocket:
            try:
                files = json.loads(message)
            except json.JSONDecodeError:
                print(f'Invalid JSON {message}')
                continue

            if not isinstance(files, list):
                print(f'Invalid data {files}')
                continue

            client_files.clear()
            client_files.update(set(files))
            print(f'Current client files {client_files}')

        await asyncio.sleep(2)


async def handler(websocket, path):
    await asyncio.gather(
        producer(websocket, path),
        consumer(websocket, path),
        file_updater(),
    )

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
