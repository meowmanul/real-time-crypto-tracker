import os, asyncio, json, statistics
import redis.asyncio as aioredis
from ..models import OrderBookSnapshot

STREAM_RAW  = os.getenv("STREAM_RAW",  "crypto_raw")
STREAM_CLEAN = os.getenv("STREAM_CLEAN", "crypto_clean")

WINDOW = 3  # для простого сглаживания

class Normalizer:
    def __init__(self, redis_url="redis://redis:6379/0"):
        self.r = aioredis.from_url(redis_url)
        self.buffers = {}  # symbol → [last N mid‑prices]


    async def run(self):
        last_id = "0-0"
        while True:
            events = await self.r.xread({STREAM_RAW: last_id}, block=1000)
            for _, msgs in events:
                for msg_id, payload in msgs:
                    snap = OrderBookSnapshot(**{k.decode(): json.loads(v) if k in (b"bids", b"asks") else v.decode() for k, v in payload.items()})
                    mid = (float(snap.bids[0].price) + float(snap.asks[0].price)) / 2
                    buff = self.buffers.setdefault(snap.symbol, [])
                    buff.append(mid); buff[:] = buff[-WINDOW:]
                    snap_mid_smoothed = statistics.mean(buff)
                    await self.r.xadd(STREAM_CLEAN, {"json": snap.model_dump_json(), "mid": snap_mid_smoothed})
                    last_id = msg_id


if __name__ == "__main__":
    asyncio.run(Normalizer().run())
