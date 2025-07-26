import asyncio
from collectors.binance import BinanceCollector


if __name__ == "__main__":
    collector = BinanceCollector("BTCUSDT")
    asyncio.run(collector.run())