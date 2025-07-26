import os, json, asyncio
import aiohttp, websockets
from .base import BaseCollector
from utils.utils import encode_for_redis
from queues import push


class BinanceCollector(BaseCollector):
    REST_URL = "https://api.binance.com/api/v3/depth"
    WS_URL = "wss://stream.binance.com:9443/ws"

    async def fetch_snapshot(self) -> dict:
        params = {
            "symbol": self.symbol,
            "limit": 100
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.REST_URL, params=params) as response:
                data = await response.json()
        return {
            "type":"snapshot",
            "symbol":self.symbol,
            "bids":data["bids"],
            "asks":data["asks"],
            "timestamp":data["lastUpdateId"],
        }


    async def listen_stream(self, on_message):
        # Стрим глубины стакана: <symbol>@depth
        stream_name = f"{self.symbol.lower()}@depth"
        url = f"{self.WS_URL}/{stream_name}"
        retry_delay = 5  # ждать 5 сек перед новой попыткой

        while True:
            try:
                async with websockets.connect(
                    url,
                    open_timeout=20,
                    ping_interval=20,
                    ping_timeout=20
                ) as ws:
                    print("WebSocket connected")
                    async for raw in ws:
                        msg = json.loads(raw)
                        normalized = {
                            "type": "update",
                            "symbol": self.symbol,
                            "bids": msg["b"],
                            "asks": msg["a"],
                            "timestamp": msg["E"]
                        }
                        await on_message(normalized)
            except (asyncio.TimeoutError, websockets.exceptions.InvalidHandshake) as e:
                print(f"WebSocket error ({e}), reconnecting in {retry_delay}s…")
                await asyncio.sleep(retry_delay)


    async def run(self):
        """
        Запускаем snapshot раз в 30 секунд + постоянно stream:
        """
        async def push_to_queue(data):
            safe_data = encode_for_redis(data)
            loop = asyncio.get_running_loop()
            print("→ Pushing to Redis:", safe_data)
            push("orderbook", safe_data)
            # await loop.run_in_executor(None, push, "orderbook", safe_data)
            # push("orderbook", safe_data)

        await asyncio.gather(
            self._loop_snapshot(push_to_queue),
            self.listen_stream(push_to_queue)
        )

    async def _loop_snapshot(self, on_message):
        while True:
            snapshot = await self.fetch_snapshot()
            await on_message(snapshot)
            await asyncio.sleep(30)


