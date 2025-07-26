// src/ws.js
export function createSocket(onMessage) {
  const ws = new WebSocket("ws://localhost:8000/ws");
  ws.onopen = () => console.log("WS connected");
  ws.onmessage = e => {
    let data;
    try {
      data = JSON.parse(e.data);  
      if (typeof data.bids === "string") {
        data.bids = JSON.parse(data.bids);
      }
      if (typeof data.asks === "string") {
        data.asks = JSON.parse(data.asks);
      }
    } catch (err) {
      console.error("WS parse error", err);
      return;
    }
    onMessage(data);
  };
  ws.onerror = err => console.error("WS error", err);
  return ws;
}
