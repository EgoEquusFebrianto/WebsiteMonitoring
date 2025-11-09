import React from "react";

const DashboardLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-700 text-white p-4 shadow-md">
        <h1 className="text-2xl font-semibold text-center">
          DDoS Network Monitoring Dashboard
        </h1>
      </header>
      <main className="p-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {children}
      </main>
    </div>
  );
};

export default DashboardLayout;
