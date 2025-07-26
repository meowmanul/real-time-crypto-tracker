import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  TimeScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
} from "chart.js";
import 'chartjs-adapter-date-fns';

ChartJS.register(TimeScale, LinearScale, PointElement, LineElement, Tooltip);

export default function PriceChart({ data }) {
  const chartData = {
    datasets: [{
      label: "Price",
      data: data.map(d => ({ x: d.t, y: d.p })),
      tension: 0.1,
      borderWidth: 1,
    }]
  };

  const options = {
    scales: {
      x: { type: "time", time: { unit: "second", tooltipFormat: 'HH:mm:ss' } },
      y: { beginAtZero: false }
    },
    animation: false,
    plugins: { legend: { display: false } },
  };

  return <Line data={chartData} options={options} />;
}
