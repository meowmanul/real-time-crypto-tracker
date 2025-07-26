import json
from typing import Any, Dict


def encode_for_redis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Преобразует значения-списки в JSON-строки, а остальные значения — в обычные строки,
    чтобы их можно было безопасно положить в Redis Streams.
    """
    encoder = json.JSONEncoder()
    encoded: Dict[str, str] = {}
    for key, value in data.items():
        if isinstance(value, list) or isinstance(value, dict):
            encoded[key] = encoder.encode(value)
        else:
            encoded[key] = str(value)
    return encoded