import asyncio
import json
import os
from pathlib import Path

import websockets
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
ch = logging.StreamHandler()
logger.addHandler(ch)

logger.info('Starting server')
DATA_DIR = Path(os.environ.get('PLOTLY_FIG_DIR', '/tmp/plotly'))
DATA_DIR.mkdir(parents=True, exist_ok=True)

client_files = set()
server_files = set()


async def file_diff_producer(websocket, path):
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
                logger.info(f'Sent {sfile}')
        await asyncio.sleep(1)


async def file_updater():
    while True:
        files = set(DATA_DIR.glob('*.json'))
        new_files = files.difference(server_files)
        if new_files:
            logger.info(f'new files {new_files}')
            server_files.update(new_files)
        await asyncio.sleep(1)


async def consumer(websocket, path):
    while True:
        async for message in websocket:
            try:
                files = json.loads(message)
            except json.JSONDecodeError:
                logger.warning(f'Invalid JSON {message}')
                continue

            if not isinstance(files, list):
                logger.warning(f'Invalid data {files}')
                continue

            client_files.clear()
            client_files.update(set(files))
            logger.info(f'Current client files {client_files}')

        await asyncio.sleep(1)


async def handler(websocket, path):
    await asyncio.gather(
        file_diff_producer(websocket, path),
        consumer(websocket, path),
        file_updater(),
    )

if __name__ == '__main__':
    start_server = websockets.serve(handler, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
