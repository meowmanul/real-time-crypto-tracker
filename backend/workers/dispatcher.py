import os, time, requests

from queues import r
from api import manager


PUBLISH_URL = os.getenv("PUBLISH_URL", "http://backend:8000/publish")




def run():
    last_id = b"0-0"
    while True:
        res = r.xread({"orderbook": last_id}, block=1000, count=10)
        if not res:
            continue
        _, messages = res[0]
        for msg_id, data in messages:  
            last_id = msg_id
            try:
                resp = requests.post(PUBLISH_URL, json=data, timeout=1)
                resp.raise_for_status()
            except Exception as e:
                print("⚠️ Broadcast failed:", e)
        
        time.sleep(0.01)




if __name__ == "__main__":
    run()