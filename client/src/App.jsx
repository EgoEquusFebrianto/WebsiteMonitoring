import { useEffect, useState, useRef } from "react";
import DashboardLayout from "./components/DashboardLayout";
import TrafficOverview from "./components/TrafficOverview";
import AttackSummary from "./components/AttackSummary";
import RealTimeStatus from "./components/RealTimeStatus";
import LogsTable from "./components/LogsTable";
import ModelSelector from "./components/ModelSelector";
import { DataProvider } from "./components/DataContext"; "./components/DataContext"
import './App.css'

function App() {

  return (
    <DataProvider>
      <DashboardLayout>
        <ModelSelector />
        <RealTimeStatus />
        <AttackSummary />
        <TrafficOverview />
        <LogsTable />
      </DashboardLayout>
    </DataProvider>
  )
}

export default App
