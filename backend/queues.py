import os
import redis # type: ignore

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), 
    port=int(os.getenv("REDIS_PORT", 6379)), 
    decode_responses=True
)


def push(stream: str, data: dict):
    r.xadd(stream, data)
