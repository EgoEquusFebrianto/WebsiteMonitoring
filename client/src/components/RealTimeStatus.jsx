import React, { useContext, useMemo } from "react";
import { DataContext } from "./DataContext"

const RealTimeStatus = () => {
  const { data } = useContext(DataContext);

  const latestSummary = useMemo(() => {
    if (!data?.attackSummary?.length) return null;
    return data.attackSummary[0];
  }, [data]);
  
    const ddosCount = latestSummary?.ddos_count ?? 0;

  let status = "✅ Safe";
  let bgColor = "bg-green-600";

  if (ddosCount > 5) {
    status = "🔥 DDoS Detected";
    bgColor = "bg-red-600";
  } else if (ddosCount > 0) {
    status = "⚠️ Suspicious Activity";
    bgColor = "bg-yellow-500";
  }

  return (
    <div
      className={`rounded-2xl p-6 shadow-md text-center text-white font-semibold text-lg transition-colors duration-500 ${bgColor}`}
    >
      {status}
    </div>
  );
};

export default RealTimeStatus;
