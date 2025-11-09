import React, { useRef, useContext, useState, useEffect} from "react";
import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts";
import { DataContext } from "./DataContext"

const AttackSummary = () => {
  const recordRef = useRef({ benign: 0, ddos: 0 }); // menyimpan total kumulatif
  const [chartData, setChartData] = useState([
    { name: "Benign", value: 0 },
    { name: "DDoS", value: 0 },
  ]);

  const { data, model } = useContext(DataContext);

  useEffect(() => {
    const latest = data.attackSummary?.[0];
    if (!latest) return;

    recordRef.current.benign += latest.benign_count || 0;
    recordRef.current.ddos += latest.ddos_count || 0;

    setChartData([
      { name: "Benign", value: recordRef.current.benign },
      { name: "DDoS", value: recordRef.current.ddos },
    ]);
  }, [data]);

  useEffect(() => {
    recordRef.current = { benign: 0, ddos: 0 };
    setChartData([
      { name: "Benign", value: 0 },
      { name: "DDoS", value: 0 },
    ]);
  }, [model]);

  const COLORS = ["#4CAF50", "#FF5722"];

  return (
    <div className="bg-white rounded-2xl p-4 shadow-md">
      <h2 className="text-lg font-semibold mb-2">Attack Summary</h2>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            outerRadius={80}
            label={({ name, value }) => `${name}: ${value}`}
            dataKey="value"
          >
            {chartData.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AttackSummary;
