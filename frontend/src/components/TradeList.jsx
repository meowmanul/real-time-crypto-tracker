import React from "react";

export default function TradeList({ trades }) {
  return (
    <ul style={{ maxHeight: 200, overflowY: "auto" }}>
      {trades.map((t, i) => (
        <li key={i}>
          <span style={{ color: t.side === "buy" ? "green" : "red" }}>
            {t.side.toUpperCase()}
          </span>{" "}
          {(+t.price).toFixed(2)} @ {(+t.quantity).toFixed(4)}
        </li>
      ))}
    </ul>
  );
}
