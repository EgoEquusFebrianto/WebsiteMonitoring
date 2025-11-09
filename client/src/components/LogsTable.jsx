import React, { useEffect, useState, useContext } from "react";
import { DataContext } from "./DataContext"


const LogsTable = () => {
  const { model, data } = useContext(DataContext);
  const [recentLogs, setRecentLogs] = useState([]);

  // Update recentLogs ketika data berubah
  useEffect(() => {
    const networkEvents = data.networkEvents || [];
    const newRecentLogs = [...networkEvents].slice(-10).reverse();
    setRecentLogs(newRecentLogs);
  }, [data]);

  // Reset recentLogs ketika model berubah
  useEffect(() => {
    setRecentLogs([]);
  }, [model]);

  // // Ambil 10 data terbaru dari networkEvents
  // const networkEvents = data.networkEvents;
  // const recentLogs = [...networkEvents].slice(-10).reverse();

  return (
    <div className="bg-white rounded-2xl p-4 shadow-md col-span-3">
      <h2 className="text-lg font-semibold mb-2">Recent Network Events</h2>
      <table className="w-full text-sm">
        <thead className="bg-gray-200">
          <tr>
            <th className="p-2 text-left">Time</th>
            <th className="p-2 text-left">Source IP</th>
            <th className="p-2 text-left">Prediction</th>
          </tr>
        </thead>
        <tbody>
          {recentLogs.map((log, index) => (
            <tr key={index} className="border-t">
              <td className="p-2">{new Date(log.timestamp).toLocaleTimeString()}</td>
              <td className="p-2">{log.src_ip}</td>
              <td
                className={`p-2 font-semibold ${
                  log.label?.toLowerCase() === "ddos"
                    ? "text-red-600"
                    : "text-green-600"
                }`}
              >
                {log.label}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LogsTable;
