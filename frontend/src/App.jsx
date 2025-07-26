import React, { useState, useEffect, useRef } from "react";
import { createSocket } from "./ws";
import OrderBook from "./components/OrderBook";
import TradeList  from "./components/TradeList";
import PriceChart from "./components/PriceChart";

export default function App() {
  const [bids, setBids] = useState([]);
  const [asks, setAsks] = useState([]);
  const [trades, setTrades] = useState([]);
  const [prices, setPrices] = useState([]); // для графика

  const wsRef = useRef(null);

  useEffect(() => {
    wsRef.current = createSocket(data => {
      if (data.type === "snapshot" || data.type === "update") {
        setBids(data.bids);
        setAsks(data.asks);
      }
      if (data.type === "trade") {
        setTrades(prev => [data, ...prev].slice(0, 20));
        setPrices(prev => [...prev, { t: data.timestamp, p: +data.price }].slice(-50));
      }
    });
    return () => wsRef.current.close();
  }, []);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ flex: 1, padding: 10 }}>
        <h2>Order Book</h2>
        <OrderBook bids={bids} asks={asks}/>
      </div>
      <div style={{ flex: 1, padding: 10 }}>
        <h2>Price Chart</h2>
        <PriceChart data={prices}/>
        <h2>Recent Trades</h2>
        <TradeList trades={trades}/>
      </div>
    </div>
  );
}