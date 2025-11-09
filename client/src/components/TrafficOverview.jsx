import React, { useEffect, useState, useContext } from "react";
import { DataContext } from "./DataContext"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const TrafficOverview = () => {
  const { model, data } = useContext(DataContext);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    // Ambil record terbaru
    const latest = data.attackSummary?.[0];
    if (!latest) return;

    const benignCount = latest?.benign_count || 0;
    const ddosCount = latest?.ddos_count || 0;

    // Buat titik data baru
    const newPoint = {
      time: new Date().toLocaleTimeString(), // waktu sekarang
      benign: benignCount,
      ddos: ddosCount,
    };

    // Simpan max 30 data terakhir
    setChartData((prev) => [...prev.slice(-15), newPoint]);
  }, [data]);

  useEffect(() => {
    setChartData([]); // Mengosongkan data chart
  }, [model]);

  return (
    <div className="bg-white rounded-2xl p-4 shadow-md col-span-2">
      <h2 className="text-lg font-semibold mb-2">Traffic Overview</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line dataKey="benign" stroke="#4CAF50" name="Normal Traffic" />
          <Line dataKey="ddos" stroke="#FF5722" name="DDoS Traffic" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrafficOverview;
