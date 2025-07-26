import React from "react";

export default function OrderBook({ bids, asks }) {
  return (
    <div style={{ display: "flex" }}>
      <table style={{ marginRight: 10 }}>
        <thead><tr><th>Price</th><th>Qty</th></tr></thead>
        <tbody>
          {asks.slice(0, 10).map(([price, qty], i) => (
            <tr key={i}>
              <td style={{ color: "red" }}>{(+price).toFixed(2)}</td>
              <td>{(+qty).toFixed(4)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <table>
        <thead><tr><th>Price</th><th>Qty</th></tr></thead>
        <tbody>
          {bids.slice(0, 10).map(([price, qty], i) => (
            <tr key={i}>
              <td style={{ color: "green" }}>{(+price).toFixed(2)}</td>
              <td>{(+qty).toFixed(4)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
